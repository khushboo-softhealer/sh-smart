# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Purchase Order billed Details",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Purchases",
    "summary": "purchase order paid amount app, count po due amount module, track billed amount, total paid amount odoo",
    "description": """Are you facing issue to check bills amounts of purchase order? How much amount paid? How much amount remaining?
So here is the solution, This module help you to find total amount billed, due amount, paid amount, % of total paid
purchase order paid amount app, count po due amount module, track billed amount, total paid amount odoo""",
    "version": "16.0.1",
    "depends": [
        "purchase",
    ],
    "application": True,
    "data": [
        'views/purchase_order_views.xml',
    ],
    "images": ["static/description/background.png", ],
    "live_test_url": "https://youtu.be/Jxt1kUzB0r0",
    "license": "OPL-1",
    "auto_install": False,
    "installable": True,
    "price": 18,
    "currency": "EUR"
}
