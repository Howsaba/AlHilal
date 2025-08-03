# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round

# Added StockQuant Fields and Inventory Backdated Changes Functionality
class StockQuant(models.Model):
    _inherit = 'stock.quant'

    inventory_backdated = fields.Datetime(string='Inventory Backdated')
    notes = fields.Char(string='Notes')

    @api.constrains('inventory_backdated')
    def _check_inventory_backdated(self):
        for record in self:
            if record.inventory_backdated and record.inventory_backdated > fields.Datetime.now():
                raise ValidationError(_("The backdate cannot be set in the future. Please select a valid date and time."))

    def _apply_inventory(self):
        """Override the apply button functionality"""
        
        move_vals = []
        move_quant_mapping = {}

        if not self.user_has_groups('stock.group_stock_manager'):
            raise UserError(_('Only a stock manager can validate an inventory adjustment.'))
        for quant in self:
            # Use the inventory_backdated date if available
            inventory_backdated = quant.inventory_backdated or fields.Datetime.now()
            notes = quant.notes or ''
            # Create and validate a move so that the quant matches its `inventory_quantity`.
            if float_compare(quant.inventory_diff_quantity, 0, precision_rounding=quant.product_uom_id.rounding) > 0:
                move_val = quant._get_inventory_move_values(quant.inventory_diff_quantity,
                                                     quant.product_id.with_company(quant.company_id).property_stock_inventory,
                                                     quant.location_id, package_dest_id=quant.package_id)
            else:
                move_val = quant._get_inventory_move_values(-quant.inventory_diff_quantity,
                                                     quant.location_id,
                                                     quant.product_id.with_company(quant.company_id).property_stock_inventory,
                                                     package_id=quant.package_id)
            move_vals.append(move_val)
            move_quant_mapping[len(move_vals) - 1] = {'inventory_backdated': inventory_backdated, 'notes': notes}  # Map move index to inventory_backdated and notes

        moves = self.env['stock.move'].with_context(inventory_mode=False).create(move_vals)
        moves._action_done()
        # Update all relevant fields with their respective inventory_backdated
        for index, move in enumerate(moves):
            inventory_backdated = move_quant_mapping[index]['inventory_backdated']
            notes = move_quant_mapping[index]['notes']

            move.write({
                    'date': inventory_backdated,
                    'inventory_backdated': True if notes else False,
                    'notes': notes
                })
            
            for move_line in move.move_line_ids:
                move_line.write({
                        'date': inventory_backdated,
                        'inventory_backdated': True if notes else False,
                        'notes': notes
                    })

            # Handle real-time valuation
            if move.product_id.valuation == 'real_time' and move.account_move_ids:
                for journal_entry in move.account_move_ids:
                    # Clear the sequence number to allow regenerating it with the new date
                    journal_entry.write({
                        'date': inventory_backdated,
                        'name': False,  # Setting the name (sequence number) to False will trigger a recompute
                        'inventory_backdated': True if notes else False,
                        'notes': notes
                    })
                    journal_entry._compute_name()  # Regenerate the sequence number based on the new date

            # Update stock valuation layers
            for valuation_layer in move.stock_valuation_layer_ids:
                self.env.cr.execute(
                    "UPDATE stock_valuation_layer SET create_date = %s WHERE id = %s",
                    (inventory_backdated, valuation_layer.id)
                )
                valuation_layer.write({
                    'inventory_backdated': True if notes else False,
                    'notes': notes
                })

        self.location_id.write({'last_inventory_date': fields.Date.today()})
        date_by_location = {loc: loc._get_next_inventory_date() for loc in self.mapped('location_id')}
        for quant in self:
            quant.inventory_date = date_by_location[quant.location_id]
        self.write({'inventory_quantity': 0, 'user_id': False})
        self.write({'inventory_diff_quantity': 0})
        self.write({'inventory_backdated': False, 'notes': False})

    @api.model
    def _get_inventory_fields_write(self):
        """ Returns a list of fields user can edit when editing a quant in `inventory_mode`."""
        res = super()._get_inventory_fields_write()
        res += ['inventory_backdated', 'notes']
        return res

# Added StockMove Fields for Inventory Notes
class StockMove(models.Model):
    _inherit = 'stock.move'

    inventory_backdated = fields.Boolean(string='Inventory Backdated')
    notes = fields.Char(string='Backdated Notes')

# Added StockMoveLine Fields for Inventory Notes
class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    inventory_backdated = fields.Boolean(string='Inventory Backdated')
    notes = fields.Char(string='Backdated Notes')

# Added StockValuationLayer Fields for Inventory Notes
class StockValuationLayer(models.Model):
    _inherit = 'stock.valuation.layer'

    inventory_backdated = fields.Boolean(string='Inventory Backdated')
    notes = fields.Char(string='Backdated Notes')

# Added AccountMove Fields for Inventory Notes
class AccountMove(models.Model):
    _inherit = 'account.move'

    inventory_backdated = fields.Boolean(string='Inventory Backdated')
    notes = fields.Char(string='Backdated Notes')