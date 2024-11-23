from odoo import models, api
from odoo.exceptions import UserError


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    def action_confirm_to_draft(self):
        for payment in self:
            if payment.state == 'posted':
                payment.state = 'draft'



    def cancel_records(self):
        for record in self:
            if record.state == 'draft':
                record.action_cancel()
            else:
                raise UserError("The record must be in the 'Draft' state to be canceled.")
