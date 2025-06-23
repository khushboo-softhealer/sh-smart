# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Payslip Auto Send By Email",

    "author": "Softhealer Technologies",

    "website": "https://www.softhealer.com",

    "support": "support@softhealer.com",

    "version": "16.0.0",

    "license": "OPL-1",

    "category": "Human Resources",

    "summary": """auto send payslip by mail app, direct mail payslip module, automatic email payslip, by default send payslip, send payslip automatic,payslip by email, payslip mail odoo""",

    "description": """This module useful to send payslip to employee email.""",

    "depends": ['sh_hr_payroll', 'mail', 'sh_employee_extra_fields'],

    "data": [
            'security/ir.model.access.csv',
            'data/template_hr_payslip_send_auto_email.xml',
            'views/hr_payslip_views.xml',
            'views/hr_employee_views.xml',
            'views/res_config_settings_views.xml',
    ],

    "images": ['static/description/background.png', ],

    "auto_install": False,
    "application": True,
    "installable": True,

    "price": 15,
    "currency": "EUR"
}
