# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountPayment(models.Model):
    _name = "account.payment"
    _inherit = ["account.payment", "analytic.mixin"]

    def _prepare_move_line_default_vals(self, write_off_line_vals=None, force_balance=None):
        result = super(AccountPayment, self)._prepare_move_line_default_vals(write_off_line_vals=write_off_line_vals, force_balance=force_balance)
        for move_line in result:
            if self.analytic_distribution:
                move_line.update({
                    "analytic_distribution": self.analytic_distribution
                })
        return result

    @api.model
    def _get_trigger_fields_to_synchronize(self):
        fields = super(AccountPayment, self)._get_trigger_fields_to_synchronize()
        fields += (('analytic_distribution',))
        return fields

    def action_post(self):
        result = super(AccountPayment, self).action_post()
        for payments in self:
            for invoice_line in payments.move_id.invoice_line_ids:
                if payments.analytic_distribution:
                    invoice_line.update({
                        "analytic_distribution": payments.analytic_distribution
                    })
        return result


