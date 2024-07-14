from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    payment_method_id = fields.Many2one('account.journal')
    payment_status = fields.Selection([('paid', 'Paid'), ('Pending', 'Pending')])
    branch_id = fields.Many2one('res.branch')
