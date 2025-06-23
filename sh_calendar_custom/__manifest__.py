# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Calendar Event",
    "author": "Softhealer Technologies(NIRALI DHOLARIA)",
    "license": "LGPL-3",
    "website": "https://www.softhealer.com",
    "support": "info@softhealer.com",
    "category": "Calendar",
    "summary": "Calendar Event",
    "description": """Calendar Event""",
    "version": "16.0.1",
    "depends": [
        "calendar",
        "sh_project_task_base",
        "sh_push_notification_tile",
        "note",
        "resource",
    ],
    "application": True,
    "data": [
        "security/ir.model.access.csv",

        "views/calendar_event_views.xml",
        "views/sh_calendar_group_template_views.xml",
    ],
    "auto_install": False,
    "installable": True,
    "price": 50,
    "currency": "EUR"
}
