from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    invoice_sale_date = fields.Date(string='Invoice Date')

    def _create_invoices(self, grouped=False, final=False, date=None):
        invoices = super(SaleOrder, self)._create_invoices(grouped, final, date)

        for invoice in invoices:
            if self.invoice_sale_date:
                invoice.invoice_date = self.invoice_sale_date


        return invoices
