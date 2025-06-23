# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Hide/Show Follower Button",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Mail",
    "summary": "We can hide/show the follow/unfollow button based on the user security group",
    "description": """We can hide/show the follow/unfollow button based on the user security group""",
    "version": "16.0.1",
    "depends": ["mail"],
    "license": "OPL-1",
    "application": True,
    "data": [
        'security/security.xml'
    ],
    'assets': {
    'web.assets_backend': [
        '/sh_hide_follow_button/static/src/js/follow_button.js',
        '/sh_hide_follow_button/static/src/xml/follow_button.xml',
        '/sh_hide_follow_button/static/src/js/follower_list_menu.js',
        '/sh_hide_follow_button/static/src/xml/follower_list_menu.xml',
    ],
},
    "images": ["static/description/background.png", ],
    "auto_install": False,
    "installable": True,
}
