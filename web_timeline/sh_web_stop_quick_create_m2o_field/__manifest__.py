# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Restrict Quick Creation/Edition Many2one Field",
    "author": "Softhealer Technologies",
    "license": "OPL-1",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "version": "16.0.1",
    "category": "Extra Tools",
    "summary": """disable product creation disable create product option Restriction on product creation Restriction on quick product creation Hide Product creation option Restrict Product creation in inventory Restrict Product creation in invoice Restrict Product creation in invoicing Restrict product creation on order line Block quick product creation Block product creation disable quick creation of product Restrict Product Creation Restrict Product Edition Restrict Product Create User Restriction For Creating Product Disable Quick Product Creation Disable Quick Product Edition Restrict Product Creation in sales Restrict Product Creation in purchase All In One Restrict Product Quick Creation All In One Restrict Product Quick Edition Sale Order Restrict Product Create Sale Order Restrict Product Edit Purchase Order Restrict Product Create Purchase Order Restrict Product Edit Invoice Restrict Product Create Invoice Restrict Product Edit Inventory Restrict Product Create Inventory Restrict Product Edit Restrict Product Update Odoo disable product variant creation disable create product variant option Restriction on product variant creation Restriction on quick product variant creation Hide product variant creation option Restrict product variant creation in inventory Restrict product variant creation in invoice Restrict product variant creation in invoicing Restrict product variant creation on order line Block quick product variant creation Block product variant creation disable quick creation of product variant Restrict product variant Creation Restrict product variant Edition Restrict product variant Create User Restriction For Creating product variant Disable Quick product variant Creation Disable Quick product variant Edition Restrict product variant Creation in sales Restrict product variant Creation in purchase All In One Restrict product variant Quick Creation All In One Restrict product variant Quick Edition Sale Order Restrict product variant Create Sale Order Restrict product variant Edit Purchase Order Restrict product variant Create Purchase Order Restrict product variant Edit Invoice Restrict product variant Create Invoice Restrict product variant Edit Inventory Restrict product variant Create Inventory Restrict product variant Edit Restrict product variant Update Odoo disable customer creation disable create customer option Restriction on customer creation Restriction on quick customer creation Hide customer creation option Restrict customer creation in inventory Restrict customer creation in invoice Restrict customer creation in invoicing Restrict customer creation on order line Block quick customer creation Block customer creation disable quick creation of customer Restrict customer Creation Restrict customer Edition Restrict customer Create User Restriction For Creating customer Disable Quick customer Creation Disable Quick customer Edition Restrict customer Creation in sales Restrict customer Creation in purchase All In One Restrict customer Quick Creation All In One Restrict customer Quick Edition Sale Order Restrict customer Create Sale Order Restrict customer Edit Purchase Order Restrict customer Create Purchase Order Restrict customer Edit Invoice Restrict customer Create Invoice Restrict customer Edit Inventory Restrict customer Create Inventory Restrict customer Edit Restrict customer Update Odoo disable products creation disable products edition disable products variants creation disable products variants edition disable customers creation disable customers edition""",
    "description": """You can restrict the quick create any model from the whole odoo. One of the attractive features of Odoo is the ability to create products from sale order lines, invoice lines, and other places. However, sometimes users can create incorrect products or customers accidentally. With the help of this module, you can restrict these types of actions for particular users. Restricting access to product and customer creation can help prevent mistakes and maintain data integrity.""",
    "depends": ["base_setup"],
    "data": [
        "security/sh_stop_quick_create_security.xml",
        "views/res_config_settings_views.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'sh_web_stop_quick_create_m2o_field/static/src/js/relations_fields.js',
        ],
    },
    "images": ["static/description/background.png", ],
    "installable": True,
    "auto_install": False,
    "application": True,
    "price": 70,
    "currency": "EUR"
}
