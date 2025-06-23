# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Manage Invoice With Helpdesk | Manage Helpdesk With Invoice",
    "author": "Softhealer Technologies",
    "website": "http://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Accounting",
    "license": "OPL-1",
	"summary": "Manage Invoice With Helpdesk Ticket,Helpdesk Ticket With Invoice,Helpdesk Support Ticket To Invoice, Manage Helpdesk With Invoices, Manage Invoice Helpdesk,Ticket from Invoice,Helpdesk Tickets Invoice,Manage helpdesk tickets Odoo",
    "description": """If your company provides prepaid support services, meaning that the authorized user accepts responsibility for payment of the charges for use of the company's service. You can do that with this module. This module allows your helpdesk team to generate an invoice directly from the helpdesk ticket vice versa they can generate a helpdesk ticket from the invoice. It helps to provide resulting in faster responses to your customer needs. You can easily manage products in tickets and display products in the ticket PDF report.""",   
    "version": "16.0.1",
    "depends": [
        "account",
        "sh_helpdesk",
    ],
    "data": [
        'security/sh_helpdesk_invoice_security.xml',
        'views/account_move_views.xml',
        'views/helpdesk_tickets_views.xml',
    ],
    "application": True,
    "auto_install": False,
    "installable": True,
	"images": ["static/description/background.png",],              
    "price": 10,
    "currency": "EUR"
}
