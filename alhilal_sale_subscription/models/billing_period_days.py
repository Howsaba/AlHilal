from odoo import models,fields,api


class SaleSubscriptionPlan(models.Model):
    _inherit = 'sale.subscription.plan'

    billing_period_days = fields.Integer(string="Billing Period Days")
