odoo.define('sh_website_dynamic_content.s_sh_dynamic_content', function (require) {
    'use strict';

    const publicWidget = require('web.public.widget');
    var wUtils = require('website.utils');
    const { Markup } = require('web.utils');
    const { qweb, _t } = require('web.core')
    const ShDynamicContent = publicWidget.Widget.extend({
        selector: '.s_sh_dynamic_content',
        disabledInEditableMode: false,
        /**
         * @override
         */
        init: function () {
            this._super.apply(this, arguments);
            this.contentHtml = undefined;
            this.defaultContent = undefined
        },
        /**
         *
         * @override
         */
        willStart: function () {
            return this._super.apply(this, arguments).then(
                () => Promise.all([
                    this.defaultContent = this.$el.html(),
                    this._fetchData(),
                ])
            );
        },
        /**
         *
         * @override
         */
        start: function () {
            return this._super.apply(this, arguments)
                .then(() => {
                    this._render();
                })
        },
        /**
         * Fetches the data.
         * @private
         */
        async _fetchData() {
            var self = this;
            const shContentId = parseInt(this.$el.get(0).dataset.shContentId !== undefined && !isNaN(this.$el.get(0).dataset.shContentId) ? this.$el.get(0).dataset.shContentId : 0);
            return this._rpc({
                route: `/sh_website_dynamic_content/get_content/${encodeURIComponent(shContentId !== -1 ? shContentId : 0)}`
            }).then(function (content) {
                if (content !== undefined) {
                    self.contentHtml = content;
                }
            });
        },
        /**
         *
         * @private
         */
        async _render() {
            var $templateArea = this.$el;
            const content = qweb.render('sh_website_dynamic_content.s_sh_dynamic_content.default_content', {
                content: Markup(_t(this.contentHtml)),
            });
            // console.log('-------content------>',content);
            $templateArea.html(content);
        }
    });

    publicWidget.registry.ShDynamicContent = ShDynamicContent;

});