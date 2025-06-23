# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    'name': 'Theme Softhealer Store',
    'description': 'Theme Softhealer Store',
    'summary': 'Theme Softhealer Store',
    'category': 'Theme/eCommerce',
    'version': '16.0.9',
    'author': 'Softhealer',
    'company': 'Softhealer',
    'maintainer': 'Softhealer',
    'website': "https://www.softhealer.com/",
    'depends': ['website_sale','softhealer_website_base', 'sh_product_base', 'sh_website_helpdesk','sh_website_sale_popup_pricelist','website_sale_wishlist','sh_ecommerce_snippet','mass_mailing',"sh_website_tnc", "sh_dynamic_currency_price","sh_confirm_sale","sh_github_connector","portal_rating"],
    'data': [
        "security/ir.model.access.csv",
        
        # SNIPPET TEMPLATES
        'views/snippets/about_us_template.xml',
        'views/snippets/contact_us_template.xml',
        'views/snippets/home_template.xml',
        'views/snippets/privacy_policy_template.xml',
        'views/snippets/terms_and_conditions.xml',
        
        # WEBSITE PAGES
        'views/pages/home_page.xml',
        #'views/pages/about_us_page.xml',
        'views/pages/about_us_page_new.xml',
        #'views/pages/contact_us_page.xml',
        'views/pages/contact_us_page_new.xml',
        #'views/pages/privacy_policy_page.xml',
        'views/pages/privacy_policy_page_new.xml',
        'views/pages/terms_and_conditions.xml',
        'views/pages/diwali_offer_page.xml',

        # WEBSITE PAGES MENUS
        'data/website_menus.xml',

        # COMMON THEME VIEWS
        'views/snippets/snippet_menus.xml',

        # Other website pages
        'views/product_detail_page.xml',
        'views/product_detail_tabs_tmpl.xml',
        'views/website_sale_templates.xml',
        'views/website_layout_template.xml',
        'views/footer.xml',
        'views/header.xml',

        # Blogs
        "views/website_blog_templates.xml",

        # Testimonial
        "views/sh_testimonial_views.xml",
        "views/testimonial_snippet.xml",
        "views/testimonial_snippet_item.xml",

        # Wishlist
        "views/website_sale_wishlist.xml",

        # Website Editor
        "views/sh_ecommerce_filter_menus.xml",
    ],
    'assets': {
        'web.assets_frontend': [
            'theme_softhealer_store/static/src/xml/product_rating_template.xml',
            'theme_softhealer_store/static/src/xml/support_diaload_box_template.xml',
            'theme_softhealer_store/static/src/js/custom.js',
            'theme_softhealer_store/static/src/js/testimonial.js',
            'theme_softhealer_store/static/src/js/product_detail_tab.js',
            'theme_softhealer_store/static/src/scss/mixin.scss',
            'theme_softhealer_store/static/src/scss/style.scss',
            'theme_softhealer_store/static/src/scss/footer.scss',
            'theme_softhealer_store/static/src/scss/custom_variables.scss',
            'theme_softhealer_store/static/src/scss/home_page.scss',
            'theme_softhealer_store/static/src/scss/about_us.scss',
            'theme_softhealer_store/static/src/scss/privacy_policy.scss',
            'theme_softhealer_store/static/src/scss/terms_and_conditions.scss',
            'theme_softhealer_store/static/src/scss/support.scss',
            'theme_softhealer_store/static/src/scss/shop.scss',
            'theme_softhealer_store/static/src/scss/product_detail.scss',
            'theme_softhealer_store/static/src/scss/blog.scss',
            'theme_softhealer_store/static/src/scss/wishlist.scss',
            'theme_softhealer_store/static/src/scss/contact_us_page.scss',
            'theme_softhealer_store/static/src/scss/header_megamenu.scss',
            'theme_softhealer_store/static/src/scss/global_search.scss',
            'theme_softhealer_store/static/src/scss/scrollbar.scss',
            'theme_softhealer_store/static/src/scss/cart.scss',
            'theme_softhealer_store/static/src/scss/common.scss',
            'theme_softhealer_store/static/src/scss/login_page.scss',
            'theme_softhealer_store/static/src/scss/diwali_offer_banner.scss',

             # Owl carousel
            "theme_softhealer_store/static/src/lib/owl_carousel/owl.css",
            "theme_softhealer_store/static/src/lib/owl_carousel/owl.js",
            "theme_softhealer_store/static/src/lib/owl_carousel/owl_init.js",
            
            # counter
            'theme_softhealer_store/static/src/js/counter.js',

            # coming soon
            "theme_softhealer_store/static/src/js/coming_soon.js",
            "theme_softhealer_store/static/src/js/website_wishlist.js",
            "theme_softhealer_store/static/src/js/website_sale_options.js",
        ],
    },
    'images': [],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,

}
