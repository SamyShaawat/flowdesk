from odoo import _, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

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
