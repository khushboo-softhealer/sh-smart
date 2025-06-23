# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "All In One Hide Feature",
    "author": "Softhealer Technologies(Nirali Dholaria)",
    "website": "https://www.softhealer.com",
    "category": "Extra Tools",
    "license": "OPL-1",
    "support": "support@softhealer.com",
    "summary": "Invisible create Button, Delete duplicate Button, Hide Action Button,Hide Duplicate Button ,Hide Edit Button, Disable Action Button, Hide Export Button,Hide Create Button,Hide Delete Button,Remove Action Button Odoo",
    "description": """Do you want to hide/show the create button? Do you want to hide/show the edit button? Do you want to hide/show the duplicate action button? Do you want to hide/show the export action button? Do you want to hide/show the delete action button? This module will help you to hide & show the buttons for a particular user. That's it. cheers!""",
    "version": "16.0.1",
    "depends": ["web", "account"],
    "application": True,
    "data": [
        'security/base_security.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sh_hide_feature/static/src/js/sh_hide_button.js',
            'sh_hide_feature/static/src/webclient/action_menus.js',
            "sh_hide_feature/static/src/xml/base.xml",
        ],
    },

    "images": ["static/description/background.png", ],
    "auto_install": False,
    "installable": True,
    "price": 30,
    "currency": "EUR"
}
