from odoo import api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('sale_order_template_id')
    def _compute_payment_term_id(self):
        # C2: template payment terms win over the partner's
        super()._compute_payment_term_id()
        for order in self.filtered('sale_order_template_id.payment_term_id'):
            order.payment_term_id = order.sale_order_template_id.payment_term_id
