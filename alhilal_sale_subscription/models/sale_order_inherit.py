from odoo import models, fields, api
from datetime import timedelta


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    end_date = fields.Date(compute='_compute_end_date', store=True, readonly=True)

    @api.depends('start_date', 'plan_id.billing_period_days')
    def _compute_end_date(self):
        for record in self:
            if record.start_date and record.plan_id and record.plan_id.billing_period_days:
                billing_period_days = record.plan_id.billing_period_days
                record.end_date = record.start_date + timedelta(days=billing_period_days - 1)
            else:
                record.end_date = False  # Correctly assign False to end_date

    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        res._compute_end_date()
        return res

    def _create_invoices(self, grouped=False, final=False, date=None):
        moves = super(SaleOrder, self)._create_invoices(grouped=grouped, final=final, date=date)

        for order in self:
            order._compute_end_date()

            for invoice in moves:
                if invoice.invoice_origin == order.name:
                    for line in invoice.invoice_line_ids:
                            line.deferred_end_date = order.end_date
                            line.name = line.product_id.name

        return moves
