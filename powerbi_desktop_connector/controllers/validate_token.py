import re
import ast
import functools
import logging
import requests
import json
from odoo.exceptions import AccessError

from odoo import http
from odoo.addons.powerbi_desktop_connector.common import (
    invalid_response,
    valid_response,
)

from odoo.http import request

def validate_token(func):

    """ This decorater helps to validate the token """

    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        """."""
        ICPSudo = request.env['ir.config_parameter'].sudo()
        access_token = request.httprequest.headers.get("authorization")
        
        if not access_token:
            return invalid_response("access_token_not_found", "missing access token in request header", 401,check_json = request.__dict__.get('jsonrequest',None))
        access_token_data = (
            ICPSudo.get_param('powerbi_desktop_connector.tf_bi_access_token')
        )
       
        if access_token_data != access_token or access_token == '*'*40:
            return invalid_response("access_token", "token seems to have expired or invalid", 401,check_json = request.__dict__.get('jsonrequest',None))

        return func(self, *args, **kwargs)

    return wrap

