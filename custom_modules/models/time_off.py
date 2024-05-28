from odoo import models, fields


class TimeOff(models.Model):
    _inherit = "hr.leave"

    ticket = fields.Char()
    visa = fields.Char()
