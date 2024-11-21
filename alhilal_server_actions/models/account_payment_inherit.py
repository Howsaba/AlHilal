from odoo import models, api
from odoo.exceptions import UserError


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    def action_confirm_to_draft(self):
        for payment in self:
            if payment.state == 'posted':
                payment.state = 'draft'


