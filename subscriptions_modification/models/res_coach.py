from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ResCoach(models.Model):
    _name = "res.coach"

    name = fields.Char(required=True)
    mobile = fields.Char(required=True)
    team_id = fields.Many2one('res.team', required=True)
    branch_id = fields.Many2one('res.branch', required=True)
