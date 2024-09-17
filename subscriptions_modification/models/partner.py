from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = "res.partner"

    arabic_name = fields.Char(required=True)
    id_type = fields.Selection([('national_iqama', 'National/Iqama ID'),
                                ('passport', 'Passport')],
                               default="national_iqama")
    national_id = fields.Char()
    passport_number = fields.Char('passport No')
    unique_id = fields.Char()
    birthday = fields.Date(required=True)
    nationality_id = fields.Many2one('res.country', required=True)
    branch_id = fields.Many2one('res.branch')
