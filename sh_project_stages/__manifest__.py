# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name":
    "Auto Project Task Stages",
    "author":
    "Softhealer Technologies",
    "website":
    "https://www.softhealer.com",
    "license": "OPL-1",
    "support":
    "support@softhealer.com",
    "version":
    "12.0.1",
    "category":
    "Project",
    "summary":
    "Project Task Stages, Manage Phases In Project, Maintain Project Task Stages,Project Stage Management Module, Handle Different Project Phases, Different Stages In Different Projects Task App Odoo",
    "description":
    """Stages are the most important things in the project. In this module, you can define project task wise stages. You can create different project task stages for different projects.""",
    "depends": ['project','sh_product_base'],
    "data": [
        'security/ir.model.access.csv',
        'views/mass_stage_update_action.xml',
        'views/mass_stage_update_wizard_view.xml',
    ],
    'images': [
        'static/description/background.png',
    ],
    "installable":
    True,
    "auto_install":
    False,
    "application":
    True,
    "price":
    15,
    "currency":
    "EUR"
}
