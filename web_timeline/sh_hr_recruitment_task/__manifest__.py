# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Hr Recruitement Task",
    "author": "Softhealer Technologies - Nayan",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "license": "OPL-1",
    "version": "16.0.1",
    "category": "Stock",
    "summary": " Hr Recruitement Task",
    "description": """Hr Recruitement Task""",
    "depends": ["hr_recruitment", "project", 'sh_hr_placement', 'sh_notifications', 'sh_push_notification_tile','website_hr_recruitment'],
    "data": [
        "security/ir.model.access.csv",
        "wizard/sh_create_task_wizard_views.xml",
        "views/hr_applicant_views.xml",
        "views/res_config_settings_views.xml",
        "views/res_users_views.xml",
        "views/hr_job_views.xml",
        "views/project_task_views.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
    "currency": "EUR"
}
