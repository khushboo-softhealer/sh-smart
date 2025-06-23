odoo.define('theme_softhealer_store.website_sale_optional', function (require) {
    'use strict';

    var ajax = require('web.ajax');
    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var publicWidget = require('web.public.widget');
    require('website_sale_options.website_sale');

    publicWidget.registry.WebsiteSale.include({

        /**
     * Submits the form with additional parameters
     * - lang
     * - product_custom_attribute_values: The products custom variant values
     *
     * @private
     * @param {Boolean} goToShop Triggers a page refresh to the url "shop/cart"
     */
    _onModalSubmit: function (goToShop) {
        const $product = $('#product_detail');
        let currency;
        if ($product.length) {
            currency = $product.data('product-tracking-info')['currency'];
        } else {
            // Add to cart from /shop page
            currency = this.$('[itemprop="priceCurrency"]').first().text();
        }
        const productsTrackingInfo = [];
        this.$('.js_product.in_cart').each((i, el) => {
            productsTrackingInfo.push({
                'item_id': el.getElementsByClassName('product_id')[0].value,
                'item_name': el.getElementsByClassName('product_display_name')[0].textContent,
                'quantity': el.getElementsByClassName('js_quantity')[0].value,
                'currency': currency,
                'price': el.getElementsByClassName('oe_price')[0].getElementsByClassName('oe_currency_value')[0].textContent,
            });
        });
        if (productsTrackingInfo) {
            this.$el.trigger('add_to_cart_event', productsTrackingInfo);
        }

        this.optionalProductsModal.getAndCreateSelectedProducts()
            .then((products) => {
                const productAndOptions = JSON.stringify(products);
                ajax.post('/shop/cart/update_option', {
                    product_and_options: productAndOptions,
                    ...this._getOptionalCombinationInfoParam()
                }).then(function (quantity) {
                    
                    if(quantity.indexOf("sh_blog_post_not_exists") != -1){
                        var quantity = JSON.parse(quantity.replace(/'/g, '"'));
                    }
                    
                    if (quantity.sh_blog_post_not_exists){
                        var dialog = new Dialog(this, {
                            title: "Product Information",
                            $content: $('<p>' + "Apologies for any inconvenience. This app is currently in the development phase for "+quantity.product_varsion+ ". If you need it for an earlier version, please don't hesitate to contact us." + '</p>'),
                            buttons: false,
                        });
                        dialog.open();
                        dialog.opened(function () {
                            dialog.$footer.addClass('d-none')
                        })
                    }
                    if (!quantity.sh_blog_post_not_exists){
                        if (goToShop) {
                            window.location.pathname = "/shop/cart";
                        }
                        const $quantity = $(".my_cart_quantity");
                        $quantity.parent().parent().removeClass('d-none');
                        $quantity.text(quantity).hide().fadeIn(600);
                        sessionStorage.setItem('website_sale_cart_quantity', quantity);
                    }
                    }).then(()=>{
                        this._getCombinationInfo($.Event('click', {target: $("#add_to_cart")}));
                    });
            });
    },

    });
});