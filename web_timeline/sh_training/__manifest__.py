# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    "name": "Softhealer Trainning",
    'author': 'Softhealer Technologies',
    'website': 'https://www.softhealer.com',
    "support": "support@softhealer.com",
    'version': '16.0.1',
    "license": "OPL-1",
    'category': "Warehouse",
    'summary': "Softhealer Trainning",
    'description': """
    
    Softhealer Trainning
    
    """,
    "depends": ['project', 'hr_timesheet'],
    "data": [
        'security/sh_training_security.xml',
        'security/ir.model.access.csv',
        'data/ir_cron.xml',
        'views/sh_training_master_views.xml',
        'views/sh_training_course_views.xml',
        'views/sh_pre_define_task_line_views.xml',
        'views/sh_training_batch_views.xml',
        'views/project_task_views.xml',
        'views/res_config_settings_views.xml',
        'wizard/sh_generate_task_wizard_views.xml',
    ],
    "installable": True,
    "application": True,
    "autoinstall": False,
}
