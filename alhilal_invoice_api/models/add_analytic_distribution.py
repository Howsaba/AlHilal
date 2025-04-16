from odoo import fields, models


class AnalyticDistribution(models.Model):
    _inherit = "res.branch"

    # sales_analytic_distributions = fields.One2many(
    #     "account.analytic.account",
    #     "branch_id",
    #     string="Sales Analytic Distributions",
    #     required=True,
    # )
    sales_analytic_distributions = fields.Many2one(
        "account.analytic.account",
        string="Sales Analytic Distributions",
        required=True,
    )


# class AccountAnalyticDistribution(models.Model):
#     _inherit = "account.analytic.account"

#     branch_id = fields.Many2one("res.branch", string="Branch")
