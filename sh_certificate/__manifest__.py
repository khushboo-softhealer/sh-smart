# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name":   "Letters and Certificates",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "license": "OPL-1",
    "category": "Extra Tools",
    "summary": """
Make Business Letter,
Make Formal Letter,
Best Employee Certificate Module,
Make Informal Letter,
Create Official Letter App,
Circular Letter,
Produce Social Letter,
Generate Employment Letter,
Make Warning Letter,
Create Offer Letter Odoo
""",
    "description": """
You probably thought of certificates/Letters only as something you received,
a document professionally produced by some distant designer,
after you need to add name and related details like
date address etc in every certificate/Letters manually
so that is the quite time consuming task.
Now with this module where can create a dynamic certificate/Letters in odoo.
here in this module provide menu where you can
create a template and then you can use it dynamically.
for example you create a template and after
you just need to select customer or partner after that
automatically fill all related details in selected template.
You can also print that in PDF file.
Using this module you can create Formal Letter,
Informal Letter, Bussiness Letter, Official Letter,
Circular Letter, Social Letter, Employment Letter,
Warning Letter, Offer Letter, etc.
Using this module you can create a certificate like
Certificate for Appreciation, Best Employee of the month,
Best Seller, Achievement, Completion, Excellence,
Professional Conformity, Professional Conformance,
Professional Air Cadet Recognition, Professional Project Completion,
Professional Job Experience, Professional Training Certificate, etc.
Generate Dynamic Letters And Certificate Odoo,
Letter And Certificate Management Odoo
Create Best Employee Certificate Module,
Make Business Letter, Make Formal Letter,
Make Informal Letter, Create Official Letter,Make Circular Letter,
Produce Social Letter, Generate Employment Letter,
Make Warning Letter, Create Offer Letter,
Produce Dynamic Template For Customer,
Create Certificate for Appreciation,
Make Achievement Certificate, Make Excellence Certificate,
Professional Certificate Maker Odoo.
Make Business Letter App, Make Formal Letter,
Create Best Employee Certificate Module,
Make Informal Letter, Create Official Letter Application,
Make Circular Letter, Produce Social Letter, Generate Employment Letter,
Make Warning Letter, Create Offer Letter, Produce Dynamic Template For Customer,
Create Certificate for Appreciation, Make Achievement Certificate,
Make Excellence Certificate, Professional Certificate Maker Odoo.
""",
    "version": "16.0.3",
    "depends": [
        "hr", "contacts",
    ],
    "application": True,
    "data": [
        "security/sh_certificate_security.xml",
        "security/ir.model.access.csv",
        "report/sh_certificate_external_templates.xml",
        "data/sh_certificate_data.xml",
        "views/sh_letter_template_views.xml",
        "views/sh_letter_views.xml",
        "views/res_partner_views.xml",
        "views/hr_employee_views.xml",
    ],
    "images": ["static/description/background.png", ],
    "live_test_url": "https://www.youtube.com/watch?v=fnzw9GbYphM&feature=youtu.be",
    "auto_install": False,
    "installable": True,
    "price": 35,
    "currency": "EUR"
}
