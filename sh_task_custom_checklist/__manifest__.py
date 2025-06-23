# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Task Own Checklist",
    "author": "Softhealer Technologies - Nayan",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    'version': '16.0.1',
    "license": "OPL-1",
    "category": "Project",
    "summary": "list of work reminder app, subtask checklist module, list of incomplete work odoo, remember of important things, task checklist",
    "description": """   
list of work reminder app, subtask checklist module, list of incomplete work odoo, remember of important things, task checklist	""",
    "depends": ['project', 'sh_task_subtasks_checklist', 'sh_message'],
    "data": [
        'security/ir.model.access.csv',
        'wizard/sh_update_state_wizard_views.xml',
        'wizard/sh_add_checklist_wizard_views.xml',
        'data/sh_task_custom_checklist_action.xml',
        # views
        'views/task_custom_checklist_line_views.xml',
        'views/project_task_views.xml',
        'views/sh_checklist_state_views.xml',
        'views/sh_task_custom_checklist_views.xml',
        'views/sh_task_checklist_template_views.xml',
        'views/sh_project_task_checklist_views.xml',
        'views/sh_task_custom_checklist_menus.xml',
    ],
    "images": [
        "static/description/background.png",
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
    "price": "20",
    "currency": "EUR",
}
