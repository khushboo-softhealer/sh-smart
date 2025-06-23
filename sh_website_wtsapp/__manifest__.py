# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "WhatsApp Live Chat",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Website",
    "license": "OPL-1",
    "summary": """
whatsapp live chat app,Customer Whatsapp, 
whatsup live chat, whatsup chat Odoo
whatsapp chat by odoo website, client whatsup chat module
""",
    "description": """
Chat with your customers through WhatsApp, the most popular messaging app.
Vital extension for your odoo website,
which allows you to create stronger relationships with your
customers by guiding and advising them in their purchases in real time.
Now your customers can chat with you at WhatsApp,
directly from your odoo website to the mobile!!
No need to add your mobile phone number to the mobile address book.
An online chat system provides customers immediate access to help.
Wait times are often much less than a call center,
and customers can easily multi-task while waiting.
This extension allows you to create a WhatsApp chat button,
highly configurable,
to show it in different parts of your site to chat
with your customers through WhatsApp, the most popular messaging app.    
""",
    "version": "16.0.2",
    "depends": ["website", "portal"],
    "application": True,
    "data": [
        "data/res_config_settings_data.xml",
        "views/sh_website_wtsapp_templates.xml",
        "views/res_config_settings_views.xml",
        "views/website_views.xml",
    ],
    'assets': {
        'web.assets_frontend': [
            'sh_website_wtsapp/static/src/js/detect_mobile.js',
            'sh_website_wtsapp/static/src/css/sh_website_wtsapp.css'
        ],
    },
    "images": ["static/description/background.png", ],
    "auto_install": False,
    "installable": True,
    "price": 25,
    "currency": "EUR"
}
