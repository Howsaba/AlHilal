from odoo import models

class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_reset_to_draft(self):

        for record in self:
            if record.state != 'draft':
                record.button_draft()
