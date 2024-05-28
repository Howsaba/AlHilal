
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Extended Subscriptions Modification',
    'version': '17.0.1.0.0',
    'summary': 'Subscription Modification',
    'sequence': -2,
    'depends': ['subscriptions_modification','base', 'sale_subscription', 'hr', 'product', 'hr_holidays', 'account'],
    'data': [
        'views/branch_view.xml',
        'views/hr_employee_view.xml',
        'views/account_move_view.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
