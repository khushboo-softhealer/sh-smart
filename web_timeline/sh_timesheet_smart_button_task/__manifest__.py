# -*- coding: utf-8 -*-
# Part of Softhealer Technology

{
    "name": "Task Timesheet By Smart Button",
    "author": "Softhealer Technologies-Krupali",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "version": "16.0.1",
    "license": "OPL-1",
    "category": "Project",
    "summary": "Smart Button In Timesheet Smart Task Timesheet Open Timesheet By Smart Button Timesheet Record By Smart Button Quick Timesheet View Project Smart Timesheet Spent Hours In Task Spent Time In Task Project Total Hours Task Total Hours Odoo",
    "description": """This module shows the hours spent on each project task & sub-tasks. Each task & subtask contains a timesheet smart button that shows how much time is spent on the task. So you can manage the timesheet and accurate the time management for the project.""",
    'depends': ['project', 'hr_timesheet'],
    'data': [
        'views/project_task_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    "images": ["static/description/background.png", ],
    "license": "OPL-1",
    "price": "15",
    "currency": "EUR"
}
