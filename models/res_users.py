from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    # C11: sales managers have no limit, see sale_order._flowdesk_discount_limit
    flowdesk_max_discount = fields.Float(
        string="Max Discount (%)", default=5.0,
        help="Highest line discount this salesperson may give without manager approval.")
