from odoo import api, fields, models, _
from odoo.exceptions import UserError


class MaterialRequest(models.Model):
    _name = "material.request"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(default='New', readonly=True)
    request_date = fields.Date(tracking=True)
    tag_ids = fields.Many2many('request.tag', tracking=True)
    source_id = fields.Many2one('stock.location', tracking=True)
    destination_id = fields.Many2one('stock.location', tracking=True)
    operation_type_id = fields.Many2one('stock.picking.type', domain=[('code', '=', 'internal')])
    picking_ids = fields.Many2many('stock.picking')
    picking_count = fields.Integer(compute='compute_counts')
    purchase_order_ids = fields.Many2many('purchase.order')
    purchase_count = fields.Integer(compute='compute_counts')
    vendor_id = fields.Many2one('res.partner')
    material_request_line_ids = fields.One2many('material.request.line', 'material_request_id', required=True,
                                                tracking=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('pending', 'Pending'),
                              ('in_progress', 'In Progress'),
                              ('done', 'Done'),
                              ('cancel', 'Cancelled'),
                              ], default='draft', tracking=True)

    @api.depends('picking_ids', 'purchase_order_ids')
    def compute_counts(self):
        for rec in self:
            rec.picking_count = len(rec.picking_ids)
            rec.purchase_count = len(rec.purchase_order_ids)

    def purchase_order_action(self):
        action = self.env['ir.actions.act_window']._for_xml_id('purchase.purchase_rfq')
        action['domain'] = [('id', 'in', self.purchase_order_ids.ids)]
        action['context'] = {
            'create': 0
        }
        return action

    def transfer_action(self):
        action = self.env['ir.actions.act_window']._for_xml_id('stock.action_picking_tree_internal')
        action['domain'] = [('id', 'in', self.picking_ids.ids)]
        action['context'] = {
            'create': 0
        }
        return action

    def check_availability(self):
        for line in self.material_request_line_ids:
            if line.qty <= line.product_id.qty_available:
                line.is_available = True

    @api.model
    def create(self, vals_list):
        if 'name' not in vals_list or vals_list['name'] == _('New'):
            vals_list['name'] = self.env['ir.sequence'].next_by_code('material.request') or _('New')
        return super().create(vals_list)

    def action_confirm(self):
        self.check_availability()
        self.state = 'pending'

    def action_create_purchase(self):
        if not self.vendor_id:
            raise UserError(_('You should enter all purchase info fields'))
        product_line = []
        for line in self.material_request_line_ids.filtered(lambda x: not x.is_available):
            if not line.purchased:
                product_line.append((0, 0, {
                    'product_id': line.product_id.id,
                    'product_qty': line.qty,
                }))
                line.purchased = True
        if product_line:
            purchase_id = self.env['purchase.order'].create({
                'partner_id': self.vendor_id.id,
                'order_line': product_line
            })
            self.purchase_order_ids = [(4, purchase_id.id)]
        else:
            raise UserError(_('There is no line to purchase'))

    def action_create_internal_transfer(self):
        if not (self.operation_type_id and self.destination_id and self.source_id):
            raise UserError(_('You should enter all inventory info fields'))
        pick_lines = []
        for line in self.material_request_line_ids.filtered(lambda x: x.is_available):
            if not line.transferred:
                pick_line_values = {
                    'name': line.product_id.name,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.qty,
                    'state': 'draft',
                    'location_id': self.source_id.id,
                    'location_dest_id': self.destination_id.id,
                }
                pick_lines.append((0, 0, pick_line_values))
                line.transferred = True
        if pick_lines:
            picking = {
                'picking_type_id': self.operation_type_id.id,
                'location_id': self.source_id.id,
                'location_dest_id': self.destination_id.id,
                'move_type': 'direct',
                'origin': f'From Material Request {self.name}',
                'move_ids_without_package': pick_lines,
            }

            transfer = self.env['stock.picking'].sudo().create(picking)
            self.picking_ids = [(4, transfer.id)]
        else:
            raise UserError(_('There is no line to Transfer'))

    def action_in_progress(self):
        if all(x.transferred for x in self.material_request_line_ids):
            self.state = 'in_progress'
        else:
            raise UserError(_('Some Product Not Transferred !!'))

    def action_done(self):
        flag = False
        for pick in self.picking_ids:
            if pick.state != 'done':
                flag = True
        if flag:
            raise UserError(_('Your picking must be done !!'))
        self.state = 'done'

    def action_cancel(self):
        self.state = 'cancel'


class MaterialRequestLine(models.Model):
    _name = "material.request.line"

    material_request_id = fields.Many2one('material.request')
    product_id = fields.Many2one('product.product')
    qty = fields.Integer()
    is_available = fields.Boolean(readonly=True)
    purchased = fields.Boolean(readonly=True)
    transferred = fields.Boolean(readonly=True)


class RequestTag(models.Model):
    _name = "request.tag"

    name = fields.Char(required=True)
