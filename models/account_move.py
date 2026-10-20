from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    # C6: an invoice earns commission once it is fully paid; the payment date decides the payslip period
    flowdesk_paid_date = fields.Date(
        string="Paid On", compute='_compute_flowdesk_paid_date', store=True, copy=False)
    flowdesk_commission_amount = fields.Monetary(
        string="Commission", compute='_compute_flowdesk_commission_amount', currency_field='company_currency_id')

    @api.depends('payment_state', 'matched_payment_ids.date')
    def _compute_flowdesk_paid_date(self):
        for move in self:
            if move.move_type != 'out_invoice' or move.payment_state not in ('paid', 'in_payment'):
                move.flowdesk_paid_date = False
            else:
                # sudo: salespeople may not read payments
                dates = move.sudo().matched_payment_ids.mapped('date')
                move.flowdesk_paid_date = max(dates) if dates else (move.invoice_date or fields.Date.context_today(move))

    @api.depends('flowdesk_paid_date', 'amount_untaxed_signed', 'invoice_user_id')
    def _compute_flowdesk_commission_amount(self):
        for move in self:
            rate = move.invoice_user_id.sudo().employee_id.flowdesk_commission_rate
            move.flowdesk_commission_amount = move.amount_untaxed_signed * rate / 100 if move.flowdesk_paid_date else 0.0

    def _flowdesk_check_3way_match(self):
        # C8: 3-way match gate. Bills on a PO can only be paid when release_to_pay is 'yes';
        # to override, someone sets "Should Be Paid" to Yes (Other Info tab) after dealing with it.
        blocked = self.filtered(
            lambda m: m.move_type == 'in_invoice'
            and m.invoice_line_ids.purchase_line_id
            and m.release_to_pay != 'yes')
        if blocked:
            raise UserError(_(
                "Cannot pay %(bills)s: ordered, received and billed quantities do not match "
                "(Should Be Paid = %(status)s). Fix the bill or the receipt, or set Should Be Paid to Yes.",
                bills=", ".join(blocked.mapped('name')),
                status=", ".join(set(blocked.mapped('release_to_pay')))))

    def action_force_register_payment(self):
        # early feedback; the payment wizard enforces the same check for every other entry point
        self._flowdesk_check_3way_match()
        return super().action_force_register_payment()
