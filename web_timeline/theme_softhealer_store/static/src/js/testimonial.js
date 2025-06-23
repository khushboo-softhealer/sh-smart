odoo.define("theme_softhealer_store.custom_s_testimonial_post", function (require) {
    var concurrency = require("web.concurrency");
    var config = require("web.config");
    var core = require("web.core");
    var publicWidget = require("web.public.widget");

    var qweb = core.qweb;

    publicWidget.registry.sh_testimonial_snippet_s_post = publicWidget.Widget.extend({
        selector: ".js_cls_get_testimonial_s_post",
        disabledInEditableMode: true,
		read_events: {
            "click .js_cls_single_client": "_onClickSingleClient",
        },

        /**
         * @constructor
         */
        init: function () {
			this._super.apply(this, arguments);
            this._dp = new concurrency.DropPrevious();
        },
        /**
         * @override
         */
        start: function () {
			this.item_template = this.$el.attr("data-item_template") || false;

			this._dp.add(this._fetch()).then(this._render.bind(this));
            return this._super.apply(this, arguments);
        },
        /**
         * @override
         */
        destroy: function () {
            this._super(...arguments);
            this.$el.find(".js_cls_render_dynamic_testimonial_area").html("");
        },

        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        /**
         * @private
         */
        _fetch: function () {
            var loading = '<i class="js_cls_tab_pane_loading fa fa-circle-o-notch fa-spin" style="font-size:80px;width:100%;text-align:center;"></i>';

            this.$el.find(".js_cls_render_dynamic_testimonial_area").append(loading);

            return this._rpc({
                route: "/theme_softhealer_store/get_posts",
                params: {
                    item_template: this.item_template,
                },
            }).then((res) => {
                return res;
            });
        },
        /**
         * @private
         */
        _render: function (res) {
            // Add dynamic content
            this.$(".js_cls_render_dynamic_testimonial_area").replaceWith(res.data);

            $('#sh_store_testimonial_section_dyn .owl-carousel').owlCarousel({
                items:2,
                loop:true,
                margin:10,
                autoplay:true,
                autoplayTimeout:3500,
                autoplayHoverPause:true,
                responsive:{
                    0:{
                        items:1,
                        nav:true
                    },
                    600:{
                        items:2,
                        nav:false
                    },
                    800:{
                        items:2,
                        nav:false
                    },
                    1000:{
                        items:2,
                        nav:true,
                    }
                }
            
            })
			
        },

    });
    
});
