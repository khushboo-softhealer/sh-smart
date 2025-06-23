# -*- coding: utf-8 -*-

{
    "name": "Expense Wallet | Employee Expense Management",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Human Resources",
    "license": "OPL-1",
    "summary": "Wallet For Employee,Employee Wallet,Customer Wallet,Employee Expense Wallet,Wallet Management,Customer Expense Wallet,User Wallet,E-commerce Wallet,Ecommerce Wallet,E commerce Wallet,Advance Payment By Wallet,Expense Request,Expense Limit Odoo",
    "description": """
    This module allows to manage the wallet for the employee expense. Money will be added in the wallet by who is managing the wallet of the employee so they have to do advance payment to add money in the wallet and this wallet can be used for future expenses. When the employee creates an expense that can be approved by only who is managing the employee wallet.
    For ex. Anita is managing employee expense and she adds $500 in the wallet. Now Azure creates expenses of $200. Once that expense is approved by Anita it will auto take $200 from the wallet. Now in the wallet will be $300.
    """,
    "version": "16.0.1",
    "depends": ["hr_expense"],
    "data": [
        'data/ir_sequence_data.xml',
        'security/ir.model.access.csv',
        'security/wallet_security.xml',
        'wizard/wallet_transaction_wizard.xml',
        'views/res_config_settings.xml',
        'views/wallet.xml',
        'views/hr_expense.xml',
    ],
    'images': ['static/description/background.png', ],
    "auto_install": False,
    "installable": True,
    "application": True,
    "price": 40,
    "currency": "EUR",

}
