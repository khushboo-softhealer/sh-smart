# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    "name": "Softhealer Attendance Sync",

    "author": "Softhealer Technologies",

    "website": "https://www.softhealer.com",

    "support": "support@softhealer.com",

    "version": "16.0.0",

    "category": "Extra Tools",

    "summary": " Attendance",

    "license": "OPL-1",

    "description": """
""",

    "depends": [
        'hr_attendance',
        'hr_work_entry_holidays',
    ],

    "data": [
        'security/ir.model.access.csv',
        'data/sh_attendance_cron_views.xml',
        'wizard/create_leave_wizard_views.xml',
        'views/sh_employee_views.xml',
        'views/sh_attendance_views.xml',
        'views/res_config_settings_views.xml',
        "views/leave_cron_log.xml"
    ],
    # 'assets': {
    #     'web.assets_backend': [
    #         "sh_attendance_sync/static/src/js/mail_notification_manager.js",
    #     ],
    # },

    "installable": True,
    "application": True,
    "auto_install": False,
}
