odoo.define('theme_mobiheal_website.mobihealFooterJs', function (require) {
    'use strict';
    
    var publicWidget = require('web.public.widget');
    
    publicWidget.registry.mobihealFooterJsScrollJs = publicWidget.Widget.extend({
        selector: '#wrapwrap',
        disabledInEditableMode: true,

        events: {
            "click .js_cls_sh_website_back_to_top": "_onClickScrollToTop",
        },
        /**
         * @override
         */
        start: function () {
            this._super.apply(this, arguments);
            const currentUrl = new URL(window.location.href);
            
            // Team Section
            var param_team_section = currentUrl.searchParams.get("team_section");
            if (param_team_section && param_team_section == 1){
                $('html, body').animate({
                    scrollTop: $(".js_cls_team_section").offset().top
                }, 1500);
            }

            // Service Section 1
            var param_service_section = currentUrl.searchParams.get("service_section");
            if (param_service_section && param_service_section == 1){
                $('html, body').animate({
                    scrollTop: $(".js_cls_mb_service_section_1").offset().top
                }, 1500);
            }
            // Service Section 2
            var param_service_section = currentUrl.searchParams.get("service_section");
            if (param_service_section && param_service_section == 2){
                $('html, body').animate({
                    scrollTop: $(".js_cls_mb_service_section_2").offset().top
                }, 1500);
            }
        },
        
        _onClickScrollToTop: function (ev) {
			ev.stopPropagation();
			ev.preventDefault();

			$('#wrapwrap').stop().animate({
				scrollTop: 0
			}, 2000, 'easeInOutExpo');
		},
    });
});