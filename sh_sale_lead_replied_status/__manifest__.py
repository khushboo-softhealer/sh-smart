# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    "name": "Sale and Lead mail replied status",
    "author": "Softhealer Technologies(NIRALI DHOLARIA)",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "version": "16.0.6",
    "category": "Extra Tools",
    "summary": "",
    "description": """""",
    "depends": ["sale_management", "crm", "sh_helpdesk"],
    "data": [
        "data/replied_status_data.xml",
        "security/ir.model.access.csv",
        "views/res_config_settings_views.xml",
        "wizard/sale_update_wizard_views.xml",
        "views/sale_order.xml",
        "views/crm_lead.xml",
        "views/account_move_views.xml",
    ],
    "license": "OPL-1",
    "installable": True,
    "application": True,
    "autoinstall": False,
}
