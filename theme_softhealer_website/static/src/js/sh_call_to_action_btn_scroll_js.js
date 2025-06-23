odoo.define('theme_softhealer_website.sh_call_to_action_btn_scroll_js', function (require) {
    'use strict';


    var publicWidget = require('web.public.widget');
    
    
    publicWidget.registry.SmoothScrollToForm = publicWidget.Widget.extend({
        selector: '.sh_call_to_action_btn_scroll_js',  // Select the anchor with this ID

        events: {
            'click': '_onClick',  // Bind the click event to the _onClick method
        },

        /**
         * Handles the click event for smooth scrolling
         *
         * @private
         * @param {Event} event
         */
        _onClick: function (event) {
            event.preventDefault(); // Prevent the default anchor behavior            

            // Get the target section
            var targetSection = document.querySelector('#sh_mobile_app_form_box');

            // Smooth scroll to the target section
            if (targetSection) {
                targetSection.scrollIntoView({ behavior: 'smooth' });
            }
        },
    });
});