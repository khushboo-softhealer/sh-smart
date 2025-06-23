# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Odoo Backend Branding | Odoo Backend Debranding",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Extra Tools",
    "license": "OPL-1",
    "summary": "Hide Odoo From Website Remove Odoo From Login Page Replace Odoo Bot Replace Odoo Image Replace Odoo From Chatter Replace Odoo From Everywhere In Website Odoo Backend Debranding Odoo Branding Delete Odoo",
    "description": """"Odoo Backend Debranding" module helps to enhance your brand. Odoo Debranding plays an important role. This module removes odoo references to customize company details. It hides odoo and promotes your organization. Hurray!""",
    "version": "16.0.1",
    "depends": ["sh_base_debranding", "mail", "portal"],
    "application": True,
    "data": [
        "views/fevicon.xml",
        "views/mail_template_views.xml",
        "views/res_config_setting_views.xml",
    ],
    'assets': {

        'web.assets_backend': [
            'sh_backend_debranding/static/src/js/system_name.js',
            'sh_backend_debranding/static/src/js/error.js',
            'sh_backend_debranding/static/src/js/dialogue.js',
            'sh_backend_debranding/static/src/js/customize_user.js',
            # 'sh_backend_debranding/static/src/js/avatar.js',
            'sh_backend_debranding/static/src/xml/**/*',
        ],
    },

    "images": ["static/description/background.png", ],
    "auto_install": False,
    "installable": True,
    "price": 70,
    "currency": "EUR"
}
