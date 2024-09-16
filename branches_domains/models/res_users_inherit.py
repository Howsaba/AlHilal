from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResUsersInherit(models.Model):
    _inherit = 'res.users'

    branch_id = fields.Many2one('res.branch', string='Default Branch')
    branch_ids = fields.Many2many('res.branch', string='Other Branches')






    @api.constrains('branch_id', 'branch_ids')
    def _check_branch_in_branch_ids(self):

        for user in self:
            if user.branch_id and user.branch_id not in user.branch_ids:
                raise ValidationError("The default branch must be one of the selected branches in 'Other Branches'.")
