odoo.define("theme_softhealer_website.sh_website_aos_init", function (require) {
    "use strict";

    var publicWidget = require("web.public.widget");
    var registry = publicWidget.registry;
    var animations = require("website.content.snippets.animation");

    AOS.init({
        duration:900,
    });

    function isElementPartiallyInViewport(el) {
        // Special bonus for those using jQuery
        if (typeof jQuery !== "undefined" && el instanceof jQuery) el = el[0];

        var rect = el.getBoundingClientRect();
        // DOMRect { x: 8, y: 8, width: 100, height: 100, top: 8, right: 108, bottom: 108, left: 8 }
        var windowHeight = window.innerHeight || document.documentElement.clientHeight;
        var windowWidth = window.innerWidth || document.documentElement.clientWidth;

        // http://stackoverflow.com/questions/325933/determine-whether-two-date-ranges-overlap
        var vertInView = rect.top <= windowHeight && rect.top + rect.height >= 0;
        var horInView = rect.left <= windowWidth && rect.left + rect.width >= 0;

        return vertInView && horInView;
    }

    registry.sAnimationWidget = animations.Animation.extend({
        selector: ".aos-init",
        disabledInEditableMode: true,
        effects: [
            {
                startEvents: "scroll",
                update: "_updateCounterOnScrollAosAnimation",
            },
        ],

        /**
         * @constructor
         */
        init: function () {
            this._super(...arguments);

        },

        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------
        /**
         * Called when the window is scrolled
         *
         * @private
         * @param {integer} scroll
         */
        
        _updateCounterOnScrollAosAnimation: function (scroll) {
            var self = this;
            
            if (isElementPartiallyInViewport(this.$el)) {
                self.$el.addClass("aos-animate");
            }
        },
    });
});