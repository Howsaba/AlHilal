from odoo import models,fields,api


class AccountMove(models.Model):
    _inherit = 'account.move'

    # end_date = fields.Date(related="invoice_line_ids.")

