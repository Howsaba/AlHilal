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
    def api_get_employee(self):
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
                }])
                if data['id_type'] == 'national_iqama':
                    new_partner_id.national_id = new_partner_id.unique_id
                else:
                    new_partner_id.passport_number = new_partner_id.unique_id
                res = f"The Player {new_partner_id.name} is created success"
            else:
                res = f"This player {partner_id.name} is already exist"
            return Response(json.dumps(res, sort_keys=True, indent=4), content_type='application/json;charset=utf-8',
                            status=200)
        except Exception as e:
            return Response(
                json.dumps({'error': e.__str__(), 'status_code': 500},
                           sort_keys=True, indent=4),
                content_type='application/json;charset=utf-8', status=200)
