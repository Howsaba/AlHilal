{
    'name': 'Branches Groups',
    'version': '17.0.1.0.0',
    'summary': 'Branches Groups',
    'sequence': -1,
    'depends': ['base', 'sale_subscription', 'hr','subscriptions_modification'],
    'data': ["views/res_users_branches.xml",
             "views/edit_branches_views.xml"

    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
