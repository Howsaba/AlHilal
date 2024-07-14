
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Material Request',
    'version': '17.0.1.0.0',
    'summary': 'Material Request',
    'sequence': -1,
    'depends': ['base', 'stock', 'purchase', 'mail', 'subscriptions_modification'],
    'data': [
        'security/sequrity.xml',
        'security/ir.model.access.csv',
        'views/material_request_view.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
