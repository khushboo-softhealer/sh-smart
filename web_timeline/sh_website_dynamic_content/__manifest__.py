# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

{
    "name": "Website Dynamic Content",
    "author": "Softhealer Technologies",
    "license": "OPL-1",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Website/Website",
    "sequence": 1,
    "summary": "Website Dynamic Content",
    "description": """Website Dynamic Content""",
    "version": "16.0.1",
    "depends": ['website'],
    "installable": True,
    "data": [
        # security.xml first, data.xml need the group to exist (checking it)
        "security/ir.model.access.csv",
        "views/sh_website_dynamic_content_views.xml",
        "views/snippets/s_sh_dynamic_content.xml",
        "views/snippets/snippets.xml",
    ],
    'assets': {
        'website.assets_wysiwyg': [
            "sh_website_dynamic_content/static/src/snippets/s_sh_dynamic_content/options.js"
        ],
        'web.assets_frontend': [
            "sh_website_dynamic_content/static/src/snippets/s_sh_dynamic_content/s_sh_dynamic_content.xml",
            "sh_website_dynamic_content/static/src/snippets/s_sh_dynamic_content/s_sh_dynamic_content.js"
        ]
    },
    "application": True,
    "auto_install": False,
    "price": 50,
    "currency": "EUR",
}
