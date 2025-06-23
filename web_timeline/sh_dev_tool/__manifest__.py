# Copyright (C) Softhealer Technologies.
{
    'name': 'Development Tool',

    'author': 'Softhealer Technologies',

    'website': 'https://www.softhealer.com',

    "support": "support@softhealer.com",

    'version': '16.0.1',

    'category': 'Extra Tools',
    
    "license": "OPL-1",

    'summary': 'Install Button On Odoo Module, Upgrade Button On App List, Uninstall Button On Screen, Bunch Module Uninstall, Bulk Apps Install, Multiple Module Upgrade Odoo',

    'description': """
Do you want to make a developer happy? This module helps the developer to manage the system. This module provides all buttons like install, upgrade & uninstall, on the main screen of the apps in kanban view & tree view. You can install, upgrade & uninstall the modules in a bunch.""",
    'depends': ['base_setup', 'web'],

    'data': [
        "views/views.xml",
        "data/data.xml"
    ],
    "images": ["static/description/background.png", ],
    'auto_install': False,
    'installable': True,
    'application': True,
    "price": 15,
    "currency": "EUR"
}
