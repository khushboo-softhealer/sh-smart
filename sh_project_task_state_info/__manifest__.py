# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Project Stage Change History",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "version": "16.0.1",
    "category": "Project",
    "license": "OPL-1",
    "summary": "Project History Project State Change History Projects History Project Stages History Project Task History Project Status History Change Stage History Stage Analysis Odoo",
    "description": """This module helps to display project stage history. You can find who has moved stage and when. We provide stage change analysis menu where you can see all stages history with details.""",
    'depends': ['project', 'sh_project_task_base'],
    'data': [
        "security/ir.model.access.csv",
        "security/security_groups.xml",
        "data/sh_project_task_state_info_actions.xml",
        "views/project_task_views.xml",
        "views/sh_project_task_info_views.xml"
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    "images": ["static/description/background.png"]
}
