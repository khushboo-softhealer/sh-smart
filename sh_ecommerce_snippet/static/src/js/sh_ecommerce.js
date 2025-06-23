odoo.define("sh_ecommerce_snippet.s_product", function (require) {
    var concurrency = require("web.concurrency");
    var config = require("web.config");
    var core = require("web.core");
    var publicWidget = require("web.public.widget");
    var utils = require("web.utils");
    var wSaleUtils = require("website_sale.utils");

    var qweb = core.qweb;

    publicWidget.registry.sh_product_snippet_s_product = publicWidget.Widget.extend({
        selector: ".js_cls_get_sh_ecom_s_product",
        disabledInEditableMode: true,
        read_events: {
            "click .js_cls_tab_a": "_onClickTab",
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
            this.column_class = this.$el.attr("data-column_class") || "col-md-4";
            this.owl_item_mobile = this.$el.attr("data-owl_item_mobile") || 1;
            this.owl_item_tablet = this.$el.attr("data-owl_item_tablet") || 3;
            this.single_tab_item_template = this.$el.attr("data-single_tab_item_template") || false;

            this.order = this.$el.attr("data-order") || "";
            this.limit = parseInt(this.$el.attr("data-limit")) || false;
            this.displayAddtocart = !!this.$el.data("displayAddtocart");
            this.displayDescription = !!this.$el.data("displayDescription");
            this.displayWishlist = !!this.$el.data("displayWishlist");
            this.displaySaleprice = !!this.$el.data("displaySaleprice");
            this.displayRating = !!this.$el.data("displayRating");
            this.displayCategory = !!this.$el.data("displayCategory");

            this.categs_ids = [];
            this.filter_id = parseInt(this.$el.data("filterId")) || false;

            //get snippet options
            var className = this.$el.attr("class");
            if (className) {
                //for category
                var categs_ids = [];
                var classArray = className.split(" ");
                var arrayLength = classArray.length;
                for (var i = 0; i < arrayLength; i++) {
                    var js_categ_id = classArray[i].match("sh_categ_(.*)_cend");
                    if (js_categ_id && js_categ_id.length == 2) {
                        categs_ids.push(parseInt(js_categ_id[1]));
                    }
                }
                this.categs_ids = categs_ids;
            }

            this._dp.add(this._fetch()).then(this._render.bind(this));
            return this._super.apply(this, arguments);
        },
        /**
         * @override
         */
        destroy: function () {
            this._super(...arguments);
            this.$el.find(".js_cls_render_dynamic_product_area").html("");
        },

        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        /**
         * @private
         */
        _fetch: function () {
            var loading = '<i class="js_cls_tab_pane_loading fa fa-circle-o-notch fa-spin" style="font-size:40px;width:100%;text-align:center;"></i>';

            this.$el.find(".js_cls_render_dynamic_product_area").append(loading);

            return this._rpc({
                route: "/sh_ecommerce_snippet/get_products",
                params: {
                    item_template: this.item_template,
                    categs_ids: this.categs_ids,
                    filter_id: this.filter_id,
                    options: {
                        order: this.order,
                        limit: this.limit,
                        display_add_to_cart: this.displayAddtocart,
                        display_description: this.displayDescription,
                        display_wishlist: this.displayWishlist,
                        display_price: this.displaySaleprice,
                        display_rating: this.displayRating,
                        display_category: this.displayCategory,
                        column_class: this.column_class,
                    },
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
            this.$(".js_cls_render_dynamic_product_area").html(res.data);

            //refresh owl
            if (res.is_show_slider_local) {
                this.$(".js_cls_tab_pane_content").owlCarousel({
                    items: res.items,
                    autoplay: res.autoplay,
                    speed: res.speed,
                    loop: res.loop,
                    nav: res.nav,
                    margin:15,
                    responsive: {
                        0: {
                            items: this.owl_item_mobile,
                        },
                        600: {
                            items: this.owl_item_tablet,
                        },
                        1000: {
                            items: res.items,
                        },
                    },
                });
            }
        },

        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------

        /**
         * Add product to cart and reload the carousel.
         * @private
         * @param {Event} ev
         */
        _onClickTab: function (ev) {
            var self = this;
            var tab_pane_id = $(ev.currentTarget).attr("href");
            var tab_id = parseInt($(ev.currentTarget).attr("data-tab_id")) || false;
            var categ_id = parseInt($(ev.currentTarget).attr("data-categ_id")) || false;
            

            var $tab_pane_content = self.$el.find(tab_pane_id).find(".js_cls_tab_pane_content");

            var is_data_loaded = $tab_pane_content.attr("data-loaded");
            
            if (is_data_loaded) {
                return;
            }

            var loading = '<i class="js_cls_tab_pane_loading fa fa-circle-o-notch fa-spin" style="font-size:40px;width:100%;text-align:center;"></i>';
            var $already_loading = $tab_pane_content.find(".js_cls_tab_pane_loading");
            if ($already_loading.length) {
                $already_loading.replaceWith(loading);
            } else {
                $tab_pane_content.prepend(loading);
            }

            this._rpc({
                route: "/sh_ecommerce_snippet/get_products",
                params: {
                    item_template: this.single_tab_item_template,
                    categs_ids: this.categs_ids,
                    filter_id: this.filter_id,
                    options: {
                        order: this.order,
                        limit: this.limit,
                        display_add_to_cart: this.displayAddtocart,
                        display_description: this.displayDescription,
                        display_wishlist: this.displayWishlist,
                        display_price: this.displaySaleprice,
                        display_rating: this.displayRating,
                        display_category: this.displayCategory,
                        tab_id: tab_id,
                        column_class: this.column_class,
                    },
                },
            }).then(function (res) {
                $tab_pane_content.html(res.data);
                $tab_pane_content.attr("data-loaded", true);

                //refresh owl
                if (res.is_show_slider_local) {
                    $tab_pane_content.owlCarousel("destroy");

                    $tab_pane_content.owlCarousel({
                        items: res.items,
                        autoplay: res.autoplay,
                        speed: res.speed,
                        loop: res.loop,
                        nav: res.nav,
                        margin:15,
                        responsive: {
                            0: {
                                items: self.owl_item_mobile,
                            },
                            600: {
                                items: self.owl_item_tablet,
                            },
                            1000: {
                                items: res.items,
                            },
                        },
                    });
                }
            });


        },
    });
});
