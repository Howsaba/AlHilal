from odoo import models, fields

class Employee2(models.Model):
    _inherit = "hr.employee"

    branch_ids = fields.Many2many('res.branch', domain="[('company_id', '=', company_id)]")
    passport_or_id_issue_date = fields.Date(string='Passport or ID Issue Date')
    passport_or_id_expiry_date = fields.Date(string='Passport or ID Expiry Date')
    contact_address = fields.Text(string='Contact Address')
    relative_type = fields.Text(string='Relative Type')
    english_name = fields.Char(string='English Employee Name', required=True)
    employee_number = fields.Float(string='Employee Number', required=True)
    date_of_birth = fields.Date(string='Date of Birth')
    religion = fields.Selection(
         [('muslim', 'Muslim'),
          ('christian', 'Christian'),
          ('other', 'Other')],
         string='Religion')
    other_religion = fields.Char(string='Other Religion')