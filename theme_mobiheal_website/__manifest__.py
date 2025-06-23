# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    'name': 'Theme Mobiheal Website',
    'description': 'Theme Mobiheal Website',
    'summary': 'Theme Mobiheal Website',
    'category': 'Theme/website',
    'version': '16.0.1',
    'author': 'Softhealer',
    'company': 'Softhealer',
    'maintainer': 'Softhealer',
    'website': "https://www.mobiheal.tech/",
    'depends': ['website','sale','sh_website_helpdesk','softhealer_website_base'],
    'data': [
        "views/footer.xml",
        "views/header.xml",
        "views/theme_options.xml",
        "views/website_templates.xml",
        "views/website_jobs_templates.xml",

        ## Pages
        "views/pages/about.xml",
        "views/pages/contact.xml",
        "views/pages/dman_page.xml",
        "views/pages/event_page.xml",
        "views/pages/home.xml",
        "views/pages/order_page.xml",
        "views/pages/privacy_policy.xml",
        "views/pages/service.xml",
        "views/pages/terms_condition.xml",
        "views/pages/support_page.xml",

        
    ],
    'assets': {
        'web.assets_frontend': [

            ## SCSS
            "theme_mobiheal_website/static/src/js/lib/owl/owl.carousel.min.css",
            "theme_mobiheal_website/static/src/js/lib/owl/owl.theme.default.min.css",
            "theme_mobiheal_website/static/src/scss/mixin.scss",
            "theme_mobiheal_website/static/src/scss/custom_footer.scss",
            "theme_mobiheal_website/static/src/scss/custom_header.scss",
            "theme_mobiheal_website/static/src/scss/home_page.scss",
            "theme_mobiheal_website/static/src/scss/swiper.min.scss",
            "theme_mobiheal_website/static/src/scss/dman_page.scss",
            "theme_mobiheal_website/static/src/scss/order_page.scss",
            "theme_mobiheal_website/static/src/scss/event_page.scss",
            "theme_mobiheal_website/static/src/scss/about_page.scss",
            "theme_mobiheal_website/static/src/scss/service_page.scss",
            "theme_mobiheal_website/static/src/scss/contact_page.scss",
            "theme_mobiheal_website/static/src/scss/privacy_policy.scss",
            "theme_mobiheal_website/static/src/scss/terms_condition.scss",
            "theme_mobiheal_website/static/src/scss/login_page.scss",
            "theme_mobiheal_website/static/src/scss/support_page.scss",
            "theme_mobiheal_website/static/src/scss/blog.scss",
            "theme_mobiheal_website/static/src/scss/jobs.scss",

            ## JS 
            "theme_mobiheal_website/static/src/js/lib/owl/owl.carousel.js",
            "theme_mobiheal_website/static/src/js/custom_header.js",
            "theme_mobiheal_website/static/src/js/swiper.min.js",
            "theme_mobiheal_website/static/src/js/style_1.js",
            "theme_mobiheal_website/static/src/js/offer.js",
            "theme_mobiheal_website/static/src/js/footer.js",
            "theme_mobiheal_website/static/src/js/counter.js",
            
        ],
    },
    'images': [],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,

}
