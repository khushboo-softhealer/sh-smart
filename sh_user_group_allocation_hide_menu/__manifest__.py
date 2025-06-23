# -*- coding: utf-8 -*-
# Part of Softhealer Technology

{
    'name': "User Hide Menu & Group Allocation | Mass User Group Allocation | Mass User Hide Menu",
    'author' : 'Softhealer Technologies',
    'website': 'https://www.softhealer.com',
    "support": "support@softhealer.com",
    'category': 'Human Resources',
    'version': '16.0.2',
    "license": "OPL-1",
    "summary": "Group Allocation Template,Mass Hide Menu Template,User Access Group Allocation,Access Rights Group Allocation,User Group Template,Access Group Template,Hide Menu Items,Disable Menu Item,Invisible Menu,Remove Menu,Delete Menu,Invisible Root Menu Odoo",
    "description": """In this module, You can generate a template for user's access rights groups and hide menu items. Once you've established a template, you can assign it to users, which will immediately enable access groups as well as hide menus for that user. You can also utilize the mass action to update several user groups quickly.""",
    "depends": ["base", "web"],
    "data": [

        'security/ir.model.access.csv',
        'wizard/sh_template_wizard.xml',
        'wizard/sh_groups_allocation_wizard.xml',
        'wizard/sh_templates_allocation_wizard.xml',
        'views/sh_template_views.xml',
        "views/res_users_views.xml",
    ],


    "auto_install": False,
    "installable": True,
    "application": True,
    'images': ['static/description/background.png', ],
    "price": 40,
    "currency": "EUR"
}
