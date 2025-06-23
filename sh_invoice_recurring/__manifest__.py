# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Invoice Order Recurring",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Accounting",
    "license": "OPL-1",
    "summary": """
Make Recurring Orders For invoices, Auto Repeat Order For invoice,
Generate Monthly Regular Order Module, Weekly Regular invoice,
Manually Recurring Order, account Recurring Module,
bill Recurring, payment Recurring App, invoice Recurring Odoo
""",
    "description": """
You can make a recurring order for your regular customers using this module.
For example, a consumer could set up an order to have
particular goods in every three months.
you can make recurring orders using this module would
let this invoice happen automatically on a regular schedule.
You can also make recurring orders manually from recurring orders.
You can set the scheduled time.
""",
    "version": "16.0.1",
    "depends": ["account", "utm"],
    "application": True,
    "data": ["security/sh_invoice_recurring_security.xml",
             "security/ir.model.access.csv",
             "data/ir_sequence.xml",
             "data/ir_cron_data.xml",
             "views/res_config_setting.xml",
             "views/account_move_views.xml",
             "views/sh_invoice_recurring_views.xml", ],
    "images": ["static/description/background.png", ],
    "live_test_url": "https://youtu.be/tcJZmLFwtQ0",
    "auto_install": False,
    "installable": True,
    "price": 36.8,
    "currency": "EUR"
}
