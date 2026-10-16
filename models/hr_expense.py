from odoo import models


class HrExpense(models.Model):
    _inherit = 'hr.expense'

    def _do_approve(self, check=True):
        # C5: approval books the journal entry right away; accounting only has to pay it.
        # ponytail: employee-paid only; company-paid keep the native Post button.
        super()._do_approve(check=check)
        to_post = self.filtered(lambda e: e.state == 'approved' and e.payment_mode == 'own_account')
        if to_post:
            to_post._post_without_wizard()
