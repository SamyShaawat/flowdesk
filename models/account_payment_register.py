from odoo import models


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    def action_create_payments(self):
        # C8: covers list-view Pay and any other path that opens the wizard
        self.line_ids.move_id._flowdesk_check_3way_match()
        return super().action_create_payments()
