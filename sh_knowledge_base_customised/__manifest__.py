# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Knowledge Customized",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "license": "OPL-1",
    "support": "support@softhealer.com",
    "category": "Extra Tools",
    "summary": """""",
    "description": """""",
    "version": "16.0.1",
    "depends": ['mail','utm','sh_project_task_base'],
    "data": [        
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/sequence_data.xml',
        'report/sh_knowledge_article_reports.xml',
        'report/sh_report_watermark.xml',
        'wizard/sh_article_update_wizard_views.xml',
        'views/sh_knowledge_article_views.xml',  
        'views/sh_sop_article_views.xml',  
        'views/sh_article_categories_views.xml',
        'views/sh_sop_article_categories_views.xml',
        'views/sh_artical_tags_views.xml',
        'views/sh_sop_artical_tags_views.xml',
        "views/sh_sop_stages_views.xml",
        "views/res_config_settings_views.xml",
        'views/sh_knowledge_menus.xml',
        
    ],
     'assets': {
        'web.assets_backend': [
         'sh_knowledge_base_customised/static/src/scss/style.scss',   
         'sh_knowledge_base_customised/static/src/js/sh_sop_custom_class.js',   
        ],
     },
    "images": ["static/description/background.png", ],
    "auto_install": False,
    "application": True,
    "installable": True,   
}
