# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Multi Company Customization",
    "author": "Softhealer Technologies,Odoo SA",
    "license": "OPL-1",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Accounting",
    "summary": "Multi Company Customization",
    "description": """Multi Company Customization""",
    "version": "16.0.1",
    'depends': [
        'sh_hr_payroll',
        'sale',
        'purchase',
        'account','hr_holidays','project','sh_project_mgmt'
    ],
    'data': [
        'security/company_security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
       'views/leave_custom.xml',
       'views/sale_view.xml',
       'views/purchase_view.xml',
       'views/account_view.xml',
       'views/project_view.xml',
       'views/multi_company_log.xml',
    ],
    "application": True,
    "auto_install": False,
    "installable": True,
    "images": ["static/description/background.png", ],
}
