# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Employee Extra Fields",

    "author": "Softhealer Technologies (Nirali Dholaria)",

    "website": "https://www.softhealer.com",

    "support": "support@softhealer.com",

    "version": "16.0.0",

    "license": "OPL-1",

    "category": "Extra Tools",

    "summary": "Add Extra Fields Module, Employee Form Add Fields, Employee Extra Fields App, Custom Fields In Employee Form, Extra Field In Employee Screen Odoo",

    "description": """Currently, odoo not provide to add extra fields for employees. This module allows you to add extra fields in the employee form view. You can track details like,Work information: Reference by, work country.
Private information: Previous nationality, passport detail, blood group, age, DOB, religion, marital status, height-weight.
Other detail: Dates(joining date, employment date, confirmation date, marriage date), social media detail, technical-non technical skills, certifications. known language, experience, education detail, job type, PF account no, facility details.""",

    "depends": [
            'hr',
    ],

    "data": [
        'security/ir.model.access.csv',
        'views/sh_skills.xml',
        'views/sh_company_facilities.xml',
        'views/sh_employee_religion.xml',
        'views/sh_employee_emergency.xml',
        'views/sh_employee_extra_fieds.xml',
    ],

    "installable": True,
    "auto_install": False,
    "application": True,
    "images": ["static/description/background.png", ],
    "price": "20",
    "currency": "EUR"
}
