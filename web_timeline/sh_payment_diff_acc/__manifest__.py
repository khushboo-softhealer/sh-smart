# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name" : "Payment Difference Account",
    "author" : "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com", 
    "category": "",
    "summary": "",       
    "license": "OPL-1",
    "version":"16.0.1",
    "depends" : [
                    "sh_import_paypal_data"
                ],
    "data" : [

            'security/ir.model.access.csv',
            'wizard/received_amount_wizard.xml',
            'views/res_config_settings.xml',
            'views/account_payment.xml',

            ],
    
    "images": ['',],
    "live_test_url": "", 
    "application" : True,             
    "auto_install": False,
    "installable" : True,
    "price": 40,
    "currency": "EUR",
}
