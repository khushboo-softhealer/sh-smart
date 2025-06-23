# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Github Connector",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Extra Tools",
    "summary": "",
    "description": """""",
    "version": "16.0.3",
    "depends": [
        "base_setup",
        "sale_management",
        "project",
        "sh_product_base",
        "sh_training",
        "sh_project_task_base",
        "sh_message",
        "sh_copyright_claim_project",
        "sh_push_notification_tile"
    ],
    "application": True,
    "data": [
        # security
        "security/ir.model.access.csv",
        "security/sh_github_connector_groups.xml",
        # data
        "data/sh_github_connector_data.xml",
        "data/mail_template_data.xml",
        "data/ir_cron_data.xml",
        # wizard
        "wizard/sh_repo_wizard_views.xml",
        # views
        "views/sh_map_categ_views.xml",
        "views/sh_repo_branch_views.xml",
        "views/blog_post_views.xml",
        "views/product_template_views.xml",
        "views/product_product_views.xml",
        "views/sh_github_connector_views.xml",
        "views/sh_git_repo_views.xml",
        # "views/sh_index_queue_views.xml",
        "views/sh_module_views.xml",
        "views/sh_connector_log_views.xml",
        "views/project_task_views.xml",
        "views/res_users_views.xml",
        "views/sh_github_connector_menues.xml",
    ],
    "license": "OPL-1",
    "auto_install": False,
    "installable": True,
}
