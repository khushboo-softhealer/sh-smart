# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

{
    "name": "Sh Employee Ot",
    
    "author": "Softhealer Technologies",
    
    "website": "https://www.softhealer.com",    
    
    "support": "support@softhealer.com",   

    "version": "16.0.1",

    "license": "OPL-1",
    
    "category": "Extra Tools",
    
    "summary": "Employee Overtime management app ",
        
    "description": """Public Holiday""",
     
    "depends": ['hr','account','sh_payslip_cancel','sh_project_task_base','sh_hr_dashboard'],
        
    "data": [
        "security/ir.model.access.csv",
        "views/sh_res_setting.xml",
        "security/ir_rule.xml",
        "data/ir_sequence.xml",
        "data/sh_ot_salary_rule.xml",
        "views/sh_employee_ot_views.xml",
    ],

    "installable": True,    
    "auto_install": False,    
    "application": True, 
    "price": "50",
    "currency": "EUR"        
}
