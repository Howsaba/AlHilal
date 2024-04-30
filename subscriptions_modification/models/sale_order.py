from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    age_group_id = fields.Many2one('age.group')
    res_team_id = fields.Many2one('res.team')
    session_id = fields.Many2one('session.session')
    payment_method_id = fields.Many2one('account.journal')
    payment_status = fields.Selection([('Cash', 'Paid'), ('Pending', 'Pending')])
