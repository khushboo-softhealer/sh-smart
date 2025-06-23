/** @odoo-module **/
import { ActionMenus } from "@web/search/action_menus/action_menus";
import { patch } from 'web.utils';
var session = require("web.session");
const components = { ActionMenus };

var group_show_print = false;
session?.user_has_group("sh_hide_feature.group_show_print").then(function (has_group) {
    group_show_print = has_group;
});

var group_show_action = false;
session?.user_has_group("sh_hide_feature.group_show_action").then(function (has_group) {
    group_show_action = has_group;
});

patch(components.ActionMenus.prototype, 'sh_hide_feature/static/webclient/action_menus.js', {

    setup() {
        this._super();
        this.group_show_print = group_show_print;
        this.group_show_action = group_show_action;
    },


});
