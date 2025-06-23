# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Update Timehsheets",
    "author": "Softhealer Technologies(Nirali  Dholaria)",
    "website": "http://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "HR",
    "license": "OPL-1",
    "summary": """Update Timehsheets""",
    "description": """Update Timehsheets""",
    "version": "16.0.1",
    "depends": [
        "base",
        "sale_management",
        "account",
        "hr",
        "sale_timesheet",
    ],

    "data": [
        'data/timesheet_multi_action.xml',
        "security/ir.model.access.csv",
        # "views/project_config_settings.xml",
        'wizard/sh_update_timesheet_wizard_views.xml',
    ],
    "images": ["static/description/background.png", ],
    "live_test_url": "",
    "application": True,
    "auto_install": False,
    "installable": True,
    "price": 30,
    "currency": "EUR"
}
