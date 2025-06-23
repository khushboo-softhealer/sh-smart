# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Employee Idea Management",

    "author": "Softhealer Technologies",
    
    "license": "OPL-1",

    "website": "https://www.softhealer.com",

    "support": "support@softhealer.com",

    "version": "16.0.1",

    "category": "Human Resources",

    "summary": "Manage Idea Management Worker Idea Manage Workers Idea Staff Idea Maintain Ideas employee votes employee share idea manage idea types employee idea notification HR employee share ideas HR share ideas Employee Idea Request Idea approval Odoo",
    
    "description": """Idea Management" helps to increase organization growth with new opportunities. Idea management is the best way for innovation also. Ideas are useless when the ideas in the spreadsheets & notes. Idea management makes it possible for the organization. Using this module you can promote new ideas easily. Employees can create their own idea with idea categories. After that posted ideas go to responsible persons and they can approve, refuse or cancel. Responsible persons gets email for ideas and employee gets email for idea approved, refused or canceled. They can give ratings and comment about decison. Idea Management System Odoo, Manage Ideas Module, Idea Management, Employee Idea Management, Manage Ideas With Types, Maintain Ideas Odoo, Manage Ideas Module, Idea Management App, Employee Idea Management, Manage Ideas With Types, Maintain Ideas Odoo""",
    "depends": [

            'hr',
    ],

    "data": [

        'security/ir.model.access.csv',
        'security/idea_security.xml',
        'data/sh_idea_sequence.xml',
        'data/new_idea_mail.xml',
        'views/sh_idea.xml',
        'wizard/sh_idea_approve_wizard.xml',
        'wizard/sh_idea_refuse_wizard.xml',
        'views/sh_idea_categories.xml',


    ],

    "installable": True,
    "auto_install": False,
    "application": True,
    "images": ["static/description/background.png", ],
    "price": "25",
    "currency": "EUR"
}
