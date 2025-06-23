# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Base Debranding",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Extra Tools",
    "license": "OPL-1",
    "summary": "Hide Odoo From Website Remove Odoo From Login Page Replace Odoo Bot Replace Odoo Image Replace Odoo From Chatter Replace Odoo From Everywhere In Website Odoo Backend Debranding Odoo Branding Delete Odoo",
    "description": """"Odoo Backend Debranding" module helps to enhance your brand. Odoo Debranding plays an important role. This module removes odoo references to customize company details. It hides odoo and promotes your organization. Hurray!""",
    "version": "16.0.1",
    "depends": ["base_setup", "web", "mail"],
    "application": True,
    "data": [
            "security/sh_debrand_rules.xml",
            "security/ir.model.access.csv",
            "data/sh_configuraion_data.xml",
            "views/menu_management_views.xml",
            "views/webclient_template.xml",
    ],
    "images": ["static/description/background.png", ],
    "auto_install": False,
    'post_init_hook': 'post_init_hook',
    "installable": True,
}
