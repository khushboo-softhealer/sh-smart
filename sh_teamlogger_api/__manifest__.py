# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

{
    'name': 'Fetch Teamlogger Details',
    'author': 'Softhealer Technologies',
    'website': 'https://www.softhealer.com',
    'license': 'OPL-1',
    'support': 'support@softhealer.com',
    'version': '0.0.1',
    'category': 'HR',
    'summary': " ",
    'description': """""",
    'depends': ['hr','hr_attendance'],
    'data': [
        "security/rmm_security.xml",
        "security/ir.model.access.csv",
        "data/teamlogger_cron.xml",
        "views/hr_employee_views.xml",
        "views/sh_teamlogger_attendance_views.xml"
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': '0',
    'currency': 'EUR',
}
