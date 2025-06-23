# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Push Notification Tile",
    
    "author": "Softhealer Technologies - (Pranav vasant)",
    
    "website": "https://www.softhealer.com",    
    
    "support": "support@softhealer.com",   

    "version": "16.0.1",

    "license": "OPL-1",
    
    "category": "Extra Tools",
    
    "summary": "Push Notification Tile",
        
    "description": """Push Notification Tile""",
     
    "depends": ['base_setup'],
        
    "data": [
        "security/ir.model.access.csv",
        'data/data.xml',
        'views/push_notification.xml',
        'views/res_users.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sh_push_notification_tile/static/src/js/systray_activity_menu.js',
            'sh_push_notification_tile/static/src/scss/notification.scss',
            'sh_push_notification_tile/static/src/xml/widget.xml',
        ],
    },
    "installable": True,    
    "auto_install": False,    
    "application": True, 
    "price": "50",
    "currency": "EUR"        
}
