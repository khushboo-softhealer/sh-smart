/** @odoo-module **/

import publicWidget from 'web.public.widget';
import { WebsiteSale } from 'website_sale.website_sale';

publicWidget.registry.WebsiteSale.include({
    /**
     * Sets the url hash from the selected product options.
     *
     * @private
     * @override
     */
    _setUrlHash: function ($parent) {
        var $attributes = $parent.find('input.js_variant_change:checked, select.js_variant_change option:selected');
        var attributeIds = _.map($attributes, function (elem) {
            return $(elem).data('value_id');
        });
        // Softhealer custom code
        // window.location.replace('#attr=' + attributeIds.join(','));
        // Softhealer custom code
    },
})