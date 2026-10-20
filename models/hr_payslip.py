from odoo import Command, models


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def _compute_input_line_ids(self):
        # C6: one Sales Commission input per payslip = sum of the commission of the employee's
        # customer invoices that were paid inside the payslip period.
        super()._compute_input_line_ids()
        input_type = self.env.ref('flowdesk.input_sales_commission', raise_if_not_found=False)
        if not input_type:
            return
        for slip in self:
            commands = [Command.unlink(line.id) for line in slip.input_line_ids if line.input_type_id == input_type]
            user = slip.employee_id.user_id
            if user and slip.date_from and slip.date_to:
                # sudo: the payroll officer generating the slip may not have accounting rights
                invoices = self.env['account.move'].sudo().search([
                    ('move_type', '=', 'out_invoice'),
                    ('invoice_user_id', '=', user.id),
                    ('company_id', '=', slip.company_id.id),
                    ('flowdesk_paid_date', '>=', slip.date_from),
                    ('flowdesk_paid_date', '<=', slip.date_to),
                ])
                amount = sum(invoices.mapped('flowdesk_commission_amount'))
                if amount:
                    commands.append(Command.create({
                        'name': slip.env._("Sales commission (%s paid invoices)", len(invoices)),
                        'input_type_id': input_type.id,
                        'amount': amount,
                    }))
            if commands:
                slip.input_line_ids = commands
