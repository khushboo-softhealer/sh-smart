# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Sh Public Holiday",
    
    "author": "Softhealer Technologies",
    
    "website": "https://www.softhealer.com",    
    
    "support": "support@softhealer.com",   

    "version": "16.0.1",

    "license": "OPL-1",
    
    "category": "Extra Tools",
    
    "summary": "Auto assign public holiday ",
        
    "description": """Public Holiday""",
     
    "depends": ['hr','mail','contacts'],
        
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence.xml.xml",
        "views/sh_public_holiday_views.xml",
        "reports/sh_public_holiday_report.xml",
        "reports/public_holiday_mail_template.xml",
    ],

    "installable": True,    
    "auto_install": False,    
    "application": True, 
    "price": "50",
    "currency": "EUR"        
}
