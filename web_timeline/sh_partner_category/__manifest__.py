# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Partner By Category",

    "author": "Softhealer Technologies-Mayur",

    "website": "https://www.softhealer.com",

    "support": "support@softhealer.com",

    'version': '16.0.1',

    "license": "OPL-1",

    "category": "Extra Tools",

    "summary": "Vendor Plans, Vendor Packages, Vendor By Plans, Vendor By Packages, Partner Plans, Partner Packages, Partner By Plans, Partner By Packages, partner management Odoo",

    "description": """This module is useful to define partner by category. We have made one new menu for partners and by default kanban and list view category wise, You can mass email to customers and vendors category wise. This module is also very useful where different packages or plans are there. So you can make different plans in category and very easily filter or group by customers or vendors by plans or packages.Customer Plans, Customer Packages, Customer By Plans, Customer By Packages, Partner Plans, Partner Packages, Partner By Plans, Partner By Packages.
Vendor Plans, Vendor Packages, Vendor By Plans, Vendor By Packages, Partner Plans, Partner Packages, Partner By Plans, Partner By Packages.""",
    "depends": ['contacts', 'sale_management', 'purchase'],

    "data": [
        'security/partner_category_security.xml',
        'security/ir.model.access.csv',
        'wizard/sh_mass_update_partner_category_wizard.xml',
        'views/res_config_settings.xml',
        'views/partner_category.xml',
        'views/mass_auto_assign_partner_category.xml',
        'views/mass_update_partner_category.xml',
        'views/sale_order_inherit.xml'
    ],

    "images": ["static/description/background.png", ],

    "installable": True,
    "auto_install": False,
    "application": True,

    "price": "20",
    "currency": "EUR"
}
