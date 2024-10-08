
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Subscriptions Modification',
    'version': '17.0.1.0.0',
    'summary': 'Subscription Modification',
    'sequence': -1,
    'depends': ['base', 'sale_subscription', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/age_group_view.xml',
        'views/res_branch_view.xml',
        'views/res_coach_view.xml',
        'views/res_partner_view.xml',
        'views/res_team_view.xml',
        'views/session_view.xml',

    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
