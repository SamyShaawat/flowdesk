from odoo import _, fields, models
from odoo.exceptions import AccessError, UserError


class FlowdeskDiscountApproval(models.Model):
    _name = 'flowdesk.discount.approval'
    _description = "Discount Approval"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    order_id = fields.Many2one('sale.order', required=True, ondelete='cascade', index=True)
    name = fields.Char(related='order_id.name', string="Quotation", store=True)
    salesperson_id = fields.Many2one('res.users', required=True, string="Salesperson")
    limit = fields.Float(string="Salesperson Limit (%)")
    max_discount = fields.Float(string="Highest Discount (%)")
    # {sale.order.line id: discount} of every line over the limit when the request was made
    snapshot = fields.Json()
    line_detail = fields.Text(string="Lines Over the Limit")
    state = fields.Selection(
        [('waiting', "Waiting for Approval"), ('approved', "Approved"),
         ('rejected', "Rejected"), ('cancelled', "Cancelled")],
        default='waiting', required=True, tracking=True)
    approver_id = fields.Many2one('res.users', string="Decided By", readonly=True)
    decision_date = fields.Datetime(string="Decided On", readonly=True)
    comment = fields.Text(string="Manager Comment")

    _PROTECTED_FIELDS = {'state', 'approver_id', 'decision_date'}

    def write(self, vals):
        # decisions only through Approve / Reject (comment check + log); the system (sudo) syncs requests
        if self._PROTECTED_FIELDS & vals.keys() and not self.env.su:
            raise AccessError(_("Use the Approve or Reject button to decide on a discount."))
        return super().write(vals)

    def _notify_managers(self):
        managers = self.env.ref('sales_team.group_sale_manager').sudo().user_ids
        for approval in self:
            for manager in managers:
                approval.activity_schedule(
                    'mail.mail_activity_data_todo', user_id=manager.id,
                    summary=_("Discount approval: %s", approval.name),
                    note=_("%(user)s asks to approve a discount of up to %(disc)s%% (limit %(limit)s%%) on %(order)s.",
                           user=approval.salesperson_id.name, disc=approval.max_discount,
                           limit=approval.limit, order=approval.name))

    def _cancel(self):
        self.write({'state': 'cancelled'})
        self.activity_unlink(['mail.mail_activity_data_todo'])

    def _decide(self, state):
        if not self.env.user.has_group('sales_team.group_sale_manager'):
            raise AccessError(_("Only sales managers can approve or reject discounts."))
        for approval in self:
            if approval.state != 'waiting':
                raise UserError(_("%s was already decided or cancelled.", approval.name))
            if state == 'rejected' and not approval.comment:
                raise UserError(_("Write a comment explaining the rejection."))
            approval.sudo().write({'state': state, 'approver_id': self.env.user.id,
                            'decision_date': fields.Datetime.now()})
            approval.activity_unlink(['mail.mail_activity_data_todo'])
            label = _("approved") if state == 'approved' else _("rejected")
            approval.order_id.message_post(body=_(
                "Discount %(label)s by %(user)s: %(detail)s%(comment)s",
                label=label, user=self.env.user.name, detail=approval.line_detail,
                comment=("\n" + approval.comment) if approval.comment else ""))
            if state == 'rejected':
                approval.order_id.sudo().activity_schedule(
                    'mail.mail_activity_data_todo', user_id=approval.salesperson_id.id,
                    summary=_("Discount rejected: %s", approval.name), note=approval.comment)

    def action_approve(self):
        self._decide('approved')

    def action_reject(self):
        self._decide('rejected')
