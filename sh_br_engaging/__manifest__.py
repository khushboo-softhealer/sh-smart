# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "BR-Engage",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "license": "OPL-1",
    "category": "",
    "summary": "",
    "description": """""",
    "version": "16.0.1",
    "depends": [
        "web", "base", "mail", "hr","calendar",
    ],
    "data": [
        "security/br_security_groups.xml",
        # "security/br_security_rules.xml",
        "security/ir.model.access.csv",
        # "data/ir_cron_data.xml",
        # "data/mail_template.xml",
        "views/res_config_settings_views.xml",
        # "views/sh_check_in_view.xml",
        # "views/sh_manage_questions_views.xml",
        # "views/calendar_event_views.xml",
        # "views/sh_talking_points_views.xml",
        # "views/sh_manage_agenda_views.xml",
        # "views/sh_realtime_feedback_view.xml",
        # "wizard/sh_give_feedback_wizard.xml",
        # "wizard/sh_request_feedback_wizard.xml",
        # "wizard/sh_update_agenda_wizard_views.xml",
        # "wizard/sh_create_1on1s_wizard_views.xml",
        "views/sh_high_five_view.xml",
        # "views/sh_br_dashboard.xml",
        "views/sh_manage_badge_views.xml",
        # "wizard/sh_view_talking_point_wizard_views.xml",
        "wizard/sh_br_custom_configuration_views.xml",

        # MANAGE MEETING AGENDA
        # "views/sh_manage_meeting_agenda_view.xml",

        # VIEW AGENDA MODEL 
        # "views/sh_view_talking_agenda_view.xml",

        "views/sh_br_engage_menuitems.xml",
    ],
     'assets': {
        'web.assets_backend': [

            "sh_br_engaging/static/src/js/br_high_five_description.js",
            "sh_br_engaging/static/src/xml/br_highfive_description_template.xml",

            # CheckIn Section 
            # "sh_br_engaging/static/src/js/check_in_component.js",
            # "sh_br_engaging/static/src/xml/br_check_in_view.xml",
            # "sh_br_engaging/static/src/scss/checkin.scss",

            # # 1on1's Section 
            # "sh_br_engaging/static/src/js/one_on_ones_component.js",
            # "sh_br_engaging/static/src/xml/one_on_ones_js_template.xml",
            # "sh_br_engaging/static/src/scss/one_on_ones.scss",

            # # Realtime Feedback
            # "sh_br_engaging/static/src/js/realtime_feedback.js",
            # "sh_br_engaging/static/src/xml/realtime_feedback_template.xml",
            # "sh_br_engaging/static/src/scss/realtime_feedback.scss",

            # Add Dynamic Class In Body 
            "sh_br_engaging/static/src/js/dynamic_class.js",

            # Add Buttons In List View 
            # "sh_br_engaging/static/src/js/listController.js",
            # "sh_br_engaging/static/src/xml/listview_buttons.xml",

            # Notifications
            # "sh_br_engaging/static/src/js/br_engage_push_notification.js",
            # "sh_br_engaging/static/src/xml/notification_menu_and_template.xml",
            # "sh_br_engaging/static/src/scss/notification.scss",

            # High Fives
            "sh_br_engaging/static/src/xml/emoji_template.xml",
            "sh_br_engaging/static/src/js/emojis_dropdown.js",
            "sh_br_engaging/static/src/js/high_fives.js",
            "sh_br_engaging/static/src/xml/high_fives.xml",
            "sh_br_engaging/static/src/scss/high_fives.scss",


            # dashboard
            # "sh_br_engaging/static/src/js/br_engage_dashboard.js",
            # "sh_br_engaging/static/src/xml/br_dashboard_template.xml",            
            # "sh_br_engaging/static/src/scss/br_dashboard.scss",

            # Kanban New Button 
            # "sh_br_engaging/static/src/js/kanban_controller.js",
            # "sh_br_engaging/static/src/xml/kanbanview_buttons.xml",

        ],

        'web._assets_primary_variables': [
          ('after', 'web/static/src/scss/primary_variables.scss', 'sh_br_engaging/data/engage_theme_config_main_scss.scss'),        
        ],
    },
    "application": True,
    "auto_install": False,
    "images": ["static/description/background.png", ],
    "installable": True,
}
