# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name":
    "Global Requests",
    "author":
    "Softhealer Technologies (Kishan Patadiya)",
    "website":
    "https://www.softhealer.com",
    "support":
    "info@softhealer.com",
    "version":
    "16.0.2",
    "license": "OPL-1",
    "category":
    "Project",
    "summary":
    """
	Global Requests""",
    "description":
    """Global Requests""",
    "depends":
    ['sh_knowledge_base_customised','sh_emp_idea','sh_emp_complain','sh_assets_manager'],
    "data": [

        'security/ir.model.access.csv',
        'security/global_request_access_group.xml',
        'wizard/sh_global_request_wizard.xml',
    ],

    "images": [
        "static/description/background.png",
    ],

    'assets': {
        'web.assets_backend': [
            'sh_global_requests/static/src/xml/global_request_icon_template.xml',
            'sh_global_requests/static/src/js/global_request_icon_menu.js',
            'sh_global_requests/static/src/scss/global_request_design.scss',
        ],
    },

    "installable":
    True,
    "auto_install":
    False,
    "application":
    True,
    "price":
    "9",
    "currency":
    "EUR"
}
