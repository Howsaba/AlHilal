from odoo import models, fields


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
        return res
