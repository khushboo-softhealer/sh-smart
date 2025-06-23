# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name":
    "Website Terms & Conditions",
    "author":
    "Softhealer Technologies",
    "website":
    "https://www.softhealer.com",
    "support":
    "support@softhealer.com",
    "license":
    "OPL-1",
    "version":
    "16.0.1",
    "category":
    "eCommerce",
    "summary":
    """
set website terms & condition,
website shop terms & condition,
create website shop terms app,
multiple terms & conditions,
multiple terms and conditions,
website terms and condition,
terms and condition odoo
""",
    "description":
    """This module offers to show the terms and conditions on the website. We have options for multiple terms & conditions also. We have the option to tick by default terms and conditions in case if you don't want to customer to tick. You can also show an alert message before the pay button to highlight/attention customers to about terms part. Cheers!""",
    "depends": ["payment","website_sale"],
    "data": [
        'security/ir.model.access.csv',
        'views/sh_website_tnc_views.xml',
        'views/res_config_settings_views.xml',
        'views/payment_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'sh_website_tnc/static/src/js/sh_website_tnc.js',
            # 'sh_website_tnc/static/src/js/website_delivery.js'
        ]
    },
    "images": [
        "static/description/background.png",
    ],
    "auto_install":
    False,
    "application":
    True,
    "installable":
    True,
    "price":
    15,
    "currency":
    "EUR"
}
