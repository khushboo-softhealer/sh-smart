# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Timesheet Report",
    "author": "Softhealer Technologies - Nitin",
    "website": "https://www.softhealer.com",
    "support": "info@softhealer.com",
    "version": "16.0.2",
    "license": "OPL-1",
    "category": "Project",
    "summary":
    """task timer, manage task time app, countdown timer module, calculate task start time, calculate work stop time, manage work time duration, time report timer odoo""",
    "description":
    """This module allow user to start/stop time of task. Easy to calculate duration of time taken for task.""",
    "depends": ['project', 'hr_timesheet', 'account', 'sh_project_task_base'],
    "data": [
        'security/ir.model.access.csv',
        'data/analytic_line_server_action.xml',
        'report/sh_timesheet_report_views.xml',
        'report/account_analytic_line_report_views.xml',
        'report/sh_all_timesheet_project_report_views.xml',
        'report/timesheet_entries_report.xml',
        'views/account_analytic_line_views.xml',
        'views/project_task_templates.xml',
        'views/project_task_views.xml',
        'views/account_move_views.xml',
        'wizard/sh_timesheet_report_wizard_views.xml',
    ],
    "qweb": ['static/src/xml/time_track.xml'],
    "images": ["static/description/background.png"],
    "installable": True,
    "auto_install": False,
    "application": True,
}
