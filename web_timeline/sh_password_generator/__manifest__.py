# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Password Generator",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "version": "16.0.1",
    "category": "Extra Tools",
    "summary": "Password Generator, Generate Dynamic Password Module, Encrypt System Password App, Provide Customer Password Application, Get Passwords For Test, Create Strong Password, Different Password Filter, Make Password With Pattern Password Generator Field Password Manager Credential Manager Password Keeper Team Password Management Odoo",
    "description": """This module is used to generate a password that can be used for any purpose like demo servers, test servers, etc. It's very difficult to manage different passwords of multiple projects/servers/customers. Here we giving a tool that helps to manage different passwords with security in one place. you can easily make a new password with your password patterns and length, You can easily track expired passwords. We have made two security groups manager and user, managers have access to do everything and the user can only read. you can easily copy the password, url, username, etc on a single click. High-level encryption added at the database level so it will help passwords to protect from SQL injection. you can also have different filter options like partner wise, IP wise, created on, etc. Also you can set a patter for generating password like only in Uppercase, Lowercase, Digits, Special symbols or all of them.""",
    "depends": ['base','mail', 'project'],
    'external_dependencies' : {
        'python' : ['password_strength'],
    },
    "data": [
        "data/sh_password_generator_data.xml",
        "security/sh_password_generator_groups.xml",
        "security/ir.model.access.csv",
        "wizard/password_generator_wizard_views.xml",
        "views/password_generator_views.xml",
        "views/res_partner_views.xml",
        "views/password_type_pattern_views.xml",
        "views/project_project_views.xml",
    ],
    # "images": ['static/description/background.png',],
    "installable": True,
    "application": True,
    "auto_install": False,
    "price": 40,
    "currency": "EUR",
    "license": "OPL-1"
}
