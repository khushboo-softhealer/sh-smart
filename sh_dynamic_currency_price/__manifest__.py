# Part of Softhealer Technologies.
{
    "name": "Dynamic Currency Price",
    "author": "Softhealer Technologies - Nitin",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "version": "16.0.1",
    "license": "OPL-1",
    "category": "Website",
    "summary": "Dynamic Currency Price",
    "description": """Dynamic Currency Price.""",
    "depends": ['base', 'product'],
    "data": [
        'data/ir_cron_data.xml',
        'views/res_currency_views.xml',
        'views/product_views.xml',
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
}
