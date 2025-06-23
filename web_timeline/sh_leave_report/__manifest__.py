# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Print Leave Report",
    "author": "Softhealer Technologies (Nitin Ubhadiya)",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Human Resources",
    "license": "OPL-1",
    "summary": """
 Print Leave Request Report, Print Leave Approved Report,
Employee Leave Report,Leave Management,Holidays Report,
Print Leave Time Off Request, Holiday Report Odoo
""",
    "description": """
Do you want to print the leave request report?
Do you want to print an approve leave report?
This module used to print employee leave reports.
The manager or employee can print the leave report.
Print Leave Request Report Odoo
Print Employee Leave Report,Print Leave Approved Report,
Leave Management, Print Employee Holiday Report Odoo
Print Leave Approved Report, Print Employee Leave Report,
Leave Management App, Print Employee Holiday Report Odoo
""",
    "license": "OPL-1",
    "version": "16.0.1",
    "depends": ["hr_holidays"],
    "application": True,
    "data": [
            "security/ir.model.access.csv",
            "data/hr_leave_data.xml",
            "report/hr_leave_templates.xml",
            "views/hr_leave_views.xml",
    ],
    'external_dependencies': {
        'python': [
            'html2text',
        ],
    },
    "images": ["static/description/background.png", ],
    "live_test_url": "https://youtu.be/HNsDQJDroME",
    "auto_install": False,
    "installable": True,
    "price": 20,
    "currency": "EUR"
}
