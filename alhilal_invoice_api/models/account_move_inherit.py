from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = "account.move"

    membership_plan_id = fields.Many2one(
        "sale.subscription.plan", string="Membership Plan"
    )
    subscription_type = fields.Selection(
        [
            ("new", "New"),
            ("renewal", "Renewal"),
        ],
        string="Subscription Type",
    )

    @api.onchange("branch_id")
    def _onchange_branch_id_set_analytic_distribution(self):
        for move in self:
            if move.branch_id and move.line_ids:
                analytic = move.branch_id.analytic_distribution_ids
                if analytic:
                    for line in move.line_ids:
                        line.analytic_distribution = analytic[0].distribution
