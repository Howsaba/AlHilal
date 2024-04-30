from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ResBranch(models.Model):
    _name = "res.branch"

    name = fields.Char(required=True)
    company_id = fields.Many2one('res.company', required=True)