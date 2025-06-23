# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Manage Timesheet With Helpdesk | Manage Helpdesk With Timesheet",
    "author": "Softhealer Technologies",
    "website": "http://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Discuss",
    "license": "OPL-1",
    "summary": "Manage Timesheet With Helpdesk Ticket,Helpdesk Ticket With Timesheet,Helpdesk Support Ticket To Timesheet, Manage Helpdesk With Timesheet, Manage Timesheet Helpdesk,Ticket from Timesheet,Helpdesk Tickets Timesheet,Manage helpdesk tickets Odoo",
    "description": """In this module, you can manage the helpdesk ticket timesheet which shows how much work done and how much time spent on the particular ticket. If you have the same description for all the timesheets then we have added a special feature "default description" that will automatically add default description entry when you end timer.""",
    "version": "16.0.1",
    "depends": [
        "sh_helpdesk",
        "hr_timesheet",
        "sh_task_time"
    ],
    "data": [
        'security/sh_helpdesk_timesheet_groups.xml',
        'security/ir.model.access.csv',
        'views/res_config_setting_views.xml',
        'views/account_analytic_line_views.xml',
        'views/ticket_time_account_line_views.xml',
        'views/helpdesk_ticket_views.xml',
        'wizard/sh_start_ticket_views.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'sh_helpdesk_timesheet/static/src/js/time_track.js',
            'sh_helpdesk_timesheet/static/src/scss/time_track.scss',
        ],
        'web.assets_frontend': [

        ],

    },

    "application": True,
    "auto_install": False,
    "installable": True,
    "images": ["static/description/background.png", ],
    "price": 10,
    "currency": "EUR"
}
