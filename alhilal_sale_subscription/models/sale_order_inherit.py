from odoo import models, fields, api
from datetime import timedelta

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    end_date = fields.Date(compute='_compute_end_date', store=True,readonly=True)

    @api.depends('start_date', 'plan_id.billing_period_days')
    def _compute_end_date(self):
        for record in self:
            if record.start_date and record.plan_id and record.plan_id.billing_period_days:
                billing_period_days = record.plan_id.billing_period_days
                record.end_date = record.start_date + timedelta(days=billing_period_days-1)
            else:
                False

    def _create_invoices(self, grouped=False, final=False, date=None):
        # Call the original method to create invoices
        moves = super(SaleOrder, self)._create_invoices(grouped=grouped, final=final, date=date)

        # After creating the invoices, update the deferred_end_date in invoice lines
        for order in self:
            for invoice in moves:
                # Ensure that the sale order and invoice are related
                if invoice.invoice_origin == order.name:
                    # Loop through the invoice lines and update the deferred_end_date
                    for line in invoice.invoice_line_ids:
                        # Check if the deferred_end_date field exists
                        if hasattr(line, 'deferred_end_date'):
                            # Update deferred_end_date with the sale order's end_date
                            line.deferred_end_date = order.end_date
                            line.name = line.product_id.name

        return moves