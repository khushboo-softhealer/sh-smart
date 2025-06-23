# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    'name': 'Migration',
    'author': 'Softhealer Technologies',
    'license': 'OPL-1',
    'website': 'https://www.softhealer.com',
    'support': 'support@softhealer.com',
    'category': 'Extra Tools',
    'summary': 'Migratoin',
    'description': '''Migratoin''',
    'license': 'OPL-1',
    'version': '16.0.2',
    'depends': [
        'sh_project_task_base',
        'sh_product_base'
    ],
    'data': [
        # SECURITY
        'security/ir.model.access.csv',
        # DATA
        'data/ir_sequence.xml',
        'data/sh_migration_actions.xml',
        # VIEWS
        'views/sh_bug_state_log_views.xml',
        'views/sh_bug_state_views.xml',
        'views/sh_module_bug_views.xml',
        'views/project_task_views.xml',
        'views/res_config_settings_views.xml',
        # MENUS
        'views/sh_migration_menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sh_migration/static/src/js/sh_migration_dashboard.js',
            'sh_migration/static/src/xml/sh_migration_dashboard_templates.xml',
            'sh_migration/static/src/scss/dashboard.css',
        ],
    },
    'application': True,
    'auto_install': False,
    'installable': True,
    'images': ['static/description/background.png'],
}
