odoo.define('sh_website_dynamic_content.s_sh_dynamic_content_options', function (require) {
    'use strict';

    const options = require('web_editor.snippets.options');
    var wUtils = require('website.utils');

    options.registry.ShDynamicContentSelectTemplateOptions = options.registry.SelectTemplate.extend({
        /**
         *
         * @override
         */
        init: function () {
            this._super.apply(this, arguments);
            // this.modelNameFilter = 'sh.website.dynamic.content';
            this.dynamic_contents = {};
        },
        /**
         * Fetches dynamic_contents.
         * @private
         * @returns {Promise}
         */
        _fetchDynamicContents: function () {
            return this._rpc({
                model: 'sh.website.dynamic.content',
                method: 'search_read',
                kwargs: {
                    domain: wUtils.websiteDomain(this),
                    fields: ['id', 'name'],
                }
            });
        },
        /**
         *
         * @override
         * @private
         */
        _renderCustomXML: async function (uiFragment) {
            await this._super.apply(this, arguments);
            await this._renderDynamicContentSelector(uiFragment);
        },
        /**
         * Renders the dynamic content option selector content into the provided uiFragment.
         * @private
         * @param {HTMLElement} uiFragment
         */
        _renderDynamicContentSelector: async function (uiFragment) {
            if (!Object.keys(this.dynamic_contents).length) {
                const dynamicContentsList = await this._fetchDynamicContents();
                this.dynamic_contents = {};
                for (let index in dynamicContentsList) {
                    this.dynamic_contents[dynamicContentsList[index].id] = dynamicContentsList[index];
                }
            }
            const dynamicContentSelectorEl = uiFragment.querySelector('[data-name="sh_content_opt"]');
            return this._renderSelectUserValueWidgetButtons(dynamicContentSelectorEl, this.dynamic_contents);
        },
        /**
         * Renders we-buttons into a SelectUserValueWidget element according to provided data.
         * @param {HTMLElement} selectUserValueWidgetElement the SelectUserValueWidget buttons
         *   have to be created into.
         * @param {Object} data
         * @private
         */
        _renderSelectUserValueWidgetButtons: async function (selectUserValueWidgetElement, data) {
            for (let id in data) {
                const button = document.createElement('we-button');
                button.dataset.selectDataAttribute = id;
                if (data[id].thumb) {
                    button.dataset.img = data[id].thumb;
                } else {
                    button.innerText = data[id].name;
                }
                selectUserValueWidgetElement.appendChild(button);
            }
        },
    });

});
