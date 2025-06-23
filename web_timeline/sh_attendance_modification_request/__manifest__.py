# -*- coding: UTF-8 -*-
# Part of Softhealer Technologies.
{
    'name': "Attendance Modification Request",
    'author': 'Softhealer Technologies',
    'website': 'https://www.softhealer.com(Nirali Dholaria)',
    "support": "support@softhealer.com",
    'category': 'Human Resources',
    "license": "OPL-1",
    'version': '16.0.1',
    "summary": "Attendances Modification Request,Attendance Modify Request,Attendance Change Request,Employee Attendance Modification,Attendance Management,Employee Attendance,Hr Attendance Modification Tracking,Attendance Track Odoo",
    "description": """Sometimes employees accidentally forget to do check-in/check-out so this module helps employees to send attendance modification requests to the manager. The manager gets a notification about the attendance modification request sent by the employee and when they approve or reject requests, an employee gets a notification about it.""",
    'depends': ['sh_hr_attendance_geolocation', 'hr_timesheet', 'sh_project_task_base'],
    'data': [
        'security/attendance_modification_request_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/mail_template_attendance_modification_request_data.xml',
        'wizard/sh_update_attendance_wizard_views.xml',
        'wizard/sh_attendance_modification_wizard_views.xml',
        'views/attendance_modification_request.xml',
        'views/action_menus.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    "images": ["static/description/background.png", ],
    "price": 30,
    "currency": "EUR"
}
