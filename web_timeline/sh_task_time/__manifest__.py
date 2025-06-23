# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name":
    "Task Timer",
    "author":
    "Softhealer Technologies (Kishan Patadiya)",
    "website":
    "https://www.softhealer.com",
    "support":
    "info@softhealer.com",
    "version":
    "16.0.2",
    "license": "OPL-1",
    "category":
    "Project",
    "summary":
    """
	task timer, manage task time app, countdown timer module, calculate task start time, calculate work stop time, manage work time duration, time report timer odoo""",
    "description":
    """This module allow user to start/stop time of task. Easy to calculate duration of time taken for task.""",
    "depends":
    ['project','sale_management', 'hr_timesheet', 'analytic','sale_timesheet',
    'sh_project_task_base','sh_notifications','sh_project_mgmt'],
    "data": [

        'security/ir.model.access.csv',
        'security/sh_edit_timesheet_groups.xml',
        'data/project_task_data.xml',
        'data/resource_calendar_attendance_data.xml',

        'wizard/sh_update_timesheet_views.xml',
        'wizard/sh_add_users_views.xml',
        'views/resource_calendar_attendance_views.xml',
        'views/sh_start_timesheet_views.xml',
        
        'views/project_project_views.xml',
        'views/task_time_account_line_views.xml',

        'views/project_task_views.xml',
        'views/res_config_setting.xml',
        'wizard/sh_create_new_task_wizard_views.xml',
        'wizard/sh_edit_timesheet_views.xml',
        
        'views/account_move_views.xml',
        'views/invoice_report.xml',
        'views/res_users_views.xml',
        'views/account_analytic_line_views.xml',

        'views/sh_transfer_timesheet.xml',
        'views/sh_pause_task_entry_views.xml',
    ],

    "images": [
        "static/description/background.png",
    ],

    'assets': {
        'web.assets_backend': [
            'sh_task_time/static/src/xml/time_track.xml',
            # new_changes
            'sh_task_time/static/src/xml/resume_tmpl.xml',

            'sh_task_time/static/src/js/HackTimer.js',
            'sh_task_time/static/src/js/time_track.js',
            
            # new_changes
            'sh_task_time/static/src/js/pending_task_menu.js',

            'sh_task_time/static/src/scss/time_track.scss',
        ],
    },

    "installable":
    True,
    "auto_install":
    False,
    "application":
    True,
    "price":
    "9",
    "currency":
    "EUR"
}
