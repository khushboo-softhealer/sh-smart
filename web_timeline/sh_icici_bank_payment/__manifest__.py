# Part of Softhealer Technologies.
{
    "name": "Icici Bank Payment",

    "author": "Softhealer Technologies(Nirali Dholaria)",

    "website": "https://www.softhealer.com",

    "support": "support@softhealer.com",

    "version": "16.0.1",

    "license": "OPL-1",

    "category": "Website",

    "summary": "Bank Details",

    "description": """Bank Format accepted by ICICI Bank""",

    "depends": ['base', 'sh_hr_payroll'],

    "data": [
        'security/ir.model.access.csv',
        'views/sh_payroll.xml',
        'views/sh_default_format.xml',
        'views/employee.xml',
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
    "price": "50",
    "currency": "EUR"
}
