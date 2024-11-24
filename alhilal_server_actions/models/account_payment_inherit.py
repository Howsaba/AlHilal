from odoo import models, api,exceptions, _
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




    def remove_move_reconcile(self):
        """
        Remove reconciliation for all invoices linked to the selected payments
        only if the payment is in the 'draft' state.
        """
        for payment in self:
            # Check if the state is not draft
            if payment.state != 'cancel':
                raise exceptions.UserError(
                    _("Reconciliation can only be removed for payments in the 'cancel' state.")
                )

            # Proceed with removing reconciliation if the state is 'draft'
            for move_line in payment.reconciled_invoice_ids.mapped('line_ids'):
                if move_line.reconciled:
                    move_line.remove_move_reconcile()
