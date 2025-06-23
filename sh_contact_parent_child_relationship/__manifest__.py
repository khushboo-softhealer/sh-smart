# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Contact Parent/Child Relationship Management",
    "author": "Amit - Softhealer Technologies",
    "website": "http://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Extra Tools",
    "license": "OPL-1",
	"summary": "Contact Parent/Child Relationship Management",
    "description": """The parent and child relationship for contacts will be managed automatically when creating any new contact in the system
    based on the email domain provided. However, 
    relations will not be managed if the email domain matches any of the common email domain configurations.
    mass actions added for to update relationship for existing contacts which we have in the system""",   
    "version": "16.0.8",
    "depends": [
        "sh_helpdesk",
    ],
    "data": [
        'security/ir.model.access.csv',
        'data/contact_update_mass_action_data.xml',
        'views/res_partner_views.xml',
        'views/sh_common_mail_domains_views.xml',
        'views/config_settings_views.xml',
        'data/ir_cron_data.xml',
    ],
    "application": True,
    "auto_install": False,
    "installable": True,
	"images": ["static/description/background.png",],              
    "price": 10,
    "currency": "EUR"
}
