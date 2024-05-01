from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_arabic_name = fields.Char()
    branch_id = fields.Many2one('res.branch')
