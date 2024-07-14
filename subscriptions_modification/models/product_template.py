from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_arabic_name = fields.Char()
    branch_id = fields.Many2one('res.branch')
    is_clothes = fields.Boolean()


class ProductProduct(models.Model):
    _inherit = "product.product"

    product_arabic_name = fields.Char(related="product_tmpl_id.product_arabic_name")
    branch_id = fields.Many2one('res.branch', related="product_tmpl_id.branch_id")
    is_clothes = fields.Boolean(related="product_tmpl_id.is_clothes")
