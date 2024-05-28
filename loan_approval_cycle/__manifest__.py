
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Loan Approval Cycle',
    'version': '17.0.1.0.0',
    'summary': 'Loan Approval Cycle',
    'sequence': -1,
    'depends': ['base', 'approvals','hr_payroll', 'account'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/approval_request_view.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
