from odoo import api, fields, models, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta


class ApprovalRequest(models.Model):
    _inherit = 'approval.request'

    salary_attachment_id = fields.Many2one('hr.salary.attachment')
    payment_id = fields.Many2one('account.payment')
    journal_id = fields.Many2one('account.journal', domain="[('type', 'in', ['cash', 'bank'])]")
    loan_flag = fields.Boolean()
    department_id = fields.Many2one('hr.department', readonly=True)
    position_id = fields.Many2one('hr.job', readonly=True)
    id_no = fields.Char()
    joining_date = fields.Date()
    last_emp_date = fields.Date('Last date for employee')
    reason = fields.Selection([('1', 'انتهاء العقد بالاتفاق بين الطرفين على انهاء العقد'),
                               ('2', 'فسخ العقد من قبل صاحب العمل'),
                               ('3', 'فسخ العقد من قبل صاحب العمل لحالة في المادة 80'),
                               ('4', 'ترك العامل العمل نتيجة لقوة قاهرة'),
                               ('5', 'انهاء العامل عقد العمل خلال ال 6 اشهر من الزواج او 3 اشهر من الوضع'),
                               ('6', ' ترك العامل العمل لاحد الاسباب الواردة في المادة 81'),
                               ('7', 'فسخ العقد من قبل العامل لغير الحالات الواردة في المادة 81')], default="1")
    end_of_service_flag = fields.Boolean()

    @api.onchange('request_owner_id')
    def onchange_request_owner_id(self):
        self.department_id = self.request_owner_id.employee_id.department_id.id
        self.position_id = self.request_owner_id.employee_id.job_id.id

    @api.onchange('category_id')
    def onchange_category_id(self):
        if self.category_id.sequence_code == 'end_of_service':
            self.end_of_service_flag = True
        if self.category_id.sequence_code == 'loan_request':
            self.loan_flag = True


    # @api.depends('category_id', 'request_status')
    # def compute_loan_flag(self):
    #     for rec in self:
    #         if rec.category_id.sequence_code == 'loan_request' and rec.request_status == 'approved':
    #             rec.loan_flag = True
    #         else:
    #             rec.loan_flag = False

    def action_confirm(self):
        if self.amount == 0 or self.quantity == 0:
            raise UserError(_('Amount or Quantity must be more than Zero!!'))
        return super().action_confirm()
    
    def action_approve(self):
        res = super().action_approve()
        if self.request_status == 'approved':
            if self.category_id.sequence_code == "loan_request":
                monthly_amount = self.amount / self.quantity
                deduction_type_id = self.env['hr.salary.attachment.type'].search([('code', '=', 'ATTACH_SALARY')])
                start_date = self.date + relativedelta(months=1)
                if not deduction_type_id:
                    raise UserError(_("You don't have salary attachment with this code (ATTACH_SALARY)"))
                salary_attachment_id = self.env['hr.salary.attachment'].create({
                    'employee_ids': [(4, self.request_owner_id.employee_id.id)],
                    'description': f'loan for {self.request_owner_id.employee_id.name}',
                    'deduction_type_id': deduction_type_id[0].id,
                    'date_start': start_date.strftime('%Y-%m-01'),
                    'monthly_amount': monthly_amount,
                    'total_amount': self.amount,
                })
                self.salary_attachment_id = salary_attachment_id.id
                self.send_message()
        return res

    def create_payment(self):
        if not self.payment_id:
            payment_vals = {
                'partner_id': self.request_owner_id.partner_id.id,
                'payment_type': 'outbound',
                'amount': self.amount,
                'journal_id': self.journal_id.id,
                # Add other required fields
            }
            payment = self.env['account.payment'].create(payment_vals)
            self.payment_id = payment.id
        else:
            raise UserError(_('Payment is already created'))

    def send_message(self):
        users = self.env.ref('account.group_account_manager').users
        for user in users:
            activity = self.env['mail.activity'].create({
                'activity_type_id': 4,  # ID of the activity type (e.g., call, meeting)
                'summary': 'Make Register Payment',
                'date_deadline': self.salary_attachment_id.date_start,  # Deadline for the activity
                'user_id': user.id,  # ID of the user responsible for the activity
                'res_id': self.id,  # ID of the record to which the activity is linked
                'res_model_id': self.env['ir.model']._get_id(self._name),
                # ID of the model to which the activity is linked
            })
            activity.action_close_dialog()

    def action_view_salary_attachment(self):
        action = self.env['ir.actions.act_window']._for_xml_id('hr_payroll.hr_salary_attachment_action')
        action['domain'] = [('id', '=', self.salary_attachment_id.id)]
        action['context'] = {
            'create': 0
        }
        return action

    def action_view_payment(self):
        action = self.env['ir.actions.act_window']._for_xml_id('account.action_account_payments_payable')
        action['domain'] = [('id', '=', self.payment_id.id)]
        action['context'] = {
            'create': 0
        }
        return action
