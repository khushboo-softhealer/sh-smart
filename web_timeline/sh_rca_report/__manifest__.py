# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "RCA Report",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Extra Tools",
    "license": "OPL-1",
    "summary": "Generate Root Cause Analysis (RCA) Reports for Project Tasks",
    "description": """This module allows users to create and manage Root Cause Analysis (RCA) reports directly from project tasks in Odoo. It helps teams systematically identify, document, and analyze the root causes of issues encountered during project execution. The module also supports logging of cron job execution and can send email notifications on success or failure, ensuring timely alerts and improved process monitoring.""",
    "version": "16.0.1",
    "depends": ["base","project","sh_project_task_base","mail"],
    "data": [
        "data/sh_rca_sequence.xml",
        "security/ir.model.access.csv",
        "views/sh_rca_report_views.xml",
        "views/project_task_views.xml",
        "reports/sh_rca_report_report.xml",
        "views/project_project_views.xml",
    ],
    "application": True,
    "auto_install": False,
    "installable": True,
}
