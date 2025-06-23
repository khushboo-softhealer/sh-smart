# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    'name': 'Softhealer Website Base',
    'author': 'Softhealer Technologies',
    'website': 'https://www.softhealer.com',
    'support': 'support@softhealer.com',
    'category': 'Website',
    'summary': 'Softhealer Website Base',
    'description': '''Softhealer Website Base''',
    'version': '16.0.5',
    # 'depends': ['website_hr_recruitment', 'website_sale', "website_blog","website_sale_loyalty", "sh_helpdesk","sh_helpdesk_customisation","sh_website_helpdesk","google_recaptcha"],
    'depends': ['website_hr_recruitment', 'website_sale', "website_blog","website_sale_loyalty", "sh_helpdesk","sh_helpdesk_customisation","sh_website_helpdesk","google_recaptcha","utm"],
    'application': True,
    'data': [
        'data/hr_applicant_form_website.xml',
        "security/website_security.xml",
        "security/ir.model.access.csv",
        "wizard/sh_cover_properties_wizard.xml",
        "views/sh_helpdesk_ticket_type_views.xml",
        "wizard/ir_ui_view_wizard.xml",
        'views/hr_job_views.xml',
        "views/website_views.xml",
        "views/website_menu_form_view.xml",
        "views/website_blog_views.xml",
        "views/website_sale.xml",
        "views/sh_website_popular_searches_views.xml",
        'views/sh_helpdesk.xml',

        ## UTM Menus
        "views/utm_capaign_views.xml",
        "views/utm_medium_views.xml",
        "views/utm_source_views.xml",
    
        ## download log
        "views/sh_module_download_log_views.xml",
        "views/sale_order_views.xml",

        # Website Editor views
        "views/website_editor/hr_job_editor_views.xml",
        "views/website_editor/website_page_editor_views.xml",
        "views/website_editor/blog_post_editor_views.xml",
        "views/website_editor/blog_blog_editor_views.xml",
        "views/website_editor/product_editor_views.xml",
        "views/website_editor/website_editor_menus.xml",
        "views/res_config_settings_views.xml",
        "views/snippets/s_sh_website_popular_searches.xml",
        "views/product_views.xml",
        # login adn sign up
        "views/signup_login_page.xml",
        # Keep it in base for external ID
        "views/website_hr_recruitment_templates.xml",
        "views/website_sale_blog_templates.xml",
        "views/website_sale_loyalty_templates.xml",
        "views/account_fiscal_position_views.xml",

        "views/sale_portal_templates.xml",
        
        "views/sh_custom_contact_us_ticket_form_vews.xml", 
        "views/website_blog_templates.xml",
        "views/hr_applicant_views.xml",
        "views/sale_order_portal_template.xml"
    ],
    'assets': {
        'web.assets_frontend': [
            'softhealer_website_base/static/src/js/website_header_global_search.js',
            'softhealer_website_base/static/src/xml/website_header_global_search.xml',
            'softhealer_website_base/static/src/scss/global_search.scss',
            'softhealer_website_base/static/src/scss/sale_portal.scss',
            'softhealer_website_base/static/src/scss/support_ticket.scss',
            'softhealer_website_base/static/src/js/common.js',
            'softhealer_website_base/static/src/js/scroll.js',

            # categ mega menu
            "softhealer_website_base/static/src/js/categ_megamenu.js",

            # Popular searches
            "softhealer_website_base/static/src/js/s_sh_popular_searches.js",
            "softhealer_website_base/static/src/xml/s_sh_popular_searches.xml",

            ## Blog
            "softhealer_website_base/static/src/scss/common.scss",
            "softhealer_website_base/static/src/scss/buy_now_button.scss",
            "softhealer_website_base/static/src/js/support_ticket.js",

            "softhealer_website_base/static/src/xml/sh_rfq_from_ticket_create.xml",
            "softhealer_website_base/static/src/js/custom_website_form.js",

        ],
        'web.assets_backend': [
            'softhealer_website_base/static/src/scss/recruitment.scss',
        ],
    },
    'images': [],
    'auto_install': False,
    'installable': True,
    'license': 'OPL-1',
    'price': '35',
    'currency': 'EUR'
}
