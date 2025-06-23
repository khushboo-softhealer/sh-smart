# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "HR Placement",

    "author": "Softhealer Technologies - Nayan",

    "website": "https://www.softhealer.com",

    "support": "support@softhealer.com",

    "version": "16.0.1",

    "category": "",

    "license": "OPL-1",

    "summary": "",

    "description":  """
                    """,

    "depends": ["base", "mail", "hr_recruitment"],

    "data": [
        'security/ir.model.access.csv',
        "wizard/sh_change_datetime_wizard_views.xml",
        "wizard/sh_change_state_wizard_views.xml",
        'views/sh_placement_views.xml',
        'views/sh_college_views.xml',
        "views/hr_applicant_views.xml",
        "views/sh_proposal_reject_reasons_views.xml",
        "views/sh_college_stages_views.xml",
        "wizard/sh_college_change_stages_wizard_views.xml",
    ],

    "installable": True,
    "auto_install": False,
    "application": True,
    "price": "25",
    "currency": "EUR"
}
