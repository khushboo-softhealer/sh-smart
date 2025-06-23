# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Download Module Internal",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Extra Tools",
    "summary": "",
    "description": """""",
    "version": "16.0.2",
    "depends": [
        "project",
        "sh_push_notification_tile",
        "sh_github_connector",
        "sh_global_requests"
    ],
    "application": True,
    "data": [
        "security/sh_download_module_internal_groups.xml",
        "security/ir.model.access.csv",
        "security/sh_download_module_internal_security.xml",
        # data
        "data/ir_cron_data.xml",
        "data/ir.activity.xml",
        # wizard
        "wizard/sh_module_req_wizard_views.xml",
        # views
        "views/res_config_settings_views.xml",
        "views/sh_download_module_req_views.xml",
        "views/sh_download_module_log_views.xml",
        "views/sh_github_connector_views.xml",
        # menus
        "views/sh_download_module_internal_menus.xml"
    ],
    'assets': {
        'web.assets_backend': [
            'sh_download_module_internal/static/src/xml/sh_global_request_icon_template.xml',
            'sh_download_module_internal/static/src/js/global_request_icon_menu.js',
        ],
    },
    "license": "OPL-1",
    "auto_install": False,
    "installable": True,
}
