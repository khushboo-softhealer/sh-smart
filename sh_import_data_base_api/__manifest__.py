# Part of Softhealer Technologies.
{
    "name": "Import Base Automated",

    "author": "Softhealer Technologies",

    "website": "https://www.softhealer.com",

    "support": "support@softhealer.com",

    "version": "16.0.1",

    "license": "OPL-1",

    "category": "Sales",

    "summary": "Import Base",

    "description": """Import Base""",

    "depends": [
        'sale_management',
        'account',
        'project',
        'hr',
        'hr_timesheet',
        'crm',
        'sh_helpdesk',
        'sh_training',
        'sh_sale_lead_replied_status', 
        'sh_employee_extra_fields',
        'sh_assets_manager',
        'sh_icici_bank_payment',
        'sh_hr_placement',
        'sh_copyright_claim_project',
        'sh_hr_contract',
    ],

    "data": [
        "security/ir.model.access.csv",
        "data/sh_import_cron_data.xml",
        "data/sh_import_multi_action.xml",
        "security/import_security.xml",
        "views/sh_import_base_views.xml",
        "views/sh_import_base_logs_views.xml",
        "views/sh_import_failed_views.xml",
        "views/crm_lead_views.xml",
        "views/sh_import_menus.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
    "images": ["static/description/background.png", ],
    "price": "0",
    "currency": "EUR"
}
