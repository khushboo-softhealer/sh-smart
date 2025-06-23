# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Softhealer Demo Database",
    "author": "Softhealer Technologies",
    "website": "http://www.softhealer.com",
    "support": "info@softhealer.com",
    "category": "crm",
    "summary": "",
    "license": "OPL-1",
    "description": """
                    """,
    "version": "16.0.6",
    "depends": [
                "sh_product_base",
                "sh_helpdesk",
    ],
    "application": True,
    "data": [
        "security/sh_demo_db_security.xml",
        "security/ir.model.access.csv",
        "data/data.xml",
        "data/demo_db_email_template.xml",
        "views/res_config_setting.xml",
        #             "views/sh_product_template_view.xml",
        #             "views/sh_demo_db_view.xml",
        "views/sh_demo_db_server_view.xml",
        "views/sh_demo_db_log_view.xml",
        "views/helpdesk_ticket.xml",
        "views/crm_lead.xml",

    ],
    "auto_install": False,
    "installable": True,
}
