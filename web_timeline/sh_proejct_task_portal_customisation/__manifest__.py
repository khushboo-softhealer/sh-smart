# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Project & Task Portal",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Extra Tools",
    "summary": "",
    "description": """""",
    "version": "16.0.2",
    "depends": ["project","sale_project", "hr_timesheet","sh_github_connector"],
    "application": True,
    "data": [
        'views/res_users_views.xml',
        'views/project_task_sharing_views.xml',
        'views/hr_timesheet_portal_templates.xml',
        'views/project_task_portal_templates.xml',
    ],
    'assets': {
        'project.webclient': [
            'sh_proejct_task_portal_customisation/static/src/js/custom_filter.js',
            'sh_proejct_task_portal_customisation/static/src/js/custom_group_by.js',
        ],
    },
    "license": "OPL-1",
    "auto_install": False,
    "installable": True,
}
