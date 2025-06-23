# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Website Helpdesk",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Website",
    "summary": "Website Helpdesk, Flexible HelpDesk Module, Customizable Help Desk App, Service Desk, HelpDesk With Stages, Help Desk Ticket Management, Helpdesk Email Templates, Helpdesk Chatter Odoo",
    "description": """Are you looking for a fully flexible and customizable helpdesk on the website? This module will work on a website with a backend. Website customer helpdesk support Ticketing System is used to give the customer an interface where he/she can send support ticket requests and attach documents from the website. Customer can view their ticket from the website portal and easily see the stage of the reported ticket also customers get a link of the portal in email as well. Our this apps almost contain everything you need for Service Desk, Technical Support Team which include service request to be managed in Odoo backend. The support ticket will send by email to the customer and admin. Customer can view their ticket from the website portal and easily see the stage of the reported ticket. This desk is fully customizable clean and flexible. The support ticket will send by email to the customer and admin. for an Online ticketing system for customer support in Odoo Support. Customer can view their ticket from the website portal and easily see the stage of the reported ticket.""",
    "version": "16.0.5",
    "license": "OPL-1",
    "depends": [
        "sh_helpdesk",
        "website",
        # CODE BY KISHAN GHELANI
        "google_recaptcha"
    ],
    "application": True,
    "data": [
        "data/sh_website_helpdesk_menu.xml",
        "data/config_data.xml",
        # "views/website_config_setting_view.xml",
        "views/sh_helpdesk_website_template.xml",
        "views/product_product_views.xml",
    ],

    'assets': {
        'web.assets_frontend': [
            'sh_website_helpdesk/static/src/js/helpdesk_page.js',
            'sh_website_helpdesk/static/src/js/libs/multi-select.selection.js',
            'sh_website_helpdesk/static/src/css/custom.css',
            'sh_website_helpdesk/static/src/scss/helpdesk_page.scss',
        ],
    },

    "images": ["static/description/background.png", ],
    "auto_install": False,
    "installable": True,
    "price": "30",
    "currency": "EUR"
}
