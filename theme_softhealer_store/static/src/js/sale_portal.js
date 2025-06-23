odoo.define('theme_softhealer_store.sale_portal_template', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');

    publicWidget.registry.sale_portal_template = publicWidget.Widget.extend({
        selector: "#portal_sale_content tbody.sale_tbody",
        disabledInEditableMode: true,
		events: {
            "click .js_cls_sale_portal_tmpl_download_btn": "_onClickSalePortalLines",
        },

        _onClickSalePortalLines: function(ev){
            ev.stopPropagation();
			ev.preventDefault();
            var $downloadBtn = $(ev.currentTarget);
            var productId = $downloadBtn.data('line_product_id');
            var saleOrderId = $downloadBtn.data('sale_order_id');
            var accessToken = $downloadBtn.parents('#sales_order_table').data('token')

            return this._rpc({
                route: "/theme_softhealer_store/sh_get_app_data",
                params: {
                    product_id:productId,
                    sale_order_id:saleOrderId,
                    access_token:accessToken
                },
            })
        }
    });        
});