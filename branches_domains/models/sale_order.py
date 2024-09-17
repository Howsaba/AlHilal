from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    branch_id = fields.Many2one('res.branch', string='Branch',
                                domain=lambda self: [('id', 'in', self._get_user_branch_ids())],
                                default=lambda self: self.env.user.branch_id.id)

    def _get_user_branch_ids(self):
        return self.env.user.branch_ids.ids

    @api.onchange('branch_ids')
    def _onchange_branch_ids(self):

        for record in self:
            if record.branch_ids:
                return {
                    'domain': {'branch_id': [('id', 'in', record.branch_ids.ids)]}
                }
            else:
                return {
                    'domain': {
                        'branch_id': []}}