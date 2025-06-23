# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name":
    "Update Template To Variants",
    "author":
    "Softhealer Technologies (Kishan Patadiya)",
    "website":
    "https://www.softhealer.com",
    "support":
    "support@softhealer.com",
    "version":
    "16.0.1",
    "category":
    "Employee",
    "license": "OPL-1",
    "summary":
    "Update Variants",
    'sequence':
    10,
    "description":
    """Update Variants""",
    "depends": ["base", "sh_product_base"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/sh_product_variant_update_wizard_action.xml",
        "wizard/sh_product_variant_update_wizard_views.xml",
    ],
    "installable":
    True,
    "auto_install":
    False,
    "application":
    True,
    "price":
    "15",
    "currency":
    "EUR"
}
