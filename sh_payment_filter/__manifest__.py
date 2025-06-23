# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    'name': 'Payment Filters',
    'author': 'Softhealer Technologies - Nitin Ubhadiya',
    'website': 'http://www.softhealer.com',
    'support': 'support@softhealer.com',
    'category': 'Accounting',
    "license": "OPL-1",
    'summary': 'Filter Invoice Payment Filter Payment By Today Filter Payment Yesterday Filter Payment This Week Filter Payment Filter Payment This Month Filter Payment This Year Filter Payment Last Week Filter Payment Last Month Filter Payment Last Year Odoo',
    'description': """This module allows to filter payment by Today, Yesterday,This Week, This Month, This Year, Last Week, Last Month, Last Year.""",
    "version": "16.0.1",
    "depends": ['account'],
    "data": ['views/account_payment_views.xml'],
    "application": True,
    "auto_install": False,
    "installable": True,
    'images': ['static/description/background.png'],
    "price": 10,
    "currency": "EUR"
}
