from odoo import models, fields
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    payment_method_selection = fields.Selection(
        [('cash', 'Cash'),
         ('bank', 'Bank'),
         ('transfer', 'Transfer'),
         ('cheque', 'Cheque')])


class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    def action_payslip_done(self):
        res = super().action_payslip_done()
        for rec in self:
            rec.move_id.payment_method_selection = rec.employee_id.payment_method_selection
            line_id = rec.move_id.line_ids.filtered(lambda x:x.name == "Loan")
            raise UserError(f'/// {line_id} ///')
            partner_id = self.env['res.partner'].search([('employee_ids', 'in', rec.employee_id.id), ('name', '=', rec.employee_id.name)], limit=1)
            line_id[0].partner_id = partner_id[0].id
        return res
