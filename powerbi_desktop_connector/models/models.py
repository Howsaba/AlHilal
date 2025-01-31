# -*- coding: utf-8 -*-
import hashlib
import logging
import os
import requests
from odoo import models, fields, api,_
from ast import literal_eval
from odoo.exceptions import ValidationError


class BIWebConnecterSetting(models.TransientModel):

    ''' Imported Setting for adding Bi connector Settings '''

    _inherit = 'res.config.settings'

    def _get_tf_bi_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        self.env['ir.config_parameter'].set_param('powerbi_desktop_connector.tf_bi_url', base_url+'/finnabi/')
        return base_url+'/finnabi/'

    tf_bi_url = fields.Char(string='Connector Url',default=_get_tf_bi_url,readonly=True)
    
    tf_bi_access_token = fields.Char(string='Access Token',default=(' '*40))

    
    def set_values(self):
        res = super(BIWebConnecterSetting, self).set_values()
        self.env['ir.config_parameter'].set_param('powerbi_desktop_connector.tf_bi_url', self.tf_bi_url)
        self.env['ir.config_parameter'].set_param('powerbi_desktop_connector.tf_bi_access_token', self.tf_bi_access_token)

        

        return res

    @api.model
    def get_values(self):
       
        res = super(BIWebConnecterSetting, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        access_token = ICPSudo.get_param('powerbi_desktop_connector.tf_bi_access_token')
        tf_bi_url = ICPSudo.get_param('powerbi_desktop_connector.tf_bi_url')

        res.update(
                tf_bi_access_token=access_token,
                tf_bi_url=tf_bi_url,

                )
      
        return res

    def nonce(self,length=40, prefix=""):
        rbytes = os.urandom(length)
        return "{}_{}".format(prefix, str(hashlib.sha1(rbytes).hexdigest()))

    def bi_generate_token(self):
        ICPSudo = self.env['ir.config_parameter'].sudo()
        self.env['ir.config_parameter'].set_param('powerbi_desktop_connector.tf_bi_access_token',self.nonce())


        


    