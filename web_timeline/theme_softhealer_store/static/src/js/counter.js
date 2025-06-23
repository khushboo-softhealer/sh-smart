odoo.define("theme_softhealer_store.sh_counter", function (require) {
    "use strict";

    var publicWidget = require("web.public.widget");
    var registry = publicWidget.registry;
    var animations = require("website.content.snippets.animation");

    registry.ShCounterSnippetCounterWidget = animations.Animation.extend({
        selector: ".sh_store_why_choose_us_snippet",
        disabledInEditableMode: true,
        effects: [
            {
                startEvents: "scroll",
                update: "_updateCounterOnScroll",
            },
        ],

        /**
         * @constructor
         */
        init: function () {
            this._super(...arguments);
            this.HasCounted = false;
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
        _updateCounterOnScroll: function (scroll) {
            var oTop = this.$el.offset().top - window.innerHeight;
            if (this.HasCounted == false && $(window).scrollTop() > oTop) {
                //counter part start here
                var looping = true;
                this.$el
                    .find(".js_cls_counter_number")
                    .each(function () {
                        var $this = $(this);
                        looping = true;
                        jQuery({ Counter: 0 }).animate(
                            { Counter: $this.text() },
                            {
                                duration: 3000,
                                easing: "swing",
                                step: function () {
                                    $this.text(Math.ceil(this.Counter));
                                },
                            }
                        );
                    })
                    .promise()
                    .done(function () {
                        looping = false;
                    });
                //counter part ends here
                this.HasCounted = true;
            }
        },
    });
});
