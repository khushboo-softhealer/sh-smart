# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Manage CRM With Helpdesk | Manage Helpdesk With CRM | Helpdesk Tickets With Leads | Leads With Helpdesk Tickets",
    "author": "Softhealer Technologies (Kishan Patadiya)",
    "website": "http://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Discuss",
    "license": "OPL-1",
	"summary": "Lead With Helpdesk,Helpdesk With Lead,Opportunity To Helpdesk,Helpdesk To Opportunity, Manage Helpdesk With Leads, Manage Lead Helpdesk,Ticket from CRM,Ticket From Lead,Ticket From Opportunity,Manage helpdesk tickets Odoo",
    "description": """If your company provides prepaid support services, meaning that the authorized user accepts responsibility for payment of the charges for use of the company's service. You can do that with this module. This module allows your helpdesk team to generate an lead/opportunity directly from the helpdesk ticket vice versa they can generate a helpdesk ticket from the lead/opportunity. It helps to provide resulting in faster responses to your customer needs. You can easily manage products in tickets and display products in the ticket PDF report.""",   
    "version": "16.0.4",
    "depends": [
        "crm",
        "sh_helpdesk",
    ],
    "data": [
        'security/sh_helpdesk_crm_groups.xml',
        "security/ir.model.access.csv",
        "views/crm_lead_views.xml",
        "views/helpdesk_ticket_views.xml",
    ],
    "application": True,
    "auto_install": False,
    "installable": True,
	"images": ["static/description/background.png",],              
    "price": 10,
    "currency": "EUR"  
}
