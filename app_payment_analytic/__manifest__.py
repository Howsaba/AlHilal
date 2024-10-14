# -*- coding: utf-8 -*-
{
    'name': 'Payment Analytic Distribution',
    'category': 'Accounting',
    'summary': 'This module help you to set analytic distribution on payment'
               '| analytic distribution on Customer/Vendor Payment '
               '| analytic distribution,on tree/from view'
               '| payment journal entries with analytic distribution',
    'description': """This apps helps you to set analytic distribution on payment.""",
    "author": "Controlwave Technologies",
    "development_status": "Production/Stable",
    "version": "17.0.1.0.0",
    'depends': ['account'],
    "images":['static/description/main_screenshot.png'],
    "data": [
        'security/account_security.xml',
        'views/account_payment_view.xml',
        'wizard/account_payment_register_analytic_view.xml',
    ],
    "license": "OPL-1",
    'price': 15,
    'currency': "EUR",
    'installable': True,
    'auto_install': False,
    'application': False,
}
