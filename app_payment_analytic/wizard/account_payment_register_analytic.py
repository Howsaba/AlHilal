# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountPaymentRegister(models.TransientModel):
    _name = 'account.payment.register'
    _inherit = ['account.payment.register','analytic.mixin']

    def _create_payment_vals_from_wizard(self, batch_result):
        # OVERRIDE
        result = super(AccountPaymentRegister, self)._create_payment_vals_from_wizard(batch_result=batch_result)
        if self.analytic_distribution:
            result.update({
                "analytic_distribution": self.analytic_distribution
            })
        return result

    def _create_payment_vals_from_batch(self, batch_result):
        result = super(AccountPaymentRegister, self)._create_payment_vals_from_batch(batch_result=batch_result)
        if self.analytic_distribution:
            result.update({
                "analytic_distribution": self.analytic_distribution
            })
        return result

