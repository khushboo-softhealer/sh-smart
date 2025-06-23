# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Leave Attachment",
    "author": "Softhealer Technologies (Nitin Ubhadiya)",
    "license": "OPL-1",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "human resources",
    "summary": "Required Leave Document",
    "description": """Using this module if you want to make attachment field required then just tick 'Sick Leave' then attachment required for that particular leave.""",
    "version": "16.0.1",
    "depends": ["hr_holidays", ],
    "application": True,
    "data": [
        "views/hr_leave_type_views.xml",
        "views/hr_leave_views.xml",
    ],
    "images": ["static/description/background.png", ],
    "live_test_url": "https://youtu.be/j0nPGXM7VQs",
    "auto_install": False,
    "installable": True,
}
