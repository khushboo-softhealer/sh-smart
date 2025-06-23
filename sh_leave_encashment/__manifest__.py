# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

{
    "name": "Employee Leave Encashment",
    
    "author": "Softhealer Technologies",
    
    "website": "https://www.softhealer.com",    
    
    "support": "support@softhealer.com",   

    "version": "16.0.1",

    "license": "OPL-1",
    
    "category": "Extra Tools",
    
    "summary": "Employee Leave Encashment app ",
        
    "description": """Employee Leave Encashment""",
     
    "depends": ['hr_contract','account','sh_employee_ot','hr','hr_holidays'],
        
    "data": [
        "data/leave_encashment_salary_rule.xml",
        "security/ir.model.access.csv",
        "views/sh_leave_encasement_views.xml"
    ],

    "installable": True,
    "auto_install": False,
    "application": True,
    "price": "50",
    "currency": "EUR"
}
