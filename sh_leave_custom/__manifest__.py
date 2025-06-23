# -*- coding: utf-8 -*-
# Part of Softhealer Technologies 2022.
{
    "name": "Leave Custom",
    "author": "Softhealer Technologies - Nitin Ubhadiya",
    "website": "https://www.softhealer.com",
    "support": "info@softhealer.com",
    'license': 'AGPL-3',
    "category": "HR",
    "summary": "Leave Custom",
    "description": """
    Leave Custom
                    """,
    "version": "16.0.1",
    "depends": ["hr_holidays", "hr_contract", "analytic", "hr_attendance", "hr_timesheet", "sh_project_task_base", "sh_hr_attendance_geolocation"],
    "application": True,
    "data": [
        'security/ir.model.access.csv',
        'security/leave_security.xml',
        'data/hr_leave_data.xml',
        'data/resource_calendar_data.xml',
        'wizard/sh_global_leave_wizard_views.xml',
        'wizard/sh_employee_leave_allocation_wizard_views.xml',
        'views/hr_leave_type_views.xml',
        'views/hr_leave_views.xml',
        'views/hr_leave_allocation_views.xml',
        'views/hr_contract_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            "sh_leave_custom/static/src/dashboard/time_off_card.xml",
        ],
    },

    "auto_install": False,
    "installable": True,
}
