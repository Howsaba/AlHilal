from odoo import models, fields

class ResCompany(models.Model):
    _inherit = "res.company"

    has_overtime = fields.Boolean()
    basic_salary_rate = fields.Float()
    total_salary_rate = fields.Float()