# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Cron Failure",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Extra Tools",
    "license": "OPL-1",
    "summary": "This module helps create logs and send email notifications on cron job success or failure.",
    "description": """This module is designed to log cron job execution details and send email notifications on both cron job success and failure, ensuring better monitoring and issue tracking.""",
    "version": "16.0.1",
    "depends": ["base","hr_attendance","sh_hr_dashboard",'mail'],
    "application": True,
    "data": [
        "security/ir.model.access.csv",
        "security/group_sh_cron_failure.xml",
        "views/res_config_setting_views.xml",
        "views/sh_cron_failure_views.xml"
    ],
    "auto_install": False,
    "installable": True,
}
