# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "All In One Sale Reports",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Sales",
    "license": "OPL-1",
    "summary": """Sales Report Based On Analysis, Compare Customer By Sales Report Module, Compare Products Based On Selling, Salesperson Wise Payment Report, Sales Report By Customer And Sales Person, Sales Report By Tax, All in one sales report Odoo""",
    "description": """ All in one sale report useful to provide different sales and invoice reports to do analysis. A sales analysis report shows the trends that occur in a company's sales volume over time. In its most basic form, a sales analysis report shows whether sales are increasing or declining. At any time during the fiscal year, sales managers may analyze the trends in the report to determine the best course of action. Sales reports are a record of sales activity over a particular period. These reports detail what reps have been up to, reveal whether the team is on track to meet its quota, and alert management to any potential issues.
Sales Report Based On Analysis, Compare Customer By Sales Report Module, Compare Products Based On Selling, Salesperson Wise Payment Report, Sales Report By Customer And Sales Person, Sales Report By Tax, Sale Report By Date And Time Odoo """,
    "version": "16.0.1",
    "depends": [
                "sale_management",
    ],
    "application": True,
    "data": [
        "security/sh_sale_reports_groups.xml",
        "sh_sale_details_report/security/ir.model.access.csv",
        "sh_sale_details_report/wizard/sh_sale_details_report_wizard_views.xml",
        "sh_sale_details_report/report/sh_sale_details_templates.xml",

        "sh_sale_report_salesperson/security/ir.model.access.csv",
        "sh_sale_report_salesperson/wizard/sh_report_salesperson_wizard_views.xml",
        "sh_sale_report_salesperson/report/sh_salesperson_templates.xml",

        "sh_top_customers/security/ir.model.access.csv",
        "sh_top_customers/wizard/sh_top_customer_wizard_views.xml",
        "sh_top_customers/report/sh_top_customer_templates.xml",

        "sh_top_selling_product/security/ir.model.access.csv",
        "sh_top_selling_product/wizard/sh_top_selling_wizard_views.xml",
        "sh_top_selling_product/views/sh_top_selling_views.xml",
        "sh_top_selling_product/report/sh_top_selling_product_templates.xml",
        
        "sh_payment_report/security/sh_payment_report_groups.xml",
        "sh_payment_report/security/ir.model.access.csv",
        "sh_payment_report/wizard/sh_payment_report_wizard_views.xml",
        "sh_payment_report/report/sh_payment_report_templates.xml",
        
        "sh_day_wise_sales/security/ir.model.access.csv",
        "sh_day_wise_sales/wizard/sh_day_wise_sales_wizard_views.xml",
        "sh_day_wise_sales/report/sh_day_wise_sales_report_templates.xml",
        
        "sh_sale_invoice_summary/security/ir.model.access.csv",
        "sh_sale_invoice_summary/report/sh_sale_invoice_summary_templates.xml",
        "sh_sale_invoice_summary/wizard/sh_sale_invoice_summary_wizard_views.xml",
        
        "sh_customer_sales_analysis/security/ir.model.access.csv",
        "sh_customer_sales_analysis/report/sh_customer_sales_analysis_templates.xml",
        "sh_customer_sales_analysis/wizard/sh_customer_sales_analysis_wizard_views.xml",
        
        "sh_sale_product_profit/security/ir.model.access.csv",
        "sh_sale_product_profit/report/sh_sale_product_profit_templates.xml",
        "sh_sale_product_profit/wizard/sh_sale_product_profit_wizard_views.xml",
        
        "sh_sale_by_category/security/ir.model.access.csv",
        "sh_sale_by_category/report/sh_sale_by_category_templates.xml",
        "sh_sale_by_category/wizard/sh_sale_by_category_wizard_views.xml",
        
        "sh_product_sales_indent/security/ir.model.access.csv",
        "sh_product_sales_indent/report/sh_sale_product_indent_templates.xml",
        "sh_product_sales_indent/wizard/sh_sale_product_indent_wizard_views.xml",
        
        'sh_sale_sector_report/security/ir.model.access.csv',
        'sh_sale_sector_report/wizard/sh_sector_report_wizard_views.xml',
        'sh_sale_sector_report/views/sh_sector_views.xml',
        
        'sh_sale_product_attribute_report/security/ir.model.access.csv',
        'sh_sale_product_attribute_report/report/sh_sale_product_attribute_templates.xml',
        'sh_sale_product_attribute_report/wizard/sh_sale_product_attribute_wizard_views.xml',

    ],
    "images": ["static/description/background.gif", ],
    "license": "OPL-1",
    "auto_install": False,
    "installable": True,
    "price": 100,
    "currency": "EUR"
}
