# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "To Do Management",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Extra Tools",
    "summary": "",
    "description": """""",
    "version": "16.0.1",
    "depends": ["base", "mail", "utm", "base_setup","sh_project_task_base","sh_global_requests","hr"],
    "application": True,
    "data": [
        # SECURITY
        "security/ir.model.access.csv",
        "security/employee_task_allocation_security.xml",
        # VIEWS
        "views/sh_employee_task_allocation_views.xml",
        # WIZARD
        "wizard/sh_employee_task_allocation_wizard_views.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'sh_to_do_management/static/src/xml/sh_global_request_icon_template.xml',
            'sh_to_do_management/static/src/js/global_request_icon_menu.js',
            'sh_to_do_management/static/src/scss/kanban_ribbon.scss',
        ],
    },
    "license": "OPL-1",
    "auto_install": False,
    "installable": True,
}
