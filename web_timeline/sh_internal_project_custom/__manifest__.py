# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Internal Project Customization",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Extra Tools",
    "summary": "",
    "description": """""",
    "version": "16.0.1",
    "depends": ["sale_management","sh_project_task_base","sh_project_mgmt","sh_helpdesk",],
    "application": True,
    "data": [
        # SECURITY
        "security/ir.model.access.csv",
        "security/project_security.xml",

        #DATA
        "data/ir_cron.xml",

        # VIEWS
        "views/project_project_views.xml",
        "views/project_task_views.xml",
        "views/sale_order_views.xml",
        "views/helpdesk_ticket_views.xml",

        # WIZARD
        "wizard/sh_move_timesheet_wizard_views.xml",
    ],
    "license": "OPL-1",
    "auto_install": False,
    "installable": True,
}
