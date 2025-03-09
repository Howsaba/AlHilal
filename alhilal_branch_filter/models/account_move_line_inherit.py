from odoo import models, fields,api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    analytic_distribution_display = fields.Char(
        string='Analytic Distribution (Display)',
        compute='_compute_analytic_distribution_display',
        store=True
    )


    @api.depends('analytic_distribution')
    def _compute_analytic_distribution_display(self):
        for record in self:
            if record.analytic_distribution:
                display_values = []
                _logger.info(f"Analytic Distribution Data: {record.analytic_distribution}")  # Debug log

                for account_id, amount in record.analytic_distribution.items():
                    try:
                        # Ensure account_id is clean and converted to an integer
                        account_id_str = str(account_id).replace(",", "").strip()
                        account_id_int = int(account_id_str)

                        analytic_account = self.env['account.analytic.account'].browse(account_id_int)

                        if analytic_account.exists():
                            display_values.append(f"{analytic_account.name}: {amount}")
                        else:
                            _logger.warning(f"Analytic Account ID {account_id_int} does not exist.")

                    except ValueError:
                        _logger.error(f"Invalid analytic account ID format: {account_id}")

                record.analytic_distribution_display = ', '.join(display_values) if display_values else 'No Distribution'
            else:
                record.analytic_distribution_display = 'No Distribution'