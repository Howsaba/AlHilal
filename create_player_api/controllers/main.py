# -*- coding: utf-8 -*-

import json
import odoo
from odoo import http, api
from odoo.http import request, Response, route


class CreateNewPlayer(http.Controller):

    def authenticate_token(self):
        IrHttp = request.env['ir.http'].sudo()
        IrHttp._auth_method_outlook()

    def check_player_exist(self, unique_id):
        partner_id = request.env['res.partner'].search([('unique_id', '=', unique_id)])
        if partner_id:
            return partner_id[0]


    @http.route('/v1/api/create_player', auth="none", type='http', methods=['POST'], csrf=False)
    def api_create_player(self):
        try:
            self.authenticate_token()
            data = json.loads(request.httprequest.data)
            env = api.Environment(request.cr, odoo.SUPERUSER_ID,{'active_test': False})
            partner_id = self.check_player_exist(unique_id=data['unique_id'])
            if not partner_id:
                new_partner_id = env["res.partner"].create([{
                    'name': data['name'],
                    'arabic_name': data['arabic_name'],
                    'id_type': data['id_type'],
                    'unique_id': data['unique_id'],
                    'phone': data['phone'],
                    'email': data['email'],
                    'branch_id': data['branch_id'],
                    'nationality_id': data['nationality_id'],
                    'birthday': data['birthday'],
                    'mobile': data['additional_phone'],
                    'street': data['address'],
                    'comment': data['comments'],
                }])
                if data['id_type'] == 'national_iqama':
                    new_partner_id.national_id = new_partner_id.unique_id
                else:
                    new_partner_id.passport_number = new_partner_id.unique_id
                res = [{
                    'msg': f"The Player {new_partner_id.name} is created success",
                    'status': "new",
                    'player_id': f'{new_partner_id.id}',
                }]
            else:
                res = [{
                    'msg': f"This player {partner_id.name} is already exist",
                    'status': "exist",
                    'player_id': f'{partner_id.id}'
                }]
            return Response(json.dumps(res, sort_keys=True, indent=4), content_type='application/json;charset=utf-8',
                            status=200)
        except Exception as e:
            return Response(
                json.dumps({'error': e.__str__(), 'status_code': 500},
                           sort_keys=True, indent=4),
                content_type='application/json;charset=utf-8', status=200)

    @http.route('/v1/api/create_subscription', auth="none", type='http', methods=['POST'], csrf=False)
    def api_create_subscription(self):
        try:
            self.authenticate_token()
            data = json.loads(request.httprequest.data)
            env = api.Environment(request.cr, odoo.SUPERUSER_ID, {'active_test': False})
            subscription_id = env["sale.order"].create([{
                'is_subscription': True,
                'partner_id': data['player_id'],
                'age_group_id': data['age_group_id'],
                'plan_id': data['membership_type_id'],
                'date_order': data['start_date'],
                'res_team_id': data['team_id'],
                'add_clothes': data['add_clothes'],
                'payment_status': data['payment_status'],
                'payment_method_id': data['payment_method_id'],
                'session_id': data['session_id'],
            }])
            subscription_id.add_clothes_to_lines(discount=data['discount(%)'])
            res = [{
                'msg': f'Your subscription created successfully',
                'subscription name': subscription_id.name
            }]
            return Response(json.dumps(res, sort_keys=True, indent=4), content_type='application/json;charset=utf-8',
                            status=200)
        except Exception as e:
            return Response(
                json.dumps({'error': e.__str__(), 'status_code': 500},
                           sort_keys=True, indent=4),
                content_type='application/json;charset=utf-8', status=200)

    @http.route('/v1/api/create_sale_order', auth="none", type='http', methods=['POST'], csrf=False)
    def api_create_sale_order(self):
        try:
            self.authenticate_token()
            data = json.loads(request.httprequest.data)
            env = api.Environment(request.cr, odoo.SUPERUSER_ID, {'active_test': False})
            lines = []
            product_lines = data['product_lines']
            for line in product_lines:
                lines.append((0, 0, {
                    'product_id': line['product_id'],
                    'product_uom_qty': line['quantity'],
                    'price_unit': line['price'],
                    'discount': line['discount(%)'],
                }))
            sale_order_id = env["sale.order"].create([{
                'partner_id': data['player_id'],
                'branch_id': data['branch_id'],
                'payment_status': data['payment_status'],
                'payment_method_id': data['payment_method_id'],
                'date_order': data['date'],
                'order_line': lines,
            }])
            res = [{
                'msg': f'Your sale order created successfully',
                'sale order name': sale_order_id.name
            }]
            return Response(json.dumps(res, sort_keys=True, indent=4), content_type='application/json;charset=utf-8',
                            status=200)
        except Exception as e:
            return Response(
                json.dumps({'error': e.__str__(), 'status_code': 500},
                           sort_keys=True, indent=4),
                content_type='application/json;charset=utf-8', status=200)

    @http.route('/v1/api/create_product', auth="none", type='http', methods=['POST'], csrf=False)
    def api_create_product(self):
        try:
            self.authenticate_token()
            data = json.loads(request.httprequest.data)
            env = api.Environment(request.cr, odoo.SUPERUSER_ID, {'active_test': False})
            product_id = env["product.product"].create([{
                'name': data['name'],
                'product_arabic_name': data['arabic_name'],
                'lst_price': data['price'],
                'description': data['product_description'],
                'image_1920': data['image(base64)'],
                'branch_id': data['branch_id'],
            }])
            res = [{
                'msg': f"Yor product {product_id.name} created successfully",
                'product_id': f'{product_id.id}'
            }]
            return Response(json.dumps(res, sort_keys=True, indent=4), content_type='application/json;charset=utf-8',
                            status=200)
        except Exception as e:
            return Response(
                json.dumps({'error': e.__str__(), 'status_code': 500},
                           sort_keys=True, indent=4),
                content_type='application/json;charset=utf-8', status=200)

    @http.route('/v1/api/create_team', auth="none", type='http', methods=['POST'], csrf=False)
    def api_create_team(self):
        try:
            self.authenticate_token()
            data = json.loads(request.httprequest.data)
            env = api.Environment(request.cr, odoo.SUPERUSER_ID, {'active_test': False})
            res_team_id = env["res.team"].create([{
                'name': data['name'],
                'arabic_name': data['arabic_name'],
                'branch_id': data['branch_id'],
                'session_id': data['session_id'],
                'coach_id': data['coach_id'],
                'team_capacity': data['team_capacity'],
                'note': data['note'],

            }])
            res = [{
                'msg': f"Yor team {res_team_id.name} created successfully",
                'team_id': f'{res_team_id.id}'
            }]
            return Response(json.dumps(res, sort_keys=True, indent=4), content_type='application/json;charset=utf-8',
                            status=200)
        except Exception as e:
            return Response(
                json.dumps({'error': e.__str__(), 'status_code': 500},
                           sort_keys=True, indent=4),
                content_type='application/json;charset=utf-8', status=200)

    @http.route('/v1/api/create_session', auth="none", type='http', methods=['POST'], csrf=False)
    def api_create_session(self):
        try:
            self.authenticate_token()
            data = json.loads(request.httprequest.data)
            env = api.Environment(request.cr, odoo.SUPERUSER_ID, {'active_test': False})
            session_id = env["session.session"].create([{
                'name': data['name'],

            }])
            res = [{
                'msg': f"Yor session {session_id.name} created successfully",
                'session_id': f'{session_id.id}'
            }]
            return Response(json.dumps(res, sort_keys=True, indent=4), content_type='application/json;charset=utf-8',
                            status=200)
        except Exception as e:
            return Response(
                json.dumps({'error': e.__str__(), 'status_code': 500},
                           sort_keys=True, indent=4),
                content_type='application/json;charset=utf-8', status=200)

    @http.route('/v1/api/create_age_group', auth="none", type='http', methods=['POST'], csrf=False)
    def api_create_age_group(self):
        try:
            self.authenticate_token()
            data = json.loads(request.httprequest.data)
            env = api.Environment(request.cr, odoo.SUPERUSER_ID, {'active_test': False})
            age_group_id = env["age.group"].create([{
                'name': data['name'],
                'arabic_name': data['arabic_name'],
                'suggested_age_year_from': data['years_from'],
                'suggested_age_year_to': data['years_to'],
                'branch_id': data['branch_id'],
            }])
            res = [{
                'msg': f"Yor age group {age_group_id.name} created successfully",
                'session_id': f'{age_group_id.id}'
            }]
            return Response(json.dumps(res, sort_keys=True, indent=4), content_type='application/json;charset=utf-8',
                            status=200)
        except Exception as e:
            return Response(
                json.dumps({'error': e.__str__(), 'status_code': 500},
                           sort_keys=True, indent=4),
                content_type='application/json;charset=utf-8', status=200)

    @http.route('/v1/api/create_coach', auth="none", type='http', methods=['POST'], csrf=False)
    def api_create_coach(self):
        try:
            self.authenticate_token()
            data = json.loads(request.httprequest.data)
            env = api.Environment(request.cr, odoo.SUPERUSER_ID, {'active_test': False})
            coach_id = env["res.coach"].create([{
                'name': data['name'],
                'mobile': data['mobile'],
                'team_id': data['team_id'],
                'branch_id': data['branch_id'],
            }])
            res = [{
                'msg': f"Yor coach {coach_id.name} created successfully",
                'session_id': f'{coach_id.id}'
            }]
            return Response(json.dumps(res, sort_keys=True, indent=4), content_type='application/json;charset=utf-8',
                            status=200)
        except Exception as e:
            return Response(
                json.dumps({'error': e.__str__(), 'status_code': 500},
                           sort_keys=True, indent=4),
                content_type='application/json;charset=utf-8', status=200)

    @http.route('/v1/api/get_product_quantities', auth="none", type='http', methods=['GET'], csrf=False)
    def get_product_quantities(self):
        try:
            self.authenticate_token()
            data = json.loads(request.httprequest.data)
            env = api.Environment(request.cr, odoo.SUPERUSER_ID, {'active_test': False})
            product_id = env["product.product"].browse(data['product_id'])
            if product_id:
                res = [{
                    'product': f"{product_id.name}",
                    'on hand': f'{product_id.qty_available}',
                    'forcasting': f'{product_id.virtual_available}'
                }]
            else:
                res = "No product found with this ID in database"
            return Response(json.dumps(res, sort_keys=True, indent=4), content_type='application/json;charset=utf-8',
                            status=200)
        except Exception as e:
            return Response(
                json.dumps({'error': e.__str__(), 'status_code': 500},
                           sort_keys=True, indent=4),
                content_type='application/json;charset=utf-8', status=200)
