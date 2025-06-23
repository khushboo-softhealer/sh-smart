odoo.define('theme_softhealer_website.upcoming_feature', function (require) {
    'use strict';

    var publicWidget = require("web.public.widget");

    publicWidget.registry.upcoming_feature = publicWidget.Widget.extend({
        selector: '.js_cls_sh_upcoming_feature_wrapper',

        events: {
            'mouseover .js_cls_sh_upcoming_box': '_on_sh_upcoming_box_mouse_enter',
           // 'mouseleave .js_cls_sh_upcoming_box': '_on_sh_upcoming_box_mouse_leave',
        },

    /**
     * Handler for Upcoming Box mouseenter event.
     *
     * @param {OdooEvent} ev
     * @private
     */
    async _on_sh_upcoming_box_mouse_enter(ev) {
        ev.stopPropagation();
        this.$el.find('.js_cls_sh_upcoming_box').removeClass('active');
        $(ev.currentTarget).addClass("active");
    },


    /**
     * Handler for Upcoming Box mouseleave event.
     *
     * @param {OdooEvent} ev
     * @private
     */
    async _on_sh_upcoming_box_mouse_leave(ev) {
        ev.stopPropagation();
        this.$el.find('.js_cls_sh_upcoming_box').removeClass('active');        
    },

    });
});