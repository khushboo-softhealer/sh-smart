# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    "name": "Website Sale Softhealer",
    'author': 'Softhealer Technologies - Sagar',
    'website': 'https://www.softhealer.com',
    "support": "support@softhealer.com",
    'version': '16.0.1',
    "license": "OPL-1",
    'category': "website",
    'summary': "",
    'description': """
    """,
    "depends": ['sh_product_base','sh_helpdesk'],
    "data": [
        "views/product_detail_tabs_tmpl.xml",
        "views/product_detail_buttons_tmpl.xml",
        "views/website_sale_templates.xml",
    ],
    'assets': {
        'web.assets_frontend': [
            'sh_ecommerce/static/src/xml/support_diaload_box_template.xml',
            'sh_ecommerce/static/src/js/custom.js',
            'sh_ecommerce/static/src/scss/style.scss',
        ],
    },
    "installable": True,
    "application": True,
    "autoinstall": False,
}
