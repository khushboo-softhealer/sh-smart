# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

{
    "name": "Website Sale Popup Pricelist",
    "version": "16.0.3",
    "category": "eCommerce",
    "support": "support@softhealer.com",
    "license": "OPL-1",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "summary": "In website sale show popup of Pricelist when user visit page.",
    "description": """In website sale show popup of Pricelist when user visit page.""",
    "depends": ["website_sale"],
    "data": [
        "views/product_pricelist_views.xml",
        "views/res_config_settings_views.xml",
        "views/website_templates.xml",
        "views/website_sale_templates.xml",
    ],
    'assets': {
        'web.assets_frontend': [
            "sh_website_sale_popup_pricelist/static/src/xml/sh_pricelist_dialog.xml",
            "sh_website_sale_popup_pricelist/static/src/scss/sh_website_sale_popup_pricelist.scss",
            "sh_website_sale_popup_pricelist/static/src/js/sh_pricelist_popup.js",
            "sh_website_sale_popup_pricelist/static/src/js/custom.js",
            ],
    },
    "installable": True,
    "application": True,
    "auto_install": False,
    "price": 50,
    "currency": "EUR"
}
