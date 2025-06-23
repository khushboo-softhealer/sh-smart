# Part of Softhealer Technologies.
{
    "name": "ChatGPT Integration With Odoo",

    "author": "Softhealer Technologies",

    "website": "https://www.softhealer.com",

    "support": "support@softhealer.com",

    "version": "16.0.4",

    "license": "OPL-1",

    "category": "Productivity",

    "summary": "ChatGPT Integration With Odoo ChatGPT From ChatRoom ChatGPT OpenAI ChatRoom 2.0 Odoo Connector for ChatGPT Odoo Integration ChatGPT and Odoo Integration Seamless ChatGPT Odoo Connection Odoo ChatGPT Integration Plugin Integrating ChatGPT with Odoo ChatGPT and Odoo Connector Solution Odoo and ChatGPT Integration Tool ChatGPT Odoo Bridge Odoo CRM ChatGPT Connector OpenAI API Integrate OpenAI API with Odoo Editor ChatGPT GPT Odoo Connector GPT-3 Odoo Connector GPT-3.5 Odoo Connector GPT-4 Odoo Connector ChatGPT Notes ChatGPT Descriptions ChatGPT Content ChatGPT Auto Response OpenAI's GPT-3.5 OpenAI GPT-3.5 OpenAI's GPT-3.5 OpenAI's Text API Chat gpt ChatGPT Odoo Connector odoo chatbot integration Chatgpt in odoo chat gpt Integration chatgpt integration odoo",

    "description": """This module is a powerful tool that easily integrates ChatGPT into the Odoo platform. By setting up the API key and configuring preferences, users can generate intelligent responses from ChatGPT directly. The module enables users to generate quotations, provide descriptions, and receive context responses by using the response button. It also offers features like content preview, summary viewing, message sending, draft response saving, and collaboration through the ChatGPT channel. Users can also enhance communication and the capabilities of ChatGPT for improved productivity and efficiency.""",

    "depends": ['base','mail','hr'],

    "data": [
        'data/demo_data.xml',
        # 'data/mail_channel_data.xml',
        'security/ir.model.access.csv',
        'security/chatgpt_security.xml',
        'wizard/response_wizard.xml',
        'views/sh_chatgpt_config_views.xml',
        'views/res_config_settings.xml',
        'views/sh_type_of_command.xml',
        'views/sh_type_of_lanugage.xml',
        'views/sh_style.xml',
        'views/sh_length.xml',
        'views/sh_translate_to_language.xml',
        'views/res_users.xml',
        'views/sh_chatgpt_menus.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'sh_odoo_chatgpt_connector/static/src/js/mail_composer.js',
            'sh_odoo_chatgpt_connector/static/src/js/field.js',
            'sh_odoo_chatgpt_connector/static/src/xml/mail_composer.xml',
            'sh_odoo_chatgpt_connector/static/src/js/chatter.js',
            'sh_odoo_chatgpt_connector/static/src/xml/chatter.xml',
            'sh_odoo_chatgpt_connector/static/src/xml/field.xml',
            'sh_odoo_chatgpt_connector/static/src/js/sh_custom_dialog.js',
            'sh_odoo_chatgpt_connector/static/src/scss/style.scss',
            'sh_odoo_chatgpt_connector/static/src/xml/sh_custom_dialog.xml',
            'sh_odoo_chatgpt_connector/static/src/js/mail_composer_text_input.js',
            'sh_odoo_chatgpt_connector/static/src/xml/mail_composer_text_input.xml',
        ],
    },

    "installable": True,
    "auto_install": False,
    "application": True,
    "images": ["static/description/background.png", ],
    "price": "60",
    "currency": "EUR"
}
