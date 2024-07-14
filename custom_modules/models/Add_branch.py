from odoo import models, fields


class StockQuant(models.Model):
    _inherit = 'stock.location'

    branch_id = fields.Many2one('res.branch')


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    branch_id = fields.Many2one('res.branch')
