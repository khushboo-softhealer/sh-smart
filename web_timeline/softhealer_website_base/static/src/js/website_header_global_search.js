odoo.define('theme_softhealer_base.global_search_dialog', function (require) {
    'use strict';

    var code = require("web.core");
    var concurrency = require("web.concurrency");
    var utils = require("web.utils");
    var Markup = utils.Markup;
    var Dialog = require("web.Dialog");
    var qweb = code.qweb;
    var publicWidget = require("web.public.widget");

    var GlobalSearchDialog = Dialog.extend({
        xmlDependencies: (Dialog.prototype.xmlDependencies || []).concat(
            ['/softhealer_website_base/static/src/xml/website_header_global_search.xml']
        ),
        template: "sh.softhealer.website.global.search.dialog",
        events: _.extend({}, Dialog.prototype.events, {
            'input .global-search-query': '_onInputGS',
            'keydown .global-search-query': '_onKeydownGS',
            'search .global-search-query': '_onSearchGS',
        }),
        autocompleteMinWidthGS: 300,
        /**
         * @override
         */
        init: function (parent, options) {
            this._super.apply(this, arguments);
            this._dpGS = new concurrency.DropPrevious();
            this._onInputGS = _.debounce(this._onInputGS, 400);
        },
        /**
         * @override
         */
        willStart: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self.$modal.find('.modal-dialog').addClass('modal-fullscreen');
                // self.$modal.find('.modal-dialog').addClass('sh_custom_dialog_box');
            });
        },
        /**
         * @override
         */
        start: function () {
            this.$inputGS = this.$('.global-search-query');
            this.$gsResultsDiv = this.$("div.js_gs_results");

            this.searchTypeGS = this.$inputGS.data('searchType');
            this.orderGS = this.$('.o_search_order_by').val();
            this.limitGS = parseInt(this.$inputGS.data('limit'));
            this.displayDescriptionGS = this.$inputGS.data('displayDescription');
            this.displayExtraLinkGS = this.$inputGS.data('displayExtraLink');
            this.displayDetailGS = this.$inputGS.data('displayDetail');
            this.displayImageGS = this.$inputGS.data('displayImage');
            this.wasEmptyGS = !this.$inputGS.val();
            // Make it easy for customization to disable fuzzy matching on specific searchboxes
            this.allowFuzzyGS = !this.$inputGS.data('noFuzzy');
            if (this.limitGS) {
                this.$inputGS.attr('autocomplete', 'off');
            }

            this.optionsGS = {
                'displayImage': this.displayImageGS,
                'displayDescription': this.displayDescriptionGS,
                'displayExtraLink': this.displayExtraLinkGS,
                'displayDetail': this.displayDetailGS,
                'allowFuzzy': this.allowFuzzyGS,
            };
            const form = this.$('.o_search_order_by').parents('form');
            for (const field of form.find("input[type='hidden']")) {
                this.optionsGS[field.name] = field.value;
            }
            const action = form.attr('action') || window.location.pathname + window.location.search;
            const [urlPath, urlParams] = action.split('?');
            if (urlParams) {
                for (const keyValue of urlParams.split('&')) {
                    const [key, value] = keyValue.split('=');
                    if (value && key !== 'search') {
                        // Decode URI parameters: revert + to space then decodeURIComponent.
                        this.optionsGS[decodeURIComponent(key.replace(/\+/g, '%20'))] = decodeURIComponent(value.replace(/\+/g, '%20'));
                    }
                }
            }
            const pathParts = urlPath.split('/');
            for (const index in pathParts) {
                const value = decodeURIComponent(pathParts[index]);
                if (index > 0 && /-[0-9]+$/.test(value)) { // is sluggish
                    this.optionsGS[decodeURIComponent(pathParts[index - 1])] = value;
                }
            }
            if (this.$inputGS.data('noFuzzy')) {
                $("<input type='hidden' name='noFuzzy' value='true'/>").appendTo(this.$inputGS);
            }
            return this._super.apply(this, arguments);
        },
        /**
         * call website autocomplete route.
         * @private
         */
        async _fetchGS() {
            const res = await this._rpc({
                route: '/website/snippet/autocomplete',
                params: {
                    'search_type': this.searchTypeGS,
                    'term': this.$inputGS.val(),
                    'order': this.orderGS,
                    'limit': this.limitGS,
                    'max_nb_chars': Math.round(Math.max(this.autocompleteMinWidthGS, parseInt(this.$el.width())) * 0.22),
                    'options': this.optionsGS,
                },
            });
            const fieldNames = [
                'name',
                'description',
                'extra_link',
                'detail',
                'detail_strike',
                'detail_extra',
            ];
            res.results.forEach(record => {
                for (const fieldName of fieldNames) {
                    if (record[fieldName]) {
                        if (typeof record[fieldName] === "object") {
                            for (const fieldKey of Object.keys(record[fieldName])) {
                                record[fieldName][fieldKey] = Markup(record[fieldName][fieldKey]);
                            }
                        } else {
                            record[fieldName] = Markup(record[fieldName]);
                        }
                    }
                }
            });
            return res;
        },
        /**
         * render Qweb template of global search autocomplete
         * @private
         */
        _renderGS: function (res) {
            if (res && this.limitGS) {
                const $prevData = this.$dialogSearchData;
                const results = res['results'];
                let template = 'sh.softhealer.website.global.search.autocomplete';
                this.$dialogSearchData = $(qweb.render(template, {
                    results: results,
                    parts: res['parts'],
                    hasMoreResults: results.length < res['results_count'],
                    search: this.$inputGS.val(),
                    fuzzySearch: res['fuzzy_search'],
                    widget: this,
                }));
                if (this.$dialogSearchData.length) {
                    if (!this.$gsResultsDiv) {
                        this.$gsResultsDiv = this.$el.find("div.js_gs_results") || this.$el.closest("div.js_gs_results");
                    }
                    this.$gsResultsDiv.append(this.$dialogSearchData); // append results to dialog div.
                }
                if ($prevData) {
                    $prevData.remove();// remove previous date
                }
            }
            else {
                if (this.$dialogSearchData) {
                    this.$dialogSearchData.remove();
                }
            }
        },
        /**
         * @private
         */
        _onInputGS: function () {
            if (!this.limitGS) {
                return;
            }
            if (this.searchTypeGS === 'all' && !this.$inputGS.val().trim().length) {
                this._renderGS();
            } else {
                this._dpGS.add(this._fetchGS()).then(this._renderGS.bind(this));
            }
        },
        /**
         * @private
         */
        _onKeydownGS: function (ev) {
            switch (ev.which) {
                case $.ui.keyCode.ESCAPE:
                    this._renderGS();
                    break;
                case $.ui.keyCode.ENTER:
                    ev.stopPropagation();
                    ev.preventDefault();
                    break;
            }
        },
        /**
         * @private
         */
        _onSearchGS: function (ev) {
            if (this.$inputGS[0].value) { // actual search
                this.limitGS = 0; // prevent autocomplete
            } else { // clear button clicked
                this._renderGS(); // remove existing suggestions
                ev.preventDefault();
                if (!this.wasEmptyGS) {
                    this.limitGS = 0; // prevent autocomplete
                    const form = this.$('.o_search_order_by').parents('form');
                    form.submit();
                }
            }
        },
        /**
        * @override
        */
        destroy() {
            this._super(...arguments);
            this._renderGS(null);
        },
    });

    publicWidget.registry.WebsiteHeaderGlobalSearch = publicWidget.Widget.extend({
        selector: '.js_cls_global_search_container',

        events: {
            "click .js_cls_global_search_btn": "_onGlobalSearchBtnClick",
        },
        /**
         * Open the global search dialog.
         * @private
         */
        _onGlobalSearchBtnClick: function () {
            var self = this;
            this.dialog = new GlobalSearchDialog(this, {
                size: 'extra-large',
                backdrop: true,
                renderHeader: false,
                renderFooter: false,
            });
            // his.dialog.open();

            this.dialog.opened().then(function () {
                self.dialog.$modal.addClass('sh_global_search_dialog_wrapper')
                self.$el.closest('.modal')
                self.$el.closest('.modal').addClass('sh_global_search_dialog_wrapper')
                self.dialog.$('.global-search-query').focus();
            });
            this.dialog.open();

        },
    });
});