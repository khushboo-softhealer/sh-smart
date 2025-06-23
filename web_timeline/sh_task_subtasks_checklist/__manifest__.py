# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Task Subtasks Checklist",
    "author": "Softhealer Technologies - Nayan",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Project",
    "license": "OPL-1",
    "summary": """ 
 Task-Subtask checklist, Manage Project Subtask Module, Create Subtask App, Analysis Of Subtask, Project Task Management, Control Task Subtask Progress Odoo
""",
    "description": """Do you want to divide the project task and subtask into stages? currently, in odoo, you can't manage the sub-task of the project. The checklist used to give an important list of items, things to be done, or points to be considered, used as a reminder.This module helps to divide sub-tasks into different stages like Draft, Done & Cancel. so, you can easily control task and sub-task progress. you can easily analyze the large project. Here if sub-tasks are remaining then you can't done parent task.
 Task-Subtask checklist Odoo
 Manage Project Subtask Module, Create Subtask, Analysis Of Subtask, Project Task Management, Reminder Of Subtask, Control Task Subtask Progress Odoo
 Manage Project Subtask Module, Create Subtask App, Analysis Of Subtask, Project Task Management, Control Task Subtask Progress, Reminder Of Subtask Odoo

""",

    "version": "16.0.1",

    "depends": ['base', 'project', 'sh_project_task_base'],

    "data": [
        "views/project_task_type_views.xml",
        "views/project_task_views.xml",
    ],

    "images": ['static/description/background.png', ],
    "live_test_url": "https://youtu.be/uriRmHN62l4",
    "auto_install": False,
    "application": True,
    "installable": True,
    "price": 35,
    "currency": "EUR"
}
