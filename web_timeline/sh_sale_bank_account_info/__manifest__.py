# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

{
    "name": "Bank Account Information in Sale",
    "author": "Softhealer Technologies - Daki Ketan",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "license": "OPL-1",
    "version": "16.0.1",
    "category": "Extra Tools",
    "summary": "Bank Account Information in Sale Odoo",
    "description": """This module useful to give Bank Account Information in Sale.""",
    "depends": [
        'account',
        'project',
        'sale_management',
        'sh_product_base',
        'sale_quotation_builder'
    ],
    "data": [
        "views/sale_order_views.xml",
        "reports/sale_bank_account_info_templates.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
