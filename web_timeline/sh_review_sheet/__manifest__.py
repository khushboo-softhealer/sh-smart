# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Employee Review Management",

    "author": "Softhealer Technologies - Mihir",

    "website": "https://www.softhealer.com",

    "support": "support@softhealer.com",

    "version": "16.0.2",

    "category": "Extra Tools",

    "summary": "Employee Review Management",

    "description": """Employee Review Management""",

    "depends": ['base','sh_project_task_base'],

    "data": [
        "security/ir.model.access.csv",
        "data/ir_cron_data.xml",
        "security/sh_review_sheet_groups.xml",
        "security/sh_review_sheet_security.xml",
        "views/sh_review_sheet_line_views.xml",
        "views/sh_review_sheet_views.xml",
    ],       
    "license": "OPL-1",
    "installable": True,
    "auto_install": False,
    "application": True,
}
