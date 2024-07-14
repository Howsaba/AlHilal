from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AgeGroup(models.Model):
    _name = "age.group"

    name = fields.Char(required=True)
    arabic_name = fields.Char(required=True)
    suggested_age_year_from = fields.Integer('Suggested Age Years', required=True)
    suggested_age_year_to = fields.Integer(required=True)
    branch_id = fields.Many2one('res.branch', required=True)
