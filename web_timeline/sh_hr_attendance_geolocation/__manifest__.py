# Part of Softhealer Technologies.

{
    'name': 'Attendance Location Information',
    'version': '16.0.1',
    'category': 'Human Resources',
    "license": "OPL-1",
    "author": "Softhealer Technologies (Nirali Dholaria)",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    'summary': "Attendance Information,Attendance With Map,Check-In Send Message Odoo, Check-Out Send Notes App, Send Login Comments Module, Send Message In Logout, Get Check In Location, Get GeoLocation With Map, Get Check Out Location Odoo",
    'description': """
Do you want to get the location of the user while Check In & Check Out? Do you want to send notes or messages when Check In & Check Out? Attendance location Information is a very unique module which will enhance odoo features with this module you can get Check In & Check Out location of the user with google maps. When User Check In & Check Out in Odoo they can write Message, Comment or any notes""",
    'depends': ['hr', 'barcodes', 'hr_attendance', 'sh_attendance_report', 'sh_project_task_base', 'hr_holidays_attendance', 'sh_message'],
    'data': [
        'security/ir.model.access.csv',
        'security/attendance_security.xml',
        # 'data/get_search_result_data.xml',
        'data/resource_calendar_actions.xml',
        'views/predefined_reason_views.xml',
        "wizard/resource_calendar_entry_wizard.xml",
        'views/resource_calender_attendance_views.xml',
        'views/resource_calendar_views.xml',
        'views/hr_attendance_views.xml',
        # 'views/attendance_geolocation_views.xml',
        "views/hr_employee_views.xml",

    ],
    'assets': {
        'web.assets_backend': [
            "sh_hr_attendance_geolocation/static/src/xml/attendance.xml",
            'sh_hr_attendance_geolocation/static/src/js/my_attendances.js',
            "sh_hr_attendance_geolocation/static/src/scss/hrms.scss",
        ],
        # 'web.assets_frontend': [
        #     "sh_hr_attendance_geolocation/static/src/scss/hrms.scss",
        # ],

    },
    'installable': True,
    'auto_install': False,
    "images": ["static/description/background.png", ],
    "live_test_url": "https://youtu.be/uWtmf_nHkdE",
    'application': True,
    "price": 80,
    "currency": "EUR"
}
