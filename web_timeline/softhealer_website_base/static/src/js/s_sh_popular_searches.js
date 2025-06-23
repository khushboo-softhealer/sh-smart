odoo.define('softhealer_website_base.ShPopularSearches', function (require) {
    'use strict';

    const publicWidget = require('web.public.widget');
    const core = require('web.core');

    const ShPopularSearches = publicWidget.Widget.extend({
        selector: '.s_sh_website_popular_searches',
        disabledInEditableMode: false,
        /**
         * @override
         */
        init: function () {
            this._super.apply(this, arguments);
            this.data = [];
            this.renderedContent = '';
            this.template_key = 'sh_website.s_sh_website_popular_search.badges';
        },
        /**
         * in fetch data request RPC.
         * @override
         */
        willStart: function () {
            return this._super.apply(this, arguments).then(
                () => Promise.all([
                    this._fetchData(),
                ])
            );
        },
        /**
         * After RPC calls are complete call to render
         * @override
         */
        start: function () {
            return this._super.apply(this, arguments).then(
                () => Promise.all([
                    this._render(),
                ])
            );
        },
        /**
         *  Clear snippets content
         * @override
         */
        destroy: function () {
            this._clearContent();
            this._super.apply(this, arguments);
        },
        /**
         * Fetches the popular searches data.
         * @private
         */
        async _fetchData() {
            const nodeData = this.el.dataset;
            const minSearchCount = nodeData.minSearchCount !== undefined && !isNaN(nodeData.minSearchCount) ? parseInt(nodeData.minSearchCount) : 100;
            this.data = await this._rpc({
                'route': '/sh_website/popular_searches',
                'params': { 'min_search_count': minSearchCount }
            });
        },
        /**
         * render qweb for popular searches.
         * @private
         */
        _prepareContent: function () {
            this.renderedContent = core.qweb.render(this.template_key, { popularSearches: this.data });
        },
        /**
         * @private
         */
        _clearContent: function () {
            const $templateArea = this.$el.find('.popular_search_snippet_template');
            $templateArea.html('');
        },
        /**
         *
         * @private
         */
        _render: function () {
            this._prepareContent();
            this._renderContent();
        },
        /**
         * Add qweb on popular search snippet template
         * @private
         */
        _renderContent: function () {
            const $templateArea = this.$el.find('.popular_search_snippet_template');
            $templateArea.html(this.renderedContent);
        },
    });

    publicWidget.registry.ShPopularSearches = ShPopularSearches;
});