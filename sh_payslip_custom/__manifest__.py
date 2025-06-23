# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Payslip Custom",
    "author": "Softhealer Technologies - Nayan",
    "website": "https://www.softhealer.com",
    "support": "info@softhealer.com",
    "category": "Website",
    "license": "OPL-1",
    "summary": "This module useful to skip address step in shop flow.",
    "description": """
    This module useful to skip address step in shop flow
                    """,
    "version": "16.0.1",
    "depends": ["sh_hr_payroll", "hr_contract"],
    "application": True,
    "data": [
        'security/hr_contract_security.xml',
        'views/hr_payslip_views.xml',
        'views/sh_payslip_run_views.xml',
        'report/hr_payslip_templates.xml',
    ],
    "auto_install": False,
    "installable": True,
}
