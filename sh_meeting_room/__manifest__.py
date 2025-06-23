# Part of Softhealer Technologies.
{
    "name": "Meeting Rooms Dashboard",

    "author": "Softhealer Technologies",

    "website": "https://www.softhealer.com",

    "support": "support@softhealer.com",

    "version": "16.0.5",

    "license": "OPL-1",

    "category": "Sales",

    "summary": "",

    "description": """""",

    "depends": ['calendar'],

    "data": [   
        "security/ir.model.access.csv", 
        "views/calender_event_views.xml",
        "views/sh_meeting_rooms_views.xml",
        "views/sh_meeting_rooms_menus.xml"         
    ],  
    "assets": {
        'web.assets_backend': [
            "sh_meeting_room/static/src/views/calender_inherit.js",
            'sh_meeting_room/static/src/scss/rooms_kanbanviews.scss',                      
        ],       
    }, 
    "installable": True,
    "auto_install": False,
    "application": True,
}
