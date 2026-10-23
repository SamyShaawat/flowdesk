from odoo import _, fields, models
from odoo.exceptions import UserError


class FlowdeskCancelReason(models.Model):
    _name = 'flowdesk.cancel.reason'
    _description = "Quotation Cancel Reason"
    _order = 'sequence, id'

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)


class FlowdeskCancelWizard(models.TransientModel):
    _name = 'flowdesk.cancel.wizard'
    _description = "Cancel Quotation Wizard"

    order_ids = fields.Many2many(
        'sale.order', default=lambda self: self.env.context.get('active_ids'))
    reason_id = fields.Many2one('flowdesk.cancel.reason', string="Reason", required=True)
    note = fields.Text(string="Note")
    has_confirmed_order = fields.Boolean(compute='_compute_has_confirmed_order')

    def _compute_has_confirmed_order(self):
        for wizard in self:
            wizard.has_confirmed_order = any(s == 'sale' for s in wizard.order_ids.mapped('state'))

    def action_cancel_orders(self):
        self.ensure_one()
        self.order_ids._flowdesk_cancel(self.reason_id, self.note)
        return {'type': 'ir.actions.act_window_close'}


class SaleMassCancelOrders(models.TransientModel):
    _inherit = 'sale.mass.cancel.orders'

    # mass cancel (list > Actions > Cancel) also asks for the reason
    flowdesk_reason_id = fields.Many2one('flowdesk.cancel.reason', string="Reason")
    flowdesk_note = fields.Text(string="Note")

    def action_mass_cancel(self):
        self.ensure_one()
        if not self.flowdesk_reason_id:
            raise UserError(_("Please pick a cancel reason."))
        self.sale_order_ids._flowdesk_cancel(self.flowdesk_reason_id, self.flowdesk_note)
        return {'type': 'ir.actions.act_window_close'}
