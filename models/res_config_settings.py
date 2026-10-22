from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    flowdesk_followup_days = fields.Integer(
        string="Follow-up After (days)", config_parameter='flowdesk.followup_days', default=3)
    flowdesk_escalation_days = fields.Integer(
        string="Escalate After (days)", config_parameter='flowdesk.escalation_days', default=7)
