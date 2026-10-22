from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    flowdesk_approval_ids = fields.One2many('flowdesk.discount.approval', 'order_id', string="Discount Approvals")
    flowdesk_discount_state = fields.Selection(
        [('required', "Approval Required"), ('waiting', "Waiting for Approval"),
         ('approved', "Discount Approved"), ('rejected', "Discount Rejected")],
        string="Discount Approval", compute='_compute_flowdesk_discount_state')

    # N2: "no reply" = no customer message in the chatter since the quotation was sent.
    flowdesk_sent_date = fields.Datetime(string="Sent On", copy=False, readonly=True)
    flowdesk_days_waiting = fields.Integer(
        string="Days Waiting", copy=False, readonly=True,
        help="Days since the quotation was sent or the customer last wrote. Refreshed daily.")
    flowdesk_followup_date = fields.Datetime(copy=False, readonly=True)
    flowdesk_escalation_date = fields.Datetime(copy=False, readonly=True)

    @api.depends('sale_order_template_id')
    def _compute_payment_term_id(self):
        # C2: template payment terms win over the partner's
        super()._compute_payment_term_id()
        for order in self.filtered('sale_order_template_id.payment_term_id'):
            order.payment_term_id = order.sale_order_template_id.payment_term_id

    @api.depends('order_line.discount', 'user_id', 'flowdesk_approval_ids.state')
    def _compute_flowdesk_discount_state(self):
        for order in self:
            order.flowdesk_discount_state = order._flowdesk_get_state()

    def _flowdesk_get_state(self):
        self.ensure_one()
        over = self._flowdesk_over_limit_lines()
        if not over:
            return False
        if not self._flowdesk_uncovered_lines():
            return 'approved'
        # sudo: salespeople only read their own approvals through the record rule
        approvals = self.sudo().flowdesk_approval_ids.filtered(lambda a: a.state != 'cancelled')
        if approvals.filtered(lambda a: a.state == 'waiting'):
            return 'waiting'
        if approvals[:1].state == 'rejected' and approvals[0].snapshot == self._flowdesk_snapshot(over):
            return 'rejected'
        return 'required'

    # C11: both typed-by-hand and pricelist discounts count, we check the final discount on the line.
    def _flowdesk_discount_limit(self):
        """Max discount % of the salesperson, None when unlimited (sales managers)."""
        self.ensure_one()
        user = (self.user_id or self.create_uid or self.env.user).sudo()
        if user.has_group('sales_team.group_sale_manager'):
            return None
        return user.flowdesk_max_discount

    def _flowdesk_over_limit_lines(self):
        self.ensure_one()
        limit = self._flowdesk_discount_limit()
        if limit is None:
            return self.order_line.browse()
        return self.order_line.filtered(lambda l: not l.display_type and l.discount > limit)

    def _flowdesk_snapshot(self, lines):
        return {str(l._origin.id or l.id): l.discount for l in lines}

    def _flowdesk_uncovered_lines(self):
        """Lines over the limit whose discount was not approved (a higher discount than approved needs a new approval)."""
        self.ensure_one()
        approved = self.sudo().flowdesk_approval_ids.filtered(lambda a: a.state == 'approved')
        return self._flowdesk_over_limit_lines().filtered(
            lambda l: not any((a.snapshot or {}).get(str(l._origin.id or l.id), -1) >= l.discount for a in approved))

    def _flowdesk_sync_approval(self):
        """Open (or refresh / cancel) the approval request so the manager is notified as soon as the line is saved."""
        for order in self.filtered(lambda o: o.id and o.state in ('draft', 'sent')):
            # sudo: salespeople can not create approvals, the system does it for them
            order_sudo = order.sudo()
            waiting = order_sudo.flowdesk_approval_ids.filtered(lambda a: a.state == 'waiting')
            if not order_sudo._flowdesk_uncovered_lines():
                waiting._cancel()
                continue
            over = order_sudo._flowdesk_over_limit_lines()
            snapshot = order_sudo._flowdesk_snapshot(over)
            vals = {
                'limit': order_sudo._flowdesk_discount_limit(),
                'max_discount': max(over.mapped('discount')),
                'snapshot': snapshot,
                'line_detail': "\n".join("%s: %s%%" % (l.name.split('\n')[0], l.discount) for l in over),
            }
            if waiting:
                waiting[:1].write(vals)
                (waiting - waiting[:1])._cancel()
                continue
            rejected = order_sudo.flowdesk_approval_ids.filtered(lambda a: a.state == 'rejected')[:1]
            if rejected and rejected.snapshot == snapshot:
                continue
            approval = self.env['flowdesk.discount.approval'].sudo().create(
                dict(vals, order_id=order.id, salesperson_id=(order.user_id or order.create_uid).id))
            approval._notify_managers()

    def _flowdesk_last_contact(self):
        """Latest of: sent date, last message written by the customer (or a colleague of theirs)."""
        self.ensure_one()
        last = self.flowdesk_sent_date or self.write_date
        message = self.env['mail.message'].sudo().search([
            ('model', '=', 'sale.order'), ('res_id', '=', self.id),
            ('message_type', 'in', ('email', 'comment')),
            ('author_id', 'child_of', self.partner_id.commercial_partner_id.id),
        ], order='date desc', limit=1)
        return max(last, message.date) if message else last

    def _flowdesk_manager(self):
        self.ensure_one()
        manager = self.team_id.user_id
        if not manager:
            manager = self.env.ref('sales_team.group_sale_manager').sudo().user_ids.filtered(
                lambda u: u.active and u.id != self.env.ref('base.user_root').id)[:1]
        return manager

    def _flowdesk_has_open_activity(self, xmlid):
        self.ensure_one()
        return bool(self.activity_ids.filtered(lambda a: a.activity_type_id == self.env.ref(xmlid)))

    @api.model
    def _cron_flowdesk_followup(self):
        get = self.env['ir.config_parameter'].sudo().get_param
        followup_days = int(get('flowdesk.followup_days', 3))
        escalation_days = int(get('flowdesk.escalation_days', 7))
        # confirmed / cancelled quotations are no longer waiting
        self.search([('state', '!=', 'sent'), ('flowdesk_days_waiting', '!=', 0)]).write({'flowdesk_days_waiting': 0})
        now = fields.Datetime.now()
        for order in self.search([('state', '=', 'sent')]):
            last = order._flowdesk_last_contact()
            days = (now - last).days
            if order.flowdesk_days_waiting != days:
                order.flowdesk_days_waiting = days
            # a customer reply after our reminder starts a new cycle
            if order.flowdesk_followup_date and order.flowdesk_followup_date < last:
                order.flowdesk_followup_date = order.flowdesk_escalation_date = False
            if days >= followup_days and not order.flowdesk_followup_date \
                    and not order._flowdesk_has_open_activity('flowdesk.activity_type_follow_up'):
                order.activity_schedule(
                    'flowdesk.activity_type_follow_up', user_id=(order.user_id or order._flowdesk_manager()).id,
                    summary=_("Follow up: no answer for %s days", days))
                order.flowdesk_followup_date = now
            manager = order._flowdesk_manager()
            if days >= escalation_days and manager and not order.flowdesk_escalation_date \
                    and not order._flowdesk_has_open_activity('flowdesk.activity_type_escalation'):
                order.activity_schedule(
                    'flowdesk.activity_type_escalation', user_id=manager.id,
                    summary=_("Escalation: no answer for %s days", days))
                order.flowdesk_escalation_date = now

    def _flowdesk_check_discount(self):
        # portal / website customers confirm with their own user: only internal users are gated
        if not self.env.user._is_internal():
            return
        for order in self:
            if order._flowdesk_uncovered_lines():
                state = dict(self._fields['flowdesk_discount_state'].selection)[order._flowdesk_get_state()]
                raise UserError(_(
                    "%(order)s has a discount above your limit of %(limit)s%% (%(state)s). "
                    "A sales manager must approve it before it can be sent or confirmed.",
                    order=order.name, limit=order._flowdesk_discount_limit(), state=state))

    def action_flowdesk_request_approval(self):
        self._flowdesk_sync_approval()

    def _confirmation_error_message(self):
        # also used by the customer portal, so it blocks every confirm path
        error = super()._confirmation_error_message()
        if not error and self._flowdesk_uncovered_lines():
            self._flowdesk_check_discount()
        return error

    def action_quotation_send(self):
        self._flowdesk_check_discount()
        return super().action_quotation_send()

    def action_quotation_sent(self):
        self._flowdesk_check_discount()
        return super().action_quotation_sent()

    def message_post(self, **kwargs):
        # the email wizard marks the quotation as sent through message_post
        if self.env.context.get('mark_so_as_sent'):
            self._flowdesk_check_discount()
        return super().message_post(**kwargs)

    def write(self, vals):
        if vals.get('state') == 'sent':
            vals = dict(vals, flowdesk_sent_date=fields.Datetime.now(), flowdesk_days_waiting=0,
                        flowdesk_followup_date=False, flowdesk_escalation_date=False)
        res = super().write(vals)
        if 'user_id' in vals:
            self._flowdesk_sync_approval()
        return res


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    flowdesk_over_limit = fields.Boolean(compute='_compute_flowdesk_over_limit')

    @api.depends('discount', 'order_id.user_id')
    def _compute_flowdesk_over_limit(self):
        for line in self:
            limit = line.order_id._flowdesk_discount_limit() if line.order_id else None
            line.flowdesk_over_limit = limit is not None and not line.display_type and line.discount > limit

    @api.depends('product_id', 'product_uom_id', 'product_uom_qty')
    def _compute_discount(self):
        # pricelist / quantity changes recompute the discount without going through write()
        super()._compute_discount()
        self.order_id._flowdesk_sync_approval()

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        lines.order_id._flowdesk_sync_approval()
        return lines

    def write(self, vals):
        res = super().write(vals)
        if 'discount' in vals:
            self.order_id._flowdesk_sync_approval()
        return res
