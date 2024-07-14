from odoo import models,fields

class AccountJournal(models.Model):
    _inherit="account.journal"

    loan_account_id=fields.Many2one('account.account')
