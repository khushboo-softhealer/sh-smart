# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Employee Performance Report",
    "author": "Softhealer Technologies - Daki Ketan",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "license": "LGPL-3",
    "version": "16.0.1",
    "category": "Accounting",
    "summary": "Employee Performance Report Odoo",
    "description": """
        Download Performance Report of Employees (.xls).
        -> in report we calculating Employees Leaves, Attendance Score, Late Coming Score,
        -> Timesheet Score, and Average. 
    """,
    "depends": [
        "analytic",
        "hr_attendance",
        "sh_hr_payroll",
        "sh_leave_custom",
        "sh_project_task_base",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/sh_performance_report_security.xml",
        "wizard/sh_performance_report_wizard_views.xml",
        "views/sh_performance_report_menus.xml",
        'views/hr_contract_views.xml',
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
}
