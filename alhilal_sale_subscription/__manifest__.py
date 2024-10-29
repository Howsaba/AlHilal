{
    'name': 'billing period days',
    'version': '17.0.1.0.0',
    'summary': 'Subscription Modification',
    'sequence': -1,
    'depends': ['base', 'sale_subscription', 'hr', 'product','contacts','sale','purchase','sale_management'],
    'data': ['views/billing_period_days.xml',
             'views/sale_order_inherit.xml'

             ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
