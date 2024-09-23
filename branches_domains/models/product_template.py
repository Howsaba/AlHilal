from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    branch_id = fields.Many2one('res.branch', string='Branch',
                                domain=lambda self: [('id', 'in', self.env.user.branch_ids.ids)],
                                default=lambda self: self.env.user.branch_id.id)



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




class ProductProduct(models.Model):
    _inherit = "product.product"

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
