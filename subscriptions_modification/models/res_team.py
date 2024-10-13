from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ResTeam(models.Model):
    _name = "res.team"

    name = fields.Char(required=True)
    arabic_name = fields.Char(required=True)
    branch_id = fields.Many2one('res.branch',required=True)
    session_id = fields.Many2one('session.session', required=True)
    coach_id = fields.Many2one('res.coach')
    team_capacity = fields.Integer(required=True)
    note = fields.Html()
