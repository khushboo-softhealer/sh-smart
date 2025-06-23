# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Employee Mass Update",
    "author": "Softhealer Technologies - Daki Ketan",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "license": "OPL-1",
    "version": "16.0.1",
    "category": "Employee",
    "summary": "Employee Mass Update",
    'sequence': 10,
    "description": """Mass Update job position, manger, hr manager, and coach in hr employee.""",
    "depends": ["sh_hr_contract"],
    "data": ["security/ir.model.access.csv",
            "security/employee_security.xml",
            "views/mass_tag_update_action.xml",

            "wizard/sh_employee_manager_update_mass_tag_wizard_views.xml",
             ],
    "installable": True,
    "auto_install": False,
    "application": True,
    "price": "15",
    "currency": "EUR",
}
