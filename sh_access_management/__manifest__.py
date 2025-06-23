# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

{
    'name' : "Access Management System",
    
    "author": "Softhealer Technologies",

    "license": "OPL-1",

    "website": "https://www.softhealer.com",

    "support": "support@softhealer.com",

    "version": "16.0.2",

    "category": "Extra Tools",

    "summary": "Access Management System Customized Menu Access Field access control Navbar button management Chatter Access Management Report action Management Multiaction views access Role-based access control Customizable user permissions User Role Management Access Control Security Policies Multi-Factor Authentication User Provisioning Access Monitoring Access Management System module User Access Control software Access Management solution Access Control System tool Manage Access Management of user access manage access All in one access control all in one access management User wise access rules user wise access control user wise access management hide menu hide any menu hide sub menu disable menu disable submenu disable any menu invisible menu hide menus usewise hide menu user wise menu hide submenus hide menus Hide field hide fields hide any field disable fields user wise fields invisible field Read only fields hide archive disable action disable delete Hide buttons hide any buttons disable button user wise buttons invisible button Hide delete hide import hide export hide actions Hide tabs hide any tabs invisible tab Hide views hide any view hide tree view hide list view hide kanban view hide graph view hide activity view hide apps invisible views hide reports disable reports user wise reports Hide chatter disable chatter invisible chatter Access rights user access roles user security access user wise accesses access rights setup Advanced Users Access Rights Manager Access Rights Management for System User Message Access Rights Model Level Access Rights Field Level Access Rights User Wise Access Rights Setup Access Rules Setup Access Rights Advanced User Access Advance User Access Rights Hide Pivot Hide Object Buttons Hide Action Button Hide Smart Buttons Hide Export Button Hide Import Button Readonly Any Field Hide Create Hide Duplicate Restrict Menu Restrict Any Menu Disable Menu Disable Any Menu Restrict Fields Restrict Any Fields Disable Fields Disable Any Fields Restrict Buttons Restrict Any Buttons Restrict Chatter Hide Send Message Hide Lognote Hide Followers Hide Activities Hide Attachments Restrict Send Message Restrict Lognote Restrict Followers Restrict Activities Restrict Attachments Hide Contacts Restrict Contacts Odoo Access Management App Read Only Users Odoo",
    
    "description": """Do you want to simplify your work environment in an organization with access rights? Then this module improves your work efficiency with Instant Access, a powerful tool that simplifies tasks. Customize who can access essential parts of your work, like Menu, Field, Navbar Button, Chatter, Report Action, and Multiaction Views. With a focus on honesty, Instant Access ensures everyone has the right permissions for their work. This access management system simplifies work processes and helps everyone collaborate better.""",

    'depends' : ['base_setup','web','base','sale_management','mail'],

    'data' : [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/data.xml',
        'views/access_manager.xml',
    ],

    'assets': {    
        'web.assets_backend': [
            'sh_access_management/static/src/js/hide_multiactions.js',
            'sh_access_management/static/src/js/chatter_container.js',
            'sh_access_management/static/src/xml/sh_create_access.xml',
            'sh_access_management/static/src/xml/chatter_container.xml',
        ],   
    },
    'demo' : [],
    'installation': True,
    'application' : True,
    'auto_install' : False,
    "images": ["static/description/background.png", ],
    "price": "91.19",
    "currency": "EUR"

}
