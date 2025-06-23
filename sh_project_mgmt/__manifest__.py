# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Project Management",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Extra Tools",
    "summary": "",
    "description": """test""",
    "version": "16.0.1",
    "depends": ["base", "base_setup", "sale", "sh_project_task_base","sh_global_requests"],
    "application": True,
    "data": [
        "security/project_security.xml",
        "security/ir.model.access.csv",
        "data/ir_cron.xml",
        "views/res_config_settings_views.xml",
        "views/res_partner_views.xml",
        "views/sale_order_views.xml",
        "views/sale_order_line_views.xml",
        "views/sh_estimation_template_views.xml",
        "views/account_analytic_line_views.xml",
        "views/project_project_views.xml",
        "views/project_task_views.xml",
        "views/project_pl_view.xml",
        "views/account_move_view.xml",
        'views/analytic_line_multi_action.xml',
        "wizards/sh_project_create_wizard.xml",
        "wizards/sh_update_project_wizard_views.xml",
    ],

    'assets': {
        'web.assets_backend': [
        'sh_project_mgmt/static/src/xml/global_project_quick_create.xml',
        'sh_project_mgmt/static/src/js/global_project_quick_create.js',
        ],
    },
    "license": "OPL-1",
    "auto_install": False,
    "installable": True,
}
