Setup/Configuration after theme installation
================================
- Press on Edit button
- set primary color "#564BC6"
- set Font Family -> "Outfit"
- select header on web page 
- choose 1st template for header design (title will be softhealer-custom-header which will display on hover of that template)
- select footer on web page
- choose 1st template for footer design (title will be softhelaer-custom-footer which will display on hover of that template)
- press on the Save button
- activate debug mode 
- click on website -> configuration -> websites -> add website logo
- Home page's will be open on click of website's logo.

Megamenu setup
=================
- enable debug mode [setup megamenu for Our Services and Categories]
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

Dynamic Content Snippet
==========================
- click on Website => Configuration => Dynamic Content menu
- add xml code from backend by creating it
- 

Home Page Setup 
=======================
- we can set different three types of banner for home page based on offer(code is already ready just add that code from backend)
- for enable popular search first go to Website -> Configuration -> Settings 
- find "Website Popular Searches" => Enable Website Popular Searches
- after setup popular search section and search anything in global search or shop page search.
- go to Webistes => Configurations => Popular Searches => tick for Is Published which you want to display
- add Testimonial content from backend by click on Website => Configuration => Testimonial

Shop page Setup
======================
- select shop screen by click on categories part
- choose "Categories" to "Top" this option
- choose "Attributes" to "Left" this option

Product Detail Page Setup (alternative product section)
===========================
- Website -> eCommerce from navbar
- Click on Products 
- Click on "Sales" tab
- Add Alternative Products Field data

Contact US Page
==========================
- NOTE : Enable "Lead" option from backend for contact us form

Categories Megamenu Setup
=========================
- <div class="sh_mega_menu js_cls_sh_store_megamenu_categories_wrapper">
    <div class="container">
        <div class="row js_cls_dyn_row">
        </div>
    </div>
  </div>
- add this code in HTML field from backend
- go to the eCommerce menu -> eCommerce Categories
- Create Catrgories if not there otherwise no need to create
- ADD SVG code for menus
- Choose boolean(tick box) for App/Themes

GO LIVE CHECKLIST
=======================
- By Default Home page will open and also on click of logo Home page should open ("No Home Menu will be there in header")
-> About Us [2nd Menu] [exact after logo]
-> Categories [3rd Megamenu]
  => Apps
  - Accounting
  - Discuss
  - Document Management
  - Ecommerce
  - Industries
  - Manufacturing
  - Marketing
  - Point of Sale
  - Productivity
  - Project
  - Purchases
  - Sales
  - Warehouse
  - Website
  - Extra Tool

  => Themes
  - Backend
  - Corporate
  - Ecommerce

-> Our Services [4th Megamenu]
   => Add megamenu content same as softhealer website. so, take code from theme_softhealer_website

-> Shop [5th Menu]
-> Blogs [6th Menu]
-> Support [7th Menu]
-> Contact Us [8th Menu]