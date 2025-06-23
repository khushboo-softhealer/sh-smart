# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "HR Payroll - TDS Calcualtion",
    "author": "Softhealer Technologies,Odoo SA",
    "license": "OPL-1",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Accounting",
    "summary": "HR Payroll - TDS Calcualtion",
    "description": """HR Payroll - TDS Calcualtion""",
    "version": "16.0.1",
    'depends': [
        'sh_hr_payroll',
    ],
    'data': [
        'data/payroll_data.xml',
        'security/ir.model.access.csv',
        'views/res_company_view.xml',
        'views/hr_employee_views.xml', 
        'views/hr_contract_view.xml',
        'views/tax_slab_template.xml',
        'views/hr_payslip_view.xml',
        'views/contract_tds_deduction_details.xml',
    ],
    "application": True,
    "auto_install": False,
    "installable": True,
    "images": ["static/description/background.png", ],
}
