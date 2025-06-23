# Part of Softhealer Technologies.
{
    "name": "Mass Update Partner",
    "author": "Softhealer Technologies - Nayan",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "license": "OPL-1",
    "version": "16.0.1",
    "category": "Extra Tools",
    "summary": "Mass Update Partner",
    "description":  """Mass Update Partner""",
    'depends': ['base_setup', 'product','contacts'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/sh_res_partner_mass_update_wizard_views.xml',
        'views/res_partner_views.xml',
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
}
