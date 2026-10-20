from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    # C10: trace one deal from the opportunity to the delivery, invoice, payment and commission
    flowdesk_picking_ids = fields.Many2many(
        'stock.picking', string="Deliveries", compute='_compute_flowdesk_trace')
    flowdesk_invoice_ids = fields.Many2many(
        'account.move', string="Invoices", compute='_compute_flowdesk_trace')
    flowdesk_payment_ids = fields.Many2many(
        'account.payment', string="Payments", compute='_compute_flowdesk_trace')
    flowdesk_commission_amount = fields.Monetary(
        string="Commission", compute='_compute_flowdesk_trace', currency_field='company_currency')

    @api.depends('order_ids.picking_ids', 'order_ids.invoice_ids.state',
                 'order_ids.invoice_ids.payment_state', 'order_ids.invoice_ids.flowdesk_paid_date', 'order_ids.invoice_ids.matched_payment_ids')
    def _compute_flowdesk_trace(self):
        for lead in self:
            # sudo: salespeople may not read invoices/payments, but must see the trail of their own deal
            orders = lead.order_ids.sudo().filtered(lambda o: o.state == 'sale')
            invoices = orders.invoice_ids.filtered(lambda m: m.move_type == 'out_invoice' and m.state == 'posted')
            lead.flowdesk_picking_ids = orders.picking_ids
            lead.flowdesk_invoice_ids = invoices
            lead.flowdesk_payment_ids = invoices.matched_payment_ids
            lead.flowdesk_commission_amount = sum(invoices.mapped('flowdesk_commission_amount'))

    def _flowdesk_open(self, model, records, name):
        action = {'type': 'ir.actions.act_window', 'name': name, 'res_model': model,
                  'domain': [('id', 'in', records.ids)], 'view_mode': 'list,form'}
        if len(records) == 1:
            action.update(view_mode='form', res_id=records.id)
        return action

    def action_open_flowdesk_pickings(self):
        return self._flowdesk_open('stock.picking', self.flowdesk_picking_ids, self.env._("Deliveries"))

    def action_open_flowdesk_invoices(self):
        return self._flowdesk_open('account.move', self.flowdesk_invoice_ids, self.env._("Invoices"))

    def action_open_flowdesk_payments(self):
        return self._flowdesk_open('account.payment', self.flowdesk_payment_ids, self.env._("Payments"))
