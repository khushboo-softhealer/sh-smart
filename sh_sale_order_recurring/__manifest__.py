# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Sale Order Recurring",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "license": "OPL-1",
    "category": "Sales",
    "summary": """
sales recurring orders app, repeat order recurring module,
generate monthly recurring, weekly regular order recurring,
manually recurring order odoo
""",
    "description": """
You can make recurring order for your regular customers using this module.
For example, a consumer could set up an order
to have particular goods in every three months.
you can make recurring order using this module would
let this purchase happen automatically on a regular schedule.
You can also make recurring order manually from recurring order.
You can set the schedule time.
sales recurring orders app, repeat order recurring module,
generate monthly recurring, weekly regular order recurring,
manually recurring order odoo                   
""",
    "version": "16.0.2",
    "depends": ["base", "base_setup", "sale","sale_management","utm","sh_project_task_base","sh_helpdesk","sh_project_mgmt"],
    "application": True,
    "data": [
        "security/sh_sale_recurring_security.xml",
        # "security/ir.model.access.csv",
        # "data/ir_sequence.xml",
        "data/ir_cron_data.xml",
        # "views/res_config_settings_views.xml",
        # "views/sh_sale_recurring_view.xml",
        "views/sale_order_views.xml",
        # "views/sale_recurring_line_views.xml",
    ],
    "images": ["static/description/background.png", ],
    "live_test_url": "https://youtu.be/BflpV7WZDuk",
    "auto_install": False,
    "installable": True,
    "price": 36.8,
    "currency": "EUR"
}
