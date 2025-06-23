# -*- coding: utf-8 -*-
{
    'name': 'eLearning Pro',
    'version': '16.0.1.6',
    'sequence': 10,
    'summary': 'Enhanced learning using learning path and added more addon features.',
    'website': 'https://www.manprax.com',
    'author': 'ManpraX Software LLP',
    'category': 'Website/eLearning',
    'description': """
Extended feature of elearning.
""",
    'depends': [
        'website_slides', 'survey'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/slide_view.xml',
        'views/res_config_settings.xml',
        'views/survey_survey_views.xml',
        'views/website_slides_templates_course.xml',
        'views/survey_template.xml',
    ],
    'demo': [],
    'qweb': [],
    'images': ["static/description/images/app_banner_pro.png"],
    'price': 500,
    'currency': 'USD',
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [ ],
        'web.assets_frontend': [
            'mx_elearning_pro/static/src/js/slide_comment_composer_fullscreen.js',
            'mx_elearning_pro/static/src/js/slides_course.js',
            'mx_elearning_pro/static/src/js/slides_course_extend.js',
            'mx_elearning_pro/static/src/js/slides_course_page_pro.js',
            'mx_elearning_pro/static/src/js/slides_course_rating_fullscreen.js',
            'mx_elearning_pro/static/lib/autoproctor/autoproctor4.js',
            'mx_elearning_pro/static/lib/Crypto/crypto4.js',
            'mx_elearning_pro/static/lib/proctoredu/supervisor.js',
            'mx_elearning_pro/static/src/xml/**/*',
            'mx_elearning_pro/static/src/scss/**/*',
        ],
        'survey.survey_assets': [
            'mx_elearning_pro/static/src/js/survey_proctor.js',
            'mx_elearning_pro/static/src/scss/survey_templates_form.scss',
        ],
    },
    'license': 'OPL-1',
}