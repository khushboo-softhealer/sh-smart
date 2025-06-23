# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Helpdesk Support Ticket To Task",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "version": "16.0.1",
    "category": "Discuss",
    "summary": "Helpdesk Ticket To Task Module, HelpDesk Task add-on,Help Desk Tasks App, Service Desk, HelpDesk With Tasks, Help Desk Ticket Management, Helpdesk Support, Helpdesk Tickets To Tasks Odoo",
    "description": """This module useful to create a task from a helpdesk support ticket, you can easily manage odoo tasks with a ticket. This module easily moves information, attachment, etc of the ticket to the task, Task is very useful in the case where you have multiple users who going to manage different actions based on tickets raised by customers.""",
    "depends": [
        'sh_helpdesk',
        'project',
    ],
    "data": [
        'security/sh_helpdesk_task_groups.xml',
        'views/helpdesk_ticket_views.xml',
        'views/project_task_views.xml',
    ],
    "images": ["static/description/background.png", ],
    "license": "OPL-1",
    "installable": True,
    "auto_install": False,
    "application": True,
    "price": "15",
    "currency": "EUR"
}
