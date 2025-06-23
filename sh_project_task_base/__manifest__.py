# Part of Softhealer Technologies.

{
    'name': 'Project Task Base',
    'version': '16.0.1',
    'category': 'Human Resources',
    "license": "OPL-1",
    "author": "Softhealer Technologies (Kishan Patadiya)",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    'summary': "",
    'description': """""",
    'depends': ['project', 'website_sale', 'sh_product_base', 'hr_timesheet', 'sh_project_stages', 'sh_training', 'sh_message'],
    'data': [
        'security/project_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'wizard/sh_mass_update_task_wizard_views.xml',
        'wizard/sh_not_billable_reason_wizard_views.xml',
        'views/sh_cr_state_views.xml',
        'views/sh_task_upcoming_feature.xml',
        'data/sh_project_task_base_actions.xml',
        'views/project_task_views.xml',
        "views/project_project_views.xml",
        "views/res_company_views.xml",
        "views/res_config_settings_views.xml",
        "views/sh_project_stage_template.xml",
        "views/sh_project_project_stage_template_views.xml",
        "views/sh_project_task_type_views.xml",
        "views/sh_account_analytic_line_views.xml",
        "views/project_task_type_views.xml",
        "views/sh_project_task_base_menus.xml",
    ],
    
    'assets': {
        'web.assets_backend': [
            'sh_project_task_base/static/src/js/wizard_template.xml',
            'sh_project_task_base/static/src/js/widget_open_wizard.js',
        ]
    },
    'installable': True,
    'auto_install': False,
    "images": ["static/description/background.png", ],
    "live_test_url": "https://youtu.be/uWtmf_nHkdE",
    'application': True,
}
