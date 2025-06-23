# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Lead Qualification",
    "author": "Amit - Softhealer Technologies",
    "website": "http://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Contact",
    "license": "OPL-1",
	"summary": "Manage Customer Qualification Data",
    "description": """Manage Customer Qualification Data Like Google Reviews, Company Strength, Company Address etc.""",   
    "version": "16.0.8",
    "depends": [
        "sh_helpdesk",
    ],
    "data": [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/sh_helpdesk_ticket_views.xml',
        'views/res_country_views.xml',
        'views/sh_type_of_industry_views.xml',
        'views/res_partner_views.xml',
    ],
    "application": True,
    "auto_install": False,
    "installable": True,
	"images": ["static/description/background.png",],              
    "price": 10,
    "currency": "EUR"
}