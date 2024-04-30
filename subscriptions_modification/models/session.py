from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SessionSession(models.Model):
    _name = "session.session"

    name = fields.Char(required=True)
