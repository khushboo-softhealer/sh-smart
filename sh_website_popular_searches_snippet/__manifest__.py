# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

{
    "name": "Website Popular Searches",
    "author": "Softhealer Technologies",
    "license": "OPL-1",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Website/Website",
    "sequence": 1,
    "summary": "Website Popular Searches",
    "description": """Website Popular Searches""",
    "version": "16.0.1",
    "depends": ['website'],
    "installable": True,
    "data": [
        # security.xml first
        "security/ir.model.access.csv",

        "views/res_config_settings_views.xml",
        "views/sh_website_popular_searches_views.xml",
        "views/snippets/s_sh_website_popular_searches.xml",
        "views/snippets/snippets.xml",
    ],
    'assets': {
        'web.assets_frontend': [
            'sh_website_popular_searches_snippet/static/src/snippets/s_sh_website_popular_searches/s_sh_popular_searches.xml',
            'sh_website_popular_searches_snippet/static/src/snippets/s_sh_website_popular_searches/s_sh_popular_searches.js',
        ]
    },
    "application": True,
    "auto_install": False,
    "price": 50,
    "currency": "EUR",
}
