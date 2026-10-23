from datetime import timedelta

from odoo import _, api, fields, models

EXPIRING_DAYS = 30


class FlowdeskVendorDocument(models.Model):
    _name = 'flowdesk.vendor.document'
    _description = "Vendor Document"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'expiry_date, id'

    partner_id = fields.Many2one('res.partner', string="Vendor", required=True, ondelete='cascade', index=True)
    doc_type = fields.Selection(
        [('commercial_registration', "Commercial Registration"), ('tax_certificate', "Tax Certificate"),
         ('insurance', "Insurance"), ('other', "Other")],
        string="Document Type", required=True, default='tax_certificate')
    number = fields.Char(string="Number")
    expiry_date = fields.Date(required=True)
    attachment = fields.Binary(string="File", attachment=True)
    attachment_name = fields.Char(string="File Name")
    # not stored: "today" changes every day, so the status is computed on read and searched on the date
    state = fields.Selection(
        [('valid', "Valid"), ('expiring', "Expiring Soon"), ('expired', "Expired")],
        compute='_compute_state', search='_search_state')
    days_left = fields.Integer(compute='_compute_state')
    reminded = fields.Boolean(copy=False, help="The purchase team was already notified for this expiry date.")

    @api.depends('expiry_date')
    def _compute_state(self):
        today = fields.Date.context_today(self)
        for doc in self:
            doc.days_left = (doc.expiry_date - today).days if doc.expiry_date else 0
            if not doc.expiry_date or doc.days_left > EXPIRING_DAYS:
                doc.state = 'valid'
            elif doc.days_left < 0:
                doc.state = 'expired'
            else:
                doc.state = 'expiring'

    def _search_state(self, operator, value):
        if operator not in ('=', '!=', 'in', 'not in'):
            raise NotImplementedError(operator)
        states = {value} if isinstance(value, str) else set(value)
        if operator in ('!=', 'not in'):
            states = {'valid', 'expiring', 'expired'} - states
        today = fields.Date.context_today(self)
        soon = today + timedelta(days=EXPIRING_DAYS)
        parts = {
            'expired': [('expiry_date', '<', today)],
            'expiring': [('expiry_date', '>=', today), ('expiry_date', '<=', soon)],
            'valid': [('expiry_date', '>', soon)],
        }
        domain = [('id', '=', False)]
        for state in sorted(states):
            domain = ['|'] + domain + (['&'] + parts[state] if len(parts[state]) > 1 else parts[state])
        return domain

    @api.depends('doc_type', 'number')
    def _compute_display_name(self):
        types = dict(self._fields['doc_type'].selection)
        for doc in self:
            doc.display_name = " ".join(filter(None, [types.get(doc.doc_type), doc.number]))

    def write(self, vals):
        if 'expiry_date' in vals:
            vals = dict(vals, reminded=False)
        return super().write(vals)

    @api.model
    def _cron_remind_expiring(self):
        docs = self.search([('state', '=', 'expiring'), ('reminded', '=', False)])
        # all_group_ids: members through implied groups (managers) count as purchase team too
        team = self.env['res.users'].sudo().search([
            ('all_group_ids', 'in', self.env.ref('purchase.group_purchase_user').id),
            ('share', '=', False), ('id', '!=', self.env.ref('base.user_root').id)])
        for doc in docs:
            for user in team:
                doc.activity_schedule(
                    'mail.mail_activity_data_todo', user_id=user.id,
                    summary=_("%(doc)s of %(vendor)s expires in %(days)s days",
                              doc=doc.display_name, vendor=doc.partner_id.name, days=doc.days_left))
            doc.reminded = True


class ResPartner(models.Model):
    _inherit = 'res.partner'

    flowdesk_document_ids = fields.One2many('flowdesk.vendor.document', 'partner_id', string="Documents")
    flowdesk_expired_count = fields.Integer(compute='_compute_flowdesk_documents')
    flowdesk_expiring_count = fields.Integer(compute='_compute_flowdesk_documents')

    @api.depends('flowdesk_document_ids.expiry_date')
    def _compute_flowdesk_documents(self):
        for partner in self:
            states = partner.flowdesk_document_ids.mapped('state')
            partner.flowdesk_expired_count = states.count('expired')
            partner.flowdesk_expiring_count = states.count('expiring')


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    flowdesk_vendor_expired = fields.Integer(related='partner_id.commercial_partner_id.flowdesk_expired_count')

    @api.onchange('partner_id')
    def _onchange_partner_id_flowdesk_documents(self):
        # warning only: blocking the order is a business decision, see PR notes
        if self.partner_id.commercial_partner_id.flowdesk_expired_count:
            return {'warning': {
                'title': _("Expired vendor document"),
                'message': _("%s has an expired document. Check its Documents tab before ordering.",
                             self.partner_id.commercial_partner_id.name),
            }}
