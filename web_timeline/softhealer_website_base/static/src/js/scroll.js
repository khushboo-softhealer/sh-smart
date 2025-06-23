odoo.define("softhealer_website_base.back_to_top_custom_js", function (require) {
    "use strict";

    var publicWidget = require("web.public.widget");
    var animations = require('website.content.snippets.animation');
    var config = require('web.config');


    publicWidget.registry.ShWebsiteBackToTop = animations.Animation.extend({
        selector: "#wrapwrap",
        disabledInEditableMode: true,
        effects: [{
            startEvents: 'scroll',
            update: '_add_remove_back_to_top_btn_on_scroll',
        }],

        /**
         * @constructor
         */
        init: function () {
            this._super(...arguments);
            var self = this;
            this.amount_scrolled = 150;
        },

        //--------------------------------------------------------------------------
        /**
         * Called when the window is scrolled
         *
         * @private
         * @param {integer} scroll
         */
        _add_remove_back_to_top_btn_on_scroll: function (scroll) {
            var self = this;

            var wrapwrap_scroll_height = $('#wrapwrap')[0].scrollHeight;
            var body_scroll_height = $('body')[0].scrollHeight;
            var document_height = wrapwrap_scroll_height - body_scroll_height;
            var scroll_percent = (scroll / document_height) * 100;
            if (scroll_percent < 0) {
                scroll_percent = 0;
            }
            if (scroll_percent > 100) {
                scroll_percent = 100;
            }

            if(scroll_percent <= 50) {
                $(".mask-right .fill").css("transform", "rotate3d(0,0,1," + ( 360 * scroll_percent / 100) + "deg)");
                $(".mask-left .fill").css("transform", "rotate3d(0,0,1," + "0)");
            } else if( scroll_percent > 50) {
                $(".mask-left .fill").css("transform", "rotate3d(0,0,1," + (( 360 * scroll_percent / 100) - 180) * 1 + "deg)");
                $(".mask-right .fill").css("transform", "rotate3d(0,0,1," + "180deg)"); 
            }
            var $liveChat = $(document).find('.o_website_livechat_button');
            var $whatsapp = document.querySelector('#sh_website_wtsapp_contact_web') || document.querySelector('#sh_website_wtsapp_contact_mobile');
            if (scroll > self.amount_scrolled) {
                $(document).find('.js_cls_sh_website_back_to_top').addClass('active');
                if (!config.device.isMobile){
                    $(document).find('.js_cls_sh_bye_now_button').css('bottom','80px');
                    $(document).find('#sh_website_wtsapp_contact_web').css('bottom','80px');
                    $(document).find('#sh_website_wtsapp_contact_mobile').css('bottom','80px');
                    if ($whatsapp){
                        $liveChat.attr('style', 'bottom: 115px !important');
                    }
                    else{
                        $liveChat.attr('style', 'bottom: 60px !important');
                    }
                }
                else {
                    $(document).find('.js_cls_sh_bye_now_button').css('bottom','60px');
                    $(document).find('#sh_website_wtsapp_contact_web').css('bottom','60px');
                    $(document).find('#sh_website_wtsapp_contact_mobile').css('bottom','60px');
                    if ($whatsapp){
                        $liveChat.attr('style', 'bottom: 100px !important');
                    }
                    else{
                        $liveChat.attr('style', 'bottom: 60px !important');
                    }
                }
                
            } else {
                $(document).find('.js_cls_sh_website_back_to_top').removeClass('active');
                $(document).find('.js_cls_sh_bye_now_button').css('bottom','16px');
                $(document).find('#sh_website_wtsapp_contact_web').css('bottom','16px');
                $(document).find('#sh_website_wtsapp_contact_mobile').css('bottom','16px');
                if ($whatsapp){
                    $liveChat.attr('style', 'bottom: 56px !important');
                }
                else{
                    $liveChat.attr('style', 'bottom: 0px !important');
                }
            }
        },


    });


  

});


