# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Helpdesk Security Groups Category Customisation",
    "author": "Nikhil - Softhealer Technologies",
    "website": "http://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Helpdesk",
    "license": "OPL-1",
	"summary": "Helpdesk Security Groups Category Customisation",
    "description": """We have added one new Group Catageory called Helpdesk management and all other helpdesk related security groups added to this category.""",   
    "version": "16.0.1",
    "depends": [
        "sh_helpdesk",
        "sh_lead_qualification",
        "sh_helpdesk_crm",
        "sh_helpdesk_so",
        "sh_helpdesk_timesheet",
        "sh_helpdesk_invoice",
        "sh_odoo_order_reference_number_management",
        "sh_helpdesk_task"
    ],
    "data": [
        'security/sh_helpdesk_security.xml',
    ],
    "application": True,
    "auto_install": False,
    "installable": True,
	"images": ["static/description/background.png",],              
}
