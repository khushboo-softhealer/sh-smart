# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Create Invoice from Timesheet",
    "author": "Softhealer Technologies(Nirali  Dholaria)",
    "website": "http://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "HR",
    "license": "OPL-1",
    "summary": """
 
  Invoice From Timesheet Module, Track Employee Project Detail App, Manage More Project One Invoice, Customer Invoice From Timesheet, Generate Invoice From Timesheet Odoo

""",
    "description": """A timesheet is a method for recording and tracking the amount of an employee’s time spent on each project. This module provides a feature to create an invoice from the timesheet. Timesheet invoice ensures payments are received much faster and the inconvenience of missed bills is eliminated because you provide all the stuff like details about projects, spent time, date of the project in one invoice so it's very easy for a client to understand about his project. Also if any customer has more than one project so you can create only one invoice of all the projects just enable a 'Group by Customer'.
 Generate Invoice From Timesheet Odoo, Timesheet Invoice Maker Odoo
 
 Create Invoice From Timesheet Module, Track Employee Project Spent Time, Manage One Invoice From More Project, Make Customer Invoice From Timesheet, Generate Invoice From Timesheet Odoo
  Invoice From Timesheet Module, Track Employee Project Detail App, Manage More Project One Invoice, Customer Invoice From Timesheet, Generate Invoice From Timesheet Odoo

""",
    "version": "16.0.1",
    "depends": [
        "base",
        "sale_management",
        "account",
        "hr",
        "sale_timesheet",
    ],

    "data": [
        "views/project_config_settings.xml",
        "views/sh_project_views.xml",
        'wizard/sh_invoice_timesheet_wizard_views.xml',
    ],
    "images": ["static/description/background.png", ],
    "live_test_url": "https://www.youtube.com/watch?v=Kf5vCebQje4&feature=youtu.be",
    "application": True,
    "auto_install": False,
    "installable": True,
    "price": 30,
    "currency": "EUR"
}
