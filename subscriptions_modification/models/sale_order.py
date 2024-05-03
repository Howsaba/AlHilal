from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    age_group_id = fields.Many2one('age.group')
    res_team_id = fields.Many2one('res.team')
    session_id = fields.Many2one('session.session')
    payment_method_id = fields.Many2one('account.journal')
    payment_status = fields.Selection([('paid', 'Paid'), ('Pending', 'Pending')])
    add_clothes = fields.Boolean()
    branch_id = fields.Many2one('res.branch')

    def add_clothes_to_lines(self, discount):
        if self.add_clothes:
            product_ids = self.env['product.product'].search([('is_clothes', '=', True)])
            for product in product_ids:
                self.env['sale.order.line'].create({
                    'product_id': product.id,
                    'price_unit': product.list_price,
                    'discount': discount,
                    'product_uom_qty': 1,
                    'order_id': self.id,
                })