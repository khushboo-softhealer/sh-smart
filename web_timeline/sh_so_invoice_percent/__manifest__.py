# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Sale Order Invoiced Details",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Sales",
    "summary": """count sale order paid amount count so due amount track billed amount total paid amount percentage sales payment details odoo""",
    "description": """
This module helps you to find the total amount invoiced, due amount, paid amount, % of total paid. Are you facing issues to check invoices amounts of sale order? How much amount paid? How much amount remaining? So here is the solution, This module helps you to find the total amount invoiced, due amount, paid amount, % of total paid. Cheers!
                    """,
    "version": "16.0.1",
    "depends": [
        "sale_management",
    ],
    "application": True,
    "data": [
        'views/sale_views.xml',
    ],
    "images": ["static/description/background.jpg", ],
    "live_test_url": "https://youtu.be/gFG9Yk6UjHc",
    "license": "OPL-1",
    "auto_install": False,
    "installable": True,
    "price": 18,
    "currency": "EUR"
}
