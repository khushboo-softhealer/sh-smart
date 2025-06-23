# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "All In One Survey Management | Morden Survey Theme | Survey By Additional Fields | Survey Templates | Survey Matrix | Custom Survey",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Extra Tools",
    "license": "OPL-1",
    "summary": "Create Awesome Survey By Email Survey By File Survey By URL Survey By Time Survey By Range Survey By Barcode Survey By QRCode Export Survey Answer XLS Latest Survey Theme Organization Survey Company Survey Creative Survey Theme Beautifull Survey Survey file upload Survey attachment upload on Survey attach file on Survey attachment upload attachment on Survey binary field Survey multi file upload Survey multi attachment on Survey attach file on Survey attachment answer Survey file upload option Survey Multi File Upload Field and upload in attachment survey theme all in one survey Odoo",
    "description": """A survey is a method to collect data from various people to gain information on different topics. The survey can be useful for multiple purposes. We have created this app to make odoo survey module more useful. Our module provides survey with many addition fields options and different theme styles. We provide 5 unique theme styles for survey so you can use different theme for different survey. You can create attractive and clean survey forms with no effort so you can easily create survey using this module. We provide 20+ additional fields For Survey.""",
    "version": "16.0.3",
    "depends": ["survey", "website", ],
    "data": [

        "security/ir.model.access.csv",
        "security/survey_security.xml",
        # Survmate

        "sh_survmate_theme/wizards/button_style_wizard_views.xml",
        "sh_survmate_theme/views/survey_layout_templates.xml",
        "sh_survmate_theme/views/survey_views.xml",
        "sh_survmate_theme/views/survey_setting_views.xml",
        "sh_survmate_theme/views/survey_question_views.xml",
        "sh_survmate_theme/views/survey_question_template.xml",
        "sh_survmate_theme/views/survey_question_matrix_templates.xml",
        "sh_survmate_theme/data/survmate_demo.xml",

        # Survey extra fields

        'sh_survey_extra_fields/views/survey_statistics_templates.xml',
        'sh_survey_extra_fields/views/survey_templates.xml',
        'sh_survey_extra_fields/views/survey_views.xml',

        # Survey Matrix Adv
        'sh_survey_matrix_adv/views/survey_templates.xml',
        'sh_survey_matrix_adv/views/survey_views.xml',

        # sh_survey_extra_fields_adv
        'sh_survey_extra_fields_adv/views/survey_page_fill_templates.xml',
        'sh_survey_extra_fields_adv/views/survey_templates.xml',
        'sh_survey_extra_fields_adv/views/survey_views.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'sh_survey_all_in_one/static/src/scss/extra_addons/sh_survmate_theme/button_style.scss',
            'sh_survey_all_in_one/static/src/scss/extra_addons/sh_survmate_theme/checkbox_style.scss',
            'sh_survey_all_in_one/static/src/scss/extra_addons/sh_survmate_theme/common_style.scss',
            'sh_survey_all_in_one/static/src/scss/extra_addons/sh_survmate_theme/input_style.scss',
            'sh_survey_all_in_one/static/src/scss/extra_addons/sh_survmate_theme/radio_btn.scss',
            'sh_survey_all_in_one/static/src/scss/extra_addons/sh_survmate_theme/section_style.scss',
        ],
        'survey.survey_assets': [
            'sh_survey_all_in_one/static/src/css/extra_addons/sh_survey_extra_fields/filter_multi_select.css',
            'sh_survey_all_in_one/static/src/js/extra_addons/sh_survey_extra_fields/bootstrap-multiselect.js',
            'sh_survey_all_in_one/static/src/js/extra_addons/sh_survey_extra_fields/filter-multi-select-bundle.min.js',
            'sh_survey_all_in_one/static/src/js/extra_addons/sh_survey_extra_fields/jSignature.js',
            'sh_survey_all_in_one/static/src/js/extra_addons/sh_survey_extra_fields/survey_form.js',
            'sh_survey_all_in_one/static/src/css/extra_addons/sh_survey_matrix_adv/survey.css',
            'sh_survey_all_in_one/static/src/js/extra_addons/sh_survey_matrix_adv/survey_form.js',

            # sh_survey_extra_fields_adv
            'sh_survey_all_in_one/static/src/css/extra_addons/sh_survey_extra_fields_adv/sh_survey_extra_fields_adv.css',
            'sh_survey_all_in_one/static/src/scss/extra_addons/sh_survey_extra_fields_adv/extra_field_barcode.scss',
            'sh_survey_all_in_one/static/src/js/extra_addons/sh_survey_extra_fields_adv/ZXing.js',
            'sh_survey_all_in_one/static/src/js/extra_addons/sh_survey_extra_fields_adv/survey_form.js',
            'sh_survey_all_in_one/static/src/js/extra_addons/sh_survey_extra_fields_adv/extra_field_barcode.js',
        ],
    },
    "images": ["static/description/background.gif", ],
    "auto_install": False,
    "installable": True,
    "application": True,
    "price": 250,
    "currency": "EUR"
}
