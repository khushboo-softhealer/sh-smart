# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Mass Update blog Post",

    "author": "Softhealer Technologies - Nayan",

    "website": "https://www.softhealer.com",

    "support": "support@softhealer.com",

    'version': '16.0.1',

    "license": "OPL-1",

    "category": "Extra Tools",

    "summary": "Mass Update blog Post",

    "description": """Mass Update blog Post""",
    "depends": ['website_blog'],

    "data": [
        'security/ir.model.access.csv',
        'wizard/sh_update_tags_blog_wizard_views.xml',
        'views/blog_post_views.xml',
    ],

    "images": ["static/description/background.png", ],

    "installable": True,
    "auto_install": False,
    "application": True,

}
