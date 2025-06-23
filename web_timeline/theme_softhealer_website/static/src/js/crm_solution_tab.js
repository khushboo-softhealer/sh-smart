odoo.define('theme_softhealer_website.crm_solution_tab_animation', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var animations = require('website.content.snippets.animation');
    
    publicWidget.registry.CRMSolutionTabAnimations = animations.Animation.extend({
        selector: '.sh_crm_solution_tab_section',
        effects: [{
            startEvents: 'scroll',
            update: '_updateTabsOnScroll',
        }],
        /**
         * Called when the window is scrolled
         *
         * @private
         * @param {integer} scroll
         */
        _updateTabsOnScroll: function (scroll) {
            var self = this;
            var active = false;
            var sectionIds = self.$el.find('a.sh_crm_solution_tabs_item_link');
            sectionIds.each(function () {
                var $target = $(this);
                var $container = self.$el.find($target.attr('href'))
                var containerPos = scroll - $container.offset().top;
                if (containerPos < scroll) {
                    if (!active) {
                        active = true;
                        sectionIds.filter('.active').removeClass('active');
                        $target.addClass('active');
                    }
                } else {
                    $target.removeClass('active');
                }
            });
        },
    });
});