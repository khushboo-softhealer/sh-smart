/** @odoo-module **/
import { MenuDropdown, MenuItem, NavBar } from '@web/webclient/navbar/navbar';

import { patch } from 'web.utils';
// import { ProfileSection } from "@sh_backmate_theme/js/profilesection";
import { ErrorHandler, NotUpdatable } from "@web/core/utils/components";
const getBoundingClientRect = Element.prototype.getBoundingClientRect;

const components = { NavBar };
var rpc = require("web.rpc");
var app_icon_style = 'style_1';
var backend_all_icon_style = 'backend_fontawesome_icon';
var festive_style = 'default';
var theme_style = 'default';
import  appDrawer  from './app_drawer';


var config = require("web.config");
rpc.query({
    model: 'sh.back.theme.config.settings',
    method: 'search_read',
    domain: [['id', '=', 1]],
    fields: ['theme_style','app_icon_style','backend_all_icon_style','festival_style']
}).then(function (data) {
    // console.log("KKKKKKKKKKdata",data)
    if (data) {
        if (data[0]['theme_style'] == 'style_7') {
            theme_style = 'style7';
        }
        else if (data[0]['theme_style'] == 'style_8') {
            theme_style = 'style8';
        }
         else {
            theme_style = 'default';
        }
        if (data[0]['app_icon_style']) {
            app_icon_style = data[0]['app_icon_style'];
        }
        if (data[0]['backend_all_icon_style']) {
            backend_all_icon_style = data[0]['backend_all_icon_style'];
        }
        festive_style = data[0]['festival_style']
    }
});


// console.log(" NavBar.components", NavBar.components)

// NavBar.components = { MenuDropdown, MenuItem, NotUpdatable, ErrorHandler, ProfileSection };
// console.log(" NavBar.components", NavBar.components)
patch(components.NavBar.prototype, 'sh_backmate_theme/static/src/js/navbar.js', {

    //--------------------------------------------------------------------------
    // Public
    //--------------------------------------------------------------------------

    /**
     * @override
     */

    // mobileNavbarTabs(...args) {
    //     return [...this._super(...args), {
    //         icon: 'fa fa-comments',
    //         id: 'livechat',
    //         label: this.env._t("Livechat"),
    //     }];
    // }
    setup() {

        this._super();
        if(theme_style == 'style8'){
            const acc = new appDrawer(this.menuService)
            acc.appendTo($('body')).then(function () {
                // $('.app_drawer_layout').addClass('sh_theme_model');
            });
        }
           

    },
    async adapt() {
        if (!this.root.el) {
            /** @todo do we still need this check? */
            // currently, the promise returned by 'render' is resolved at the end of
            // the rendering even if the component has been destroyed meanwhile, so we
            // may get here and have this.el unset
            return;
        }

        // ------- Initialize -------
        // Get the sectionsMenu
        const sectionsMenu = this.appSubMenus.el;
        if (!sectionsMenu) {
            // No need to continue adaptations if there is no sections menu.
            return;
        }

        // Save initial state to further check if new render has to be done.
        const initialAppSectionsExtra = this.currentAppSectionsExtra;
        const firstInitialAppSectionExtra = [...initialAppSectionsExtra].shift();
        const initialAppId = firstInitialAppSectionExtra && firstInitialAppSectionExtra.appID;

        // Restore (needed to get offset widths)
        const sections = [
            ...sectionsMenu.querySelectorAll(":scope > *:not(.o_menu_sections_more)"),
        ];
        for (const section of sections) {
            section.classList.remove("d-none");
        }
        this.currentAppSectionsExtra = [];

        // ------- Check overflowing sections -------
        // use getBoundingClientRect to get unrounded values for width in order to avoid rounding problem
        // with offsetWidth.
        const sectionsAvailableWidth = getBoundingClientRect.call(sectionsMenu).width;
        const sectionsTotalWidth = sections.reduce(
            (sum, s) => sum + getBoundingClientRect.call(s).width,
            0
        );
        // if (sectionsAvailableWidth < sectionsTotalWidth) {
            // Sections are overflowing
            // Initial width is harcoded to the width the more menu dropdown will take
            let width = 216;
            for (const section of sections) {
                if (sectionsAvailableWidth < width + section.offsetWidth) {
                    // Last sections are overflowing
                    const overflowingSections = sections.slice(sections.indexOf(section));
                    overflowingSections.forEach((s) => {
                        // Hide from normal menu
                        s.classList.add("d-none");
                        // Show inside "more" menu
                        const sectionId =
                            s.dataset.section ||
                            s.querySelector("[data-section]").getAttribute("data-section");
                        const currentAppSection = this.currentAppSections.find(
                            (appSection) => appSection.id.toString() === sectionId
                        );
                        this.currentAppSectionsExtra.push(currentAppSection);
                    });
                    break;
                }
                width += section.offsetWidth;
            }
        // }

        // ------- Final rendering -------
        const firstCurrentAppSectionExtra = [...this.currentAppSectionsExtra].shift();
        const currentAppId = firstCurrentAppSectionExtra && firstCurrentAppSectionExtra.appID;
        if (
            initialAppSectionsExtra.length === this.currentAppSectionsExtra.length &&
            initialAppId === currentAppId
        ) {
            // Do not render if more menu items stayed the same.
            return;
        }
        return this.render();
    },

    onNavBarDropdownItemSelection(menu) {
        if(window.event.shiftKey){
            localStorage.setItem("sh_add_tab",1)
        }else{
            localStorage.setItem("sh_add_tab",0)
        }
        if (menu) {
            setTimeout(() => {
                if (theme_style == 'style7') {
                    $("body").removeClass("sh_sidebar_background_enterprise");
                    $(".sh_search_container").css("display", "none");
                    $(".sh_backmate_theme_appmenu_div").removeClass("show")
                    $(".o_action_manager").removeClass("d-none");
                    $(".o_menu_brand").css("display", "block");
                    $(".full").removeClass("sidebar_arrow");
                    $(".o_menu_sections").css("display", "flex");
                }
            }, 500);
        }
        return this._super(menu);
    },
    onNavBarDropdownItemClick(ev) {
        if(ev.shiftKey){
            localStorage.setItem("sh_add_tab",1)
        }else{
            localStorage.setItem("sh_add_tab",0)
        }
        

    },
    getAppClassName(app){
        var app_name = app.xmlid
        return app_name.replaceAll('.', '_')
    },
    getIconStyle() {
        return app_icon_style;
    },
    getBackend_icon(){
        return backend_all_icon_style;
    },
    getThemeStyle(ev) {
        return theme_style;
    },
    getFestiveStyle(ev){
        return festive_style;
    },
    isMobile(ev) {
        return config.device.isMobile;
    },
    click_secondary_submenu(ev) {
        if (config.device.isMobile) {
            $(".sh_sub_menu_div").addClass("o_hidden");
        }

        $(".o_menu_sections").removeClass("show")
    },
    click_close_submenu(ev) {
        $(".sh_sub_menu_div").addClass("o_hidden");
        $(".o_menu_sections").removeClass("show")
    },
    click_mobile_toggle(ev) {
        $(".sh_sub_menu_div").removeClass("o_hidden");

    },
    click_app_toggle(ev) {
        if($(".sh_backmate_theme_appmenu_div").hasClass("sh_first_load")){
            $(".sh_backmate_theme_appmenu_div").removeClass("show")
            $(".sh_backmate_theme_appmenu_div").removeClass("sh_first_load")
        }

        if ($(".sh_backmate_theme_appmenu_div").hasClass("show")) {
            $("body").removeClass("sh_sidebar_background_enterprise");
            $(".sh_search_container").css("display", "none");

            $(".sh_backmate_theme_appmenu_div").removeClass("show")
            $(".o_action_manager").removeClass("d-none");
            $(".o_menu_brand").css("display", "block");
            $(".full").removeClass("sidebar_arrow");
            $(".o_menu_sections").css("display", "flex");
        } else {
            $(".sh_backmate_theme_appmenu_div").addClass("show")
            $("body").addClass("sh_sidebar_background_enterprise");
            $(".sh_backmate_theme_appmenu_div").css("opacity", "1");
            //$(".sh_search_container").css("display","block");
            $(".o_action_manager").addClass("d-none");
            $(".full").addClass("sidebar_arrow");
            $(".o_menu_brand").css("display", "none");
            $(".o_menu_sections").css("display", "none");
        }


    },
    open_app_drawer(ev) {
        ev.preventDefault();
                    
        if ($('.app_drawer_layout').length) {
            if ($('.sh_theme_model').length) {
                $('.app_drawer_layout').removeClass('sh_theme_model');
                $('.o_web_client').removeClass('sh_overlay_app_drawer');
            } else{
                $('.app_drawer_layout').addClass('sh_theme_model');
                $('.o_web_client').addClass('sh_overlay_app_drawer');
            }
        }else{
           if(theme_style == 'style8'){
            const acc = new appDrawer(this.menuService)
            acc.appendTo($('body')).then(function () {
                $('.app_drawer_layout').addClass('sh_theme_model');
                $('.o_web_client').addClass('sh_overlay_app_drawer');
            });
       }


           

        }

    },


});






