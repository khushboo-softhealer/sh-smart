# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Backmate Backend Theme Basics- Compatibility With Frontend",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "license": "OPL-1",
    "category": "Extra Tools",
    "summary": "Material Backend Multi Tab Responsive fully functional Backend Theme flexible Backend Theme fast Backend Theme lightweight Backend Theme animated Backend Theme modern multipurpose theme Login Style With Website Login Page Login Theme For Website Odoo",
    "description": """Are you bored with your standard odoo backend theme? Are You are looking for modern, creative, clean, clear, materialize Odoo theme for your backend? So you are at right place, We have made sure that this theme is highly customizable and it comes with a premium look and feel. Our theme is not only beautifully designed but also fully functional, flexible, fast, lightweight, animated and modern multipurpose theme. Our backend theme is suitable for almost every purpose.""",
    "version": "16.0.1",
    "depends":
    [
        "sh_backmate_theme", "website"
    ],

    "data":
    [
       "views/login_layout.xml"
    ],
     'assets': {
          'web.assets_frontend': [
            'sh_backmate_theme_website_login/static/src/scss/login_page/login_style.scss',
        ],
  
    },
    "live_test_url": "https://softhealer.com/contact_us",
    "installable": True,
    "application": True,
    "images": ["static/description/background.png", ],
    "price": 10,
    "currency": "EUR",
    "bootstrap": True,

}
