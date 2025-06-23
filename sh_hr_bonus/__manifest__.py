# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "HR Bonus",
    "author": "Softhealer Technologies - Nayan",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "",
    "summary": "",
    "license": "OPL-1",
    "version": "16.0.1",
    "depends": ["sh_hr_payroll", "sh_hr_dashboard", "sh_icici_bank_payment"],
    "data": [
        'data/ir_sequence.xml',
        'data/salary_rule.xml',
        'security/ir.model.access.csv',
        'report/sh_bonus_template_templates.xml',
        'views/sh_bonus_template_views.xml',
        'views/sh_bonus_allocation_views.xml',
    ],

    "images": [""],
    "live_test_url": "",
    "auto_install": False,
    "installable": True,
    "application": True,
    "price": "",
    "currency": ""
}
