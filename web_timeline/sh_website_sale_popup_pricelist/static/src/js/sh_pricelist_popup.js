odoo.define('sh_website_sale_popup_pricelist.ShWebsitePricelist', function (require) {
    'use strict';

    const { qweb } = require('web.core');
    var publicWidget = require('web.public.widget');
    var Dialog = require('web.Dialog');

    var ShPriceListDialog = Dialog.extend({
        willStart: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                // Added Class in modal dialog div For SCSS.
                self.$modal.find('.modal-dialog').addClass('sh_cls_wsale_price_list_popup');
            });
        }
    });

    publicWidget.registry.ShWebsitePricelist = publicWidget.Widget.extend({
        selector: "#wrapwrap[data-show-website-sale-pricelist-popup='True']",
        
        /**
        * @override
        */
        willStart: function () {
            return this._super.apply(this, arguments).then(
                () => Promise.all([
                    this._checkPricelistPopupConfig(),
                ])
            );
        },

        /**
         * Call _rpc for get value of pricelist.
         * Add show popup.
         * @private
         */
        _showPopup: async function () {
            var stored_pricelist = localStorage.getItem('sh_website_sale_popup_current_pl');
            this._rpc({
                route: "/sh_website_sale_popup_pricelist/get_pricelist_available_for_popup",
                params: {
                    'stored_pricelist':stored_pricelist,
                },
            }).then(function (pricelist) {
                if (pricelist.length > 1) {
                    var $content = qweb.render('ShPricelistDialog', {
                        ShWebsiteSalePriceLists: pricelist
                    });
                    new ShPriceListDialog(this, {
                        // renderHeader: false,
                        title:"Select Currency",
                        renderFooter: false,
                        $content: $content,
                        dialogClass: "p-0"
                    }).open();
                }
            });
        },

        /**
         * @private
        */
        _checkPricelistPopupConfig: async function () {
            if (this.$el[0].dataset.showWebsiteSalePricelistPopup !== undefined && this.$el[0].dataset.showWebsiteSalePricelistPopup === 'True') {
                var $hiddenUrl = this.$el.find("input[name='sh_website_sale_popup_pricelist_pages_url']")
                var popupPages = $hiddenUrl.length ? $hiddenUrl[0].value : ''
                var re = /\s*(?:,|$)\s*/;

                // CASE 1: SHOW POPUP IN ALL PAGES IF PAGES URL FIELD IS BLANK IN WEBSITE SETTING.
                if (!popupPages.length) {
                    this._showPopup();
                }
                // CASE 2: SHOW POPUP IN SPECIFIC PAGE IF PAGES URL GIVEN IN WEBSITE SETTINGS.
                else {
                    var url = popupPages.trim().split(re).filter(url => url.length > 0 && url.startsWith("/") && window.location.href.includes(url.toLowerCase()));
                    if (url.length) {
                        this._showPopup();
                    }
                }
            }
        },
        
    })

    
});