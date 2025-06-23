# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Employee Goal Management",

    "author": "Softhealer Technologies - Nitin",

    "website": "https://www.softhealer.com",

    "support": "support@softhealer.com",

    "version": "16.0.2",

    "category": "Extra Tools",

    "summary": "Employee Goal Management",

    "description": """Employee Goal Management""",

    "depends": ['base_setup', 'hr', 'project', 'partner_autocomplete','hr_contract','sh_hr_contract','sh_leave_custom'],

    "data": [
        "data/ir_sequence.xml",
        "data/ir_cron_data.xml",
        "security/ir.model.access.csv",
        "security/sh_employee_goal_management_groups.xml",
        "security/sh_employee_goal_management_security.xml",

        "views/sh_goal_sheet_template_views.xml",
        "views/sh_goal_sheet_category_views.xml",
        "views/sh_goal_sheet_views.xml",
        "views/sh_goal_marks_views.xml",
        "views/res_config_setting_views.xml",
        "views/sh_goal_sheet_line_views.xml",
        "views/hr_contract_view.xml",

        "wizard/sh_generate_goal_sheet_wizard_views.xml",
    ],
    'assets': {
        'web.assets_backend': [
    
            # pyeval domain
            "sh_employee_goal_management/static/src/lib/pyeval.js",
        ],
       
    },
    "license": "OPL-1",
    "installable": True,
    "auto_install": False,
    "application": True,
    "price": "500",
    "currency": "EUR"
}
