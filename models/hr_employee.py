from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.model_create_multi
    def create(self, vals_list):
        employees = super().create(vals_list)
        # C4: every new hire gets the Onboarding Checklist plan, no manual launch.
        plan = self.env.ref('flowdesk.plan_onboarding_checklist', raise_if_not_found=False)
        # skip imports and install/demo data so they do not flood the assignee with activities
        if plan and not (self.env.context.get('install_mode') or self.env.context.get('import_file')):
            today = fields.Date.context_today(self)
            for employee in employees:
                for tpl in plan.template_ids:
                    employee.activity_schedule(
                        activity_type_id=tpl.activity_type_id.id,
                        automated=False,
                        summary=tpl.summary,
                        note=tpl.note,
                        user_id=tpl.responsible_id.id,
                        date_deadline=tpl._get_date_deadline(today))
        return employees
