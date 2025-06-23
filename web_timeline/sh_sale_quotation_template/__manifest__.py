# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Quotation Template For Sale Order",
    
    "author": "Softhealer Technologies",

    "website": "https://www.softhealer.com",

    "support": "support@softhealer.com",

    "category": "Sales",

    "license": "OPL-1",
    
    "summary": "Sale Quotation Templates Reusable Template Create Template Button Create Quotation Template Quotation Templates Order Detail Management Quotation templates so Quotation template odoo quotations custom template make template of quote sales product template module Sale Order Templates Sales Order Template Sales Template Sale Order Product Templates Sales Order Product Template Sales Product Template Sale Template Sale Product Template Odoo",

    "description": """Quotation on a single click in the sale order. 
    How exactly does it work, First need to create a custom 
    quotation template and add a different kind of product to that, 
    you need to select that quotation template in the sale order and 
    auto all related details will be added in the sale order. 
    you have done! it will make your effort very less otherwise you 
    need to add all the details one by one in the sale order. 
    It will reduce manual data entry for frequently sold products.""",

    "version": "16.0.1",

    "depends": [
                "sale_management",
                ],
    "application": True,
    "data": [
        "security/ir.model.access.csv",
        'views/sale_order_views.xml',
        "wizard/sh_sale_quotation_cancel_wizard.xml",
        "views/sh_sale_order_cancel_views.xml",
        "views/sale_order_template_views.xml"  
        ],
    "images": ["static/description/background.png", ],

    "installable": True,

    "auto_install": False,

    "application": True,

    "price": 25,
    
    "currency": "EUR"
}