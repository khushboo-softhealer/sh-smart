# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "SH backend",
    
    "author": "Softhealer Technologies Pvt.Ltd",
    
    "website": "https://www.softhealer.com",    
    
    "support": "info@softhealer.com",    
    
    "version": "16.0.2",
    
    "category": "Extra Tools",

    "license": "OPL-1",
    
    "summary": "Backend Blog Description",    

    "description": """
""", 
    
    "depends": ['base', 'crm', 'product','sale_management','mail','website',
                'hr_expense','website_blog','website_sale','project','sh_product_base', 'sh_message'],
    
    "data": [
            'security/security_groups.xml',
            'security/ir.model.access.csv',
            'data/product_tempalte_cron.xml',

            'wizard/sh_res_user_wizard_views.xml',
            'wizard/sh_assign_edition_wizard_views.xml',
            'wizard/sh_assign_scale_wizard_views.xml',

            #'views/product_view_inherit.xml',
            'data/product_template_actions.xml',
            'data/product_product_actions.xml',
            'data/project_task_actions.xml',

            'wizard/sh_assign_new_version_wizard_views.xml',
            'wizard/sh_update_git_repo_wizard_views.xml',

            'views/sale_order_views.xml',
            'views/product_template.xml',
            'views/crm_lead_inherit_view.xml',
            'views/sh_pricelist_view.xml',

            'views/website_product_category.xml',
            'views/res_partner_view.xml',

            'views/menu_view.xml',
            'views/product_category.xml',
            'views/app_menu_views.xml',

            'wizard/sh_product_extra_image_views.xml',
            'views/product_extra_image.xml',
            'views/sh_assign_employee.xml',
            'wizard/sh_update_category_wizard_views.xml',
            'wizard/sh_update_ecommerce_category_wizard_views.xml',
            'wizard/sh_update_product_type_wizard_views.xml',
            'views/product_image.xml',            

    ],     
    
    "installable": True,
    "application": True,   
    "auto_install": False,
    
}
