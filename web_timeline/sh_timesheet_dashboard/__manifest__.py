# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Timesheet Dashboard",

    "author": "Softhealer Technologies",

    "website": "https://www.softhealer.com",

    "support": "support@softhealer.com",

    "license": "OPL-1",

    "category": "Sales",

    "summary": "Timesheet Dashboard",

    "description": """User Timesheet Dashboard""",

    "version": "16.0.1",

    "depends": ['hr_attendance', 'hr_timesheet', "sh_task_time"],

    "data": [
        'security/ir.model.access.csv',
        'views/timesheet_dashboard.xml',
        'data/data.xml',
        'views/timesheet_table.xml',
        'views/timesheet_employee_data.xml',
    ],
    "assets": {
        "web.assets_backend": [
            "sh_timesheet_dashboard/static/src/js/timesheet_dashboard.js",
            "sh_timesheet_dashboard/static/src/css/style.css",
        ]
    },
    "images": [],

    "auto_install": False,
    "application": True,
    "installable": True,

    "price": 0,
    "currency": "EUR"
}
