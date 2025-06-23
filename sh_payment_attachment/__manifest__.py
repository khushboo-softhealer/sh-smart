# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

{
    'name': 'Payment Attachment',
    'author': 'Softhealer Technologies - Daki Ketan',
    'website': 'https://www.softhealer.com',
    "support": "support@softhealer.com",
    "license": "OPL-1",
    'version': '16.0.1',
    'category': 'Extra Tools',
    'summary': 'Payment Attachment Odoo',
    'description': """Files Attachment Feature add for Payment Registration""",
    'depends': ['account'],
    'data': ["wizard/account_payment_register_wizard_views.xml", ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
