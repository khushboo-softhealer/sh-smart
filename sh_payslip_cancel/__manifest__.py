# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Payslip Cancel",
    "author": "Softhealer Technologies - Nayan",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Human Resources",
    "license": "OPL-1",
    "summary": "Payslip Cancel Odoo, Reject Payslip, Cancel Employee Payslip, Delete Payslip Module, Reject Payslip, Remove User Payslip, Denied Payslip App, Cancel Journal Entry, Remove Journal Entry, Cancel Payslip, Payslip Cancel, Reject Journal Entry Odoo",
    "description": """
Do you want to cancel Payslip of an employee even if it's done? This module helps to cancel payslip which is already in the done state. This module will cancel the journal entry. here we added the "Refunded Payslip" field it shows detail if payslip is refunded.""",
    "version": "16.0.1",
    "depends": [
        "sh_hr_payroll",
        "sh_hr_payroll_account",
        "account"
    ],
    "data": [
        'views/hr_payslip_views.xml',
    ],

    'images': ['static/description/background.png', ],
    "live_test_url": "https://youtu.be/hr1EWCOh_Ng",
    "application": True,
    "auto_install": False,
    "installable": True,
    "price": 20,
    "currency": "EUR"

}
