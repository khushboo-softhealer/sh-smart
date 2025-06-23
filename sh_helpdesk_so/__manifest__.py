# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Manage Sale Order With Helpdesk | Manage Helpdesk With Sale Order",
    "author": "Softhealer Technologies (Kishan Patadiya)",
    "website": "http://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Sales",
    "license": "OPL-1",
	"summary": "Manage Sale Order With Helpdesk Ticket,Helpdesk Ticket With Sale Order,Helpdesk Support Ticket To Sale Order, Manage Helpdesk With Sale Order, Manage Quotation Helpdesk,Ticket from Sale Order,Helpdesk Tickets Sale Order,Manage helpdesk tickets Odoo",
    "description": """If your company provides prepaid support services, meaning that the authorized user accepts responsibility for payment of the charges for use of the company's service. You can do that with this module. This module allows your helpdesk team to generate a quotation/Sale order directly from the helpdesk ticket vice versa they can generate a helpdesk ticket from the Sale order/ quotation. It helps to provide resulting in faster responses to your customer needs. You can easily manage products in tickets and display products in the ticket PDF report.""",   
    "version": "16.0.3",
    "depends": [
        "sale_management",
        "sh_helpdesk",
    ],
    "data": [
        'security/sh_helpdesk_so_groups.xml',
        'views/sale_order_views.xml',
        'views/helpdesk_ticket_views.xml',
        'report/sale_order_report_template.xml',
    ],
    "application": True,
    "auto_install": False,
    "installable": True,
	"images": ["static/description/background.png",],              
    "price": 10,
    "currency": "EUR"
}
