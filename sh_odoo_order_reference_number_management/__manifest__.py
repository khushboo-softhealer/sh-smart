# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Odoo order reference number management",
    "author": "Amit - Softhealer Technologies",
    "website": "http://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Helpdesk",
    "license": "OPL-1",
	"summary": "Order Reference Management",
    "description": """Order Reference Management like getting the past order details and current as well based on Order reference 
    or Ticket partner and it's parent or child""",   
    "version": "16.0.16",
    "depends": [
        "sh_helpdesk",
        "sh_sol_views"
    ],
    "data": [
        'security/odoo_app_details_security.xml',
        'views/helpdesk_ticket_views.xml',
        'views/sale_order_views.xml',
        'data/update_order_information_action.xml',
    ],
    "application": True,
    "auto_install": False,
    "installable": True,
	"images": ["static/description/background.png",],              
}
