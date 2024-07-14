from odoo import models, fields


class Branch(models.Model):
    _inherit = 'res.branch'

    location_ids = fields.Many2many('stock.location', required=True)
    analytic_account_ids = fields.Many2many('account.analytic.account', required=True)
