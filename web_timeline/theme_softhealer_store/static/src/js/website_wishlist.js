odoo.define('theme_softhealer_store.website_sale_wishlist', function (require) {
    'use strict';
    
    var publicWidget = require('web.public.widget');
    var Dialog = require('web.Dialog');
    var wSaleUtils = require('website_sale.utils');

    publicWidget.registry.ProductWishlist.include({

        /**
         * @private
         */
        _addToCart: async function (productID, qty) {
            self.dialog_opened = false
            const $tr = this.$(`tr[data-product-id="${productID}"]`);
            const productTrackingInfo = $tr.data('product-tracking-info');
            if (productTrackingInfo) {
                productTrackingInfo.quantity = qty;
                $tr.trigger('add_to_cart_event', [productTrackingInfo]);
            }
            return this._rpc({
                route: "/shop/cart/update_json",
                params: this._getCartUpdateJsonParams(productID, qty),
            }).then(function (data) {
                if (data.sh_blog_post_not_exists){
                    self.dialog_opened = true
                    var dialog = new Dialog(this, {
                        title: "Product Information",
                        $content: $('<p>' + "Apologies for any inconvenience. This app is currently in the development phase for "+data.product_varsion+ ". If you need it for an earlier version, please don't hesitate to contact us." + '</p>'),
                        buttons: false,
                    });
                    dialog.open();
                    dialog.opened(function () {
                        dialog.$footer.addClass('d-none')
                    })
                }
                if (!data.sh_blog_post_not_exists){
                    self.dialog_opened = false
                    sessionStorage.setItem('website_sale_cart_quantity', data.cart_quantity);
                    wSaleUtils.updateCartNavBar(data);
                    wSaleUtils.showWarning(data.warning);
                }
            });
        },


        /**
         * @private
         */
        _addOrMoveWish: async function (e) {
            var $navButton = $('header .o_wsale_my_cart').first();
            var tr = $(e.currentTarget).parents('tr');
            var product = tr.data('product-id');
            $('.o_wsale_my_cart').removeClass('d-none');
            wSaleUtils.animateClone($navButton, tr, 25, 40);

            if ($('#b2b_wish').is(':checked')) {
                return this._addToCart(product, tr.find('add_qty').val() || 1);
            } else {
                var adding_deffered = await this._addToCart(product, tr.find('add_qty').val() || 1);
                if(!self.dialog_opened){
                    this._removeWish(e, adding_deffered);
                }
                return adding_deffered;
            }
        },

    });
});