Setup/Configuration after module installation
================================
- Press on Edit button
- set primary color "#564BC6"
- set Font Family -> "Outfit"
- select header on web page 
- choose 1st template for header design (title will be Global Search which will display on hover of that template)
- select footer on web page
- choose 1st template for footer design (title will be softhelaer-custom-footer which will display on hover of that template)
- enable Copyright boolean which is visible below the footer template when we select footer from web page
- press on the Save button
- activate debug mode 
- click on website -> configuration -> websites -> add website logo and add website scrolled logo
- NOTE: please follow menu sequence same as v12 as we have applied css for megmenu width based on number of menu

Megamenu setup
=================
- enable debug mode 
- go to Website => configuration menu => Menus
- create menu for which you want megamenu by presssing on NEW button
- choose particular website from more than one website in which you want megamenu
- click on menu for what you want megamenu
- after opening form view -> click boolean of "Is Mega Menu"
- add megamenu code/content in html field and press on save/apply html button

NOTE: don't perform any edition from snippet panel when you are in Home page because it will shows more than one next/prev arrow in owl carousel as it's standard behaviour. so, take care of this point.

All CSS Variable Usage/Overview
=================================
- o-color(o-color-1) => this is used for priamry color(standard odoo variable)
- var(--sh-section-heading-font-color) => main section heading text color
- var(--sh-section-heading-font-size) => main section heading text size
- var(--sh-section-heading-sub-title-font-color) => this is for main section header's text(subtitle) color
- var(--sh-website-heading-title-font-color) => this is for card box main card title text color
- var(--sh-website-normal-text-font-color) => this is for card box's paragraph type text color
- var(--sh-section-background-color) => this is for full section's background color


GO LIVE CHECKLIST
=======================
- By Default Home page will open and also on click of logo Home page should open ("No Home Menu will be there in header")
-> Company [1st exact after logo] [Megamenu]
  - About
  - Mission, Vision and Values
  - Why Softhealer Services? 
-> Our Services [2nd Megamenu]
    Two Submenu inside this "Services" & "Odoo Services"
  => Services
        - ERP Solution
        - CRM Solution
        - POS Solution
        - Web Development
        - Mobile Apps
        - Custom Software
  => Odoo Services
        - Odoo Services
        - Odoo Customization
        - Odoo Support
        - Odoo Migration
        - Odoo Implementation
        - Odoo Training 
        - Third Party App Integration
-> Solutions [3rd Megamenu]
  => Solutions
        - Readymade-Solution
        - POS Retail Solution
        - POS Sale Retail Shop-KSA-E-Invoicing
        - Appointment Management
        - Law Management System
        - Helpdesk Management
        - Pathology Lab Management System
        - Bus Booking Management
        - Visitor Management System
        - Parking Management System
        - Event Seat Booking
        - Project Management System 
        - Human Resource Management System
        - Survey Management System
        - Third Party Apps - Trello Odoo Connector
        - Third Party Apps - Taxjar Connector
-> Career [4th Menu]
-> Blogs [5th Menu]
-> Support [6th Menu]
-> Contact Us [7th Menu]