# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name":"Hr Contract",
    "author":"Softhealer Technologies - Nayan",
    "website":"https://www.softhealer.com",
    "support":"info@softhealer.com",
    "version":"16.0.1",
    "license": "OPL-1",
    "category":"Extra Tools",
    "summary":"Hr Contract Description",
    "description":
    """
    
    Add configuration for Annexure - B,add contract details,signature,salary structure,Annexure - B,improvements,goals in contracts,Add Buttons send contract by email,send confirmation by email in contracts for send email,print contract report and confirmation report in contracts,
    
    
""",
    "depends": ['base', 'hr_contract','hr_holidays_attendance', 'sh_employee_extra_fields', 'sh_push_notification_tile','sh_leave_custom'],
    "data": [
        'security/ir.model.access.csv',
        'report/hr_contract_templates.xml',
        'data/mail_template_data.xml',
        'wizard/sh_renew_contract_view.xml',
        'views/hr_contract_views.xml',
        'views/res_config_settings_views.xml',
        'views/hr_employee_views.xml',
    ],
    "installable":True,
    "application":True,
    "auto_install":False,
}
