# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

{
    "name": "Attendance Auto Checkout",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "license": "OPL-1",
    "category": "Human Resources",
    "summary": "Auto-checkout attendance of employees,  Manage Employee Attendance Module, Calculate Working Hours App,Track Check-Out Time, Get Attendance Detail, Auto Checkout Attendance,Employee Work Hours,Attendance management,Auto Attendance Odoo",
    "description": """Do you want auto-checkout attendance of employees? This module helps to manage attendance easily. When an employee forgets to check out at the end on the day then this module auto-checkout the attendance. cheers!
 Attendance Auto Checkout Odoo
 Manage Employee Attendance Module, Calculate Employee Working Hours, Track Employee Check-Out Time, Auto Checkout Attendance, Handle Employee Work Hours Odoo """,
    "version": "16.0.1",
    "depends": ["hr_attendance", "sh_attendance_modification_request", "account", "sh_task_time", "sh_attendance_sync", "sh_hr_dashboard"],
    "application": True,
    "data": [
        "data/attendance_auto_checkout_data.xml",
        "views/res_config_settings_views.xml",

    ],
    "images": ["static/description/background.png", ],
    "auto_install": False,
    "installable": True,
    "license": "OPL-1",
    "price": 30,
    "currency": "EUR"
}
