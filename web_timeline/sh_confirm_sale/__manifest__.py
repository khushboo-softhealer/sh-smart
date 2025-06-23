# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Confirm Sale",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Extra Tools",
    "summary": "",
    "description": """""",
    "version": "16.0.1",
    "depends": ["sale", "account"],
    "application": True,
    "data": [
        # data
        "data/mail_template_data.xml",
        "data/sale_order_data.xml",
        # views
        "views/sale_order_views.xml",
        "views/res_partner_views.xml"
    ],
    "license": "OPL-1",
    "auto_install": False,
    "installable": True,
    # 'post_init_hook': 'is_old_orders_are_confirmed',
}
