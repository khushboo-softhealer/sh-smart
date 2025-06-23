# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "All in one mass confirm | Sale orer mass confirm | Purchase orer mass confirm | Invoice mass confirm",
    "author": "Softhealer Technologies - Nayan",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Extra Tools",
    "license": "OPL-1",
    "summary": "request for quotation mass confirm, RFQ bulk confirm,invoices bunch confirm module, multiple PO confirm, Multi SO Confirm, account mass conform odoo",
    "description": """This module useful to mass confirm quotation, rfq, invoices.
mass confirm quotations app, bulk confirm request for quote, bunch invoices confirm module, multiple rfq confirm odoo""",
    "version": "16.0.1",
    "depends": ["base", "sale", "sale_management", "purchase", "account"],
    "application": True,
    "data": [
        'views/sale_order_views.xml',
        'views/purchase_order_views.xml',
        'views/account_move_views.xml',
    ],
    "images": ["static/description/background.png", ],
    "live_test_url": "https://youtu.be/0-hDS8J0TeU",
    "auto_install": False,
    "installable": True,
    "price": 15,
    "currency": "EUR"
}
