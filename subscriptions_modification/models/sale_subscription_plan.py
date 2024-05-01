from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleSubscriptionPlan(models.Model):
    _inherit = "sale.subscription.plan"

    membership_in_arabic = fields.Char()
    branch_id = fields.Many2one('res.branch')
