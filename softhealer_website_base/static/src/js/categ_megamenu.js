odoo.define('theme_softhealer_store.store_megamenu_for_categories', function (require) {

    var publicWidget = require('web.public.widget');
    var concurrency = require("web.concurrency");
    var ajax = require('web.ajax');

    publicWidget.registry.store_megamenu_for_categories = publicWidget.Widget.extend({
        selector: ".js_cls_sh_store_megamenu_categories_wrapper",
        disabledInEditableMode: true,

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
            this._dp.add(this._fetch()).then(this._render.bind(this));
            return this._super.apply(this, arguments);
        },

        /**
         * @private
         */
        _fetch: function () {
			// Add dynamic content
            return this._rpc({
                route: "/softhealer_website_base/get_app_theme_categories",
            }).then((res) => {
                return res;
            });
        },

        /**
         * @private
         */
        _render: function (res) {
            this.$(".js_cls_dyn_row").html(res.data);
        },
    });
});



