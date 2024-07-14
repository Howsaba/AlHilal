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

    def action_confirm(self):
        res = super().action_confirm()
        if self.picking_ids:
            for pick in self.picking_ids:
                pick.branch_id = self.branch_id.id
        return res

    def put_branch_in_invoice(self):
        if self.invoice_ids:
            for move in self.invoice_ids:
                move.branch_id = self.branch_id.id
                move.payment_method_id = self.payment_method_id.id
                move.payment_status = self.payment_status


class SaleAdvancePayment(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    def create_invoices(self):
        res = super().create_invoices()
        for order in self.sale_order_ids:
            order.put_branch_in_invoice()
        return res