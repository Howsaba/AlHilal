from odoo import models, fields

class Employee2(models.Model):
    _inherit = "hr.employee"

    branch_ids = fields.Many2many('res.branch', domain="[('company_id', '=', company_id)]")
    passport_or_id_issue_date = fields.Date(string='Passport or ID Issue Date')
    passport_or_id_issue_ids = fields.Many2many('res.country')
    passport_or_id_expiry_date = fields.Date(string='Passport or ID Expiry Date')
    contact_address = fields.Text(string='Contact Address')
    relative_type = fields.Text(string='Relative Type')
    english_name = fields.Char(string='English Employee Name', required=True)
    employee_number = fields.Integer(string='Employee Number', required=True)
    religion = fields.Selection(
         [('muslim', 'Muslim'),
          ('christian', 'Christian'),
          ('other', 'Other')],
         string='Religion')
    other_religion = fields.Char(string='Other Religion')


    insurance_no = fields.Char()
    policy_number = fields.Char()
    category = fields.Char()
    activation_code = fields.Date()
    cost = fields.Float()
    insurance_council = fields.Char('Availability at the Health Insurance Council')
    insurance_council_date = fields.Date('Health Insurance Council start date')

    payment_method_selection = fields.Selection(
        [('cash', 'Cash'),
         ('bank', 'Bank'),
         ('transfer', 'Transfer'),
         ('cheque', 'Cheque')],
        default='cash')
    bank_name = fields.Char()
    iban = fields.Char('IBAN')
    account_owner_name = fields.Char()
    account_owner_arabic_name = fields.Char()
    branch_name = fields.Char()
    branch_arabic_name = fields.Char()
    swift_code = fields.Char()
    sort_code = fields.Char()
    account_no = fields.Char()
    country = fields.Many2one('res.country')
    bank_location = fields.Many2one('res.country')
    bank_type = fields.Selection(
        [('account', 'Bank Account'),
         ('card', 'Employee Card')],
        default='account')
    contract_id = fields.Many2one(
        'hr.contract', string='Current Contract', groups="base.group_user",
        domain="[('company_id', '=', company_id), ('employee_id', '=', id)]", help='Current contract of the employee',
        copy=False)


    def get_overtime_from_work_entry(self, from_date, to_date):
        work_entry_ids = self.env['hr.work.entry'].search([('employee_id', '=', self.id),
                                                           ('date_start', '>=', from_date),
                                                           ('date_stop', '<=', to_date)])
        filtered_work_entry_ids = work_entry_ids.filtered(lambda x: x.work_entry_type_id.code == 'OVERTIME').mapped('duration')
        return sum(filtered_work_entry_ids)