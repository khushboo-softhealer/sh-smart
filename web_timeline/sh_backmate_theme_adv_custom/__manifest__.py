# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Backmate Backend Theme Advance",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "description": """
                Are you bored with your standard odoo backend theme? Are You are looking for modern, creative, clean, clear, materialize Odoo theme for your backend? So you are at right place, We have made sure that this theme is highly customizable and it comes with a premium look and feel. Our theme is not only beautifully designed but also fully functional, flexible, fast, lightweight, animated and modern multipurpose theme. Our backend theme is suitable for almost every purpose.
                """,
    "summary": "Advance Material Backend Theme, Responsive Theme, Fully functional Theme, flexible Backend Theme, fast Backend Theme, lightweight Backend Theme, Animated Backend Theme, Modern multipurpose theme, Customizable Backend Theme, Multi Tab Backend Theme Odoo",
    "category": "Themes/Backend",
    "version": "16.0.3",
    "depends":
    [
        "web", "mail" , "sh_backmate_theme_adv"
    ],

    "data":
    [
        "views/assets.xml",
        
    ],
     'assets': {
       
        'web.assets_backend': [
            'sh_backmate_theme_adv_custom/static/src/scss/frontend.scss',
            'sh_backmate_theme_adv_custom/static/src/scss/theme.scss',
            'sh_backmate_theme_adv_custom/static/src/scss/style.css',

        ],
      
       
    },
 
    'images': [
        'static/description/splash-screen.png',
        'static/description/splash-screen_screenshot.gif'
    ],
    "live_test_url": "https://softhealer.com/support?ticket_type=demo_request",
    "installable": True,
    "application": True,
    "price": 125,
    "currency": "EUR",
    "bootstrap": True,
    "license": "OPL-1",

}
