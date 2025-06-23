# Part of Softhealer Technologies.
# Copyright (C) Softhealer Technologies.
{
    'name': 'Push Modules Details in Project Task',
    'version': '16.0.1',
    'category': 'Project',
    "license": "OPL-1",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    'summary': "",
    'description': """""",
    'depends': ['project','sh_task_subtasks_checklist',],
    'data': [
        'security/ir.model.access.csv',
        "views/sh_push_module_views.xml",
        'views/project_task_views.xml',
    ],
    'assets': {

    },
    'installable': True,
    'auto_install': False,
    "images": ["static/description/background.png", ],
    'application': True,
}
