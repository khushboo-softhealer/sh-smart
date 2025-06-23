# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name":"Employee Onboarding",
    "author":"Softhealer Technologies",
    "website":"https://www.softhealer.com",
    "support":"info@softhealer.com",
    "version":"16.0.1",
    "license": "OPL-1",
    "category":"Extra Tools",
    "summary":"HR Onboarding",
    "description":
    """
    
Employee Onboarding    
    
""",
    "depends": ['base', 'hr_contract','sh_hr_dashboard', 
                'sh_hr_payroll','sh_employee_extra_fields',
                  'sh_push_notification_tile','sh_user_group_allocation_hide_menu'],
    "data": [
        'data/mail_template.xml',
        "security/onboarding_security.xml",
        'security/ir.model.access.csv',
        'views/hr_onboarding_views.xml',
    ],
    "installable":True,
    "application":True,
    "auto_install":False,
}
