from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    invoice_sale_date = fields.Date(string='Invoice Date')

    def _create_invoices(self, grouped=False, final=False, date=None):
        invoices = super(SaleOrder, self)._create_invoices(grouped, final, date)

        for order in self:
            related_invoices = invoices.filtered(lambda inv: inv.invoice_origin == order.name)

            if order.invoice_sale_date:
                for invoice in related_invoices:
                    invoice.invoice_date = order.invoice_sale_date

        return invoices
