# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "HR Payroll Report",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Extra Tools",
    "summary": "",
    "description": """""",
    "version": "16.0.1",
    "depends": ["base", "base_setup", "sh_hr_payroll", "sh_hr_payroll_tds"],
    "application": True,
    "data": [
        "security/ir.model.access.csv",
        "wizard/sh_hr_payroll_report_wizard_views.xml"
    ],
    "license": "OPL-1",
    "auto_install": False,
    "installable": True,
}
