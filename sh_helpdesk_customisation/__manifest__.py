# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Helpdesk Customisation",
    "author": "Softhealer Technologies",
    "website": "http://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Accounting",
    "license": "OPL-1",
	"summary": "Helpdesk Customisation",
    "description": """Helpdesk Customisation.""",   
    "version": "16.0.8",
    "depends": [
        "sh_helpdesk",
    ],
    "data": [
        'security/sh_helpdesk_security.xml',
        'security/ir.model.access.csv',
        'data/update_edition_details_in_ticket.xml',
        'wizard/sh_add_user_to_task_views.xml',
        'views/sh_helpdesk_ticket_view.xml',
        'views/helpdesk_stages_views.xml',
    ],
    "application": True,
    "auto_install": False,
    "installable": True,
	"images": ["static/description/background.png",],              
    "price": 10,
    "currency": "EUR"
}
