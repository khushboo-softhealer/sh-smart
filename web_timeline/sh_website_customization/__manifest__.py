# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies

{
    "name": "Website Customization",
    "author": "Softhealer Technologies",
    "license": "OPL-1",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Extra Tools",
    "summary": "",
    "description": """""",
    "version": "16.0.3",
    "depends": ["website_sale"],
    "installable": True,
    "data": [
        "views/website_sale_templates.xml",
        "views/sale_view.xml"
    ],
    'assets': {
        'web.assets_frontend': [
            "sh_website_customization/static/src/js/website_sale.js"
        ]
    },
    "application": True,
    "auto_install": False,
    "price": 50,
    "currency": "EUR",
}
