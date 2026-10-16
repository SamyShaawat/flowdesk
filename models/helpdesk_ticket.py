from odoo import _, api, fields, models
from odoo.exceptions import UserError


class HelpdeskStage(models.Model):
    _inherit = 'helpdesk.stage'

    flowdesk_requires_payment = fields.Boolean(
        string="Requires Payment",
        help="Tickets linked to a sale order cannot enter this stage until its invoice is paid.")


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    # C7: the sale order link comes from helpdesk_sale (sale_order_id); this adds invoice + payment status.
    flowdesk_invoice_ids = fields.Many2many(
        'account.move', string="Customer Invoices", compute='_compute_flowdesk_payment_state')
    flowdesk_payment_state = fields.Selection(
        [('not_invoiced', "Not Invoiced"), ('unpaid', "Unpaid"), ('paid', "Paid")],
        string="Payment", compute='_compute_flowdesk_payment_state', store=True)

    @api.depends('sale_order_id.invoice_ids.state', 'sale_order_id.invoice_ids.payment_state')
    def _compute_flowdesk_payment_state(self):
        for ticket in self:
            # sudo: support agents may not have accounting rights
            invoices = ticket.sale_order_id.sudo().invoice_ids.filtered(
                lambda m: m.move_type == 'out_invoice' and m.state == 'posted')
            ticket.flowdesk_invoice_ids = invoices
            if not ticket.sale_order_id:
                ticket.flowdesk_payment_state = False
            elif not invoices:
                ticket.flowdesk_payment_state = 'not_invoiced'
            elif all(m.payment_state in ('paid', 'in_payment') for m in invoices):
                # in_payment = payment registered, bank statement not matched yet
                ticket.flowdesk_payment_state = 'paid'
            else:
                ticket.flowdesk_payment_state = 'unpaid'

    def write(self, vals):
        if vals.get('stage_id') and self.env['helpdesk.stage'].browse(vals['stage_id']).flowdesk_requires_payment:
            # ponytail: tickets without a sale order are free support and are not gated
            unpaid = self.filtered(lambda t: t.flowdesk_payment_state in ('not_invoiced', 'unpaid'))
            if unpaid:
                raise UserError(_(
                    "Cannot move %(tickets)s to this stage: the invoice of the linked sales order "
                    "is not paid yet. Register the payment first.",
                    tickets=", ".join(unpaid.mapped('display_name'))))
        return super().write(vals)

    def action_open_flowdesk_invoices(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _("Invoices"),
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.flowdesk_invoice_ids.ids)],
        }
