/** @odoo-module **/

import { ListController } from "@web/views/list/list_controller";
import core from "web.core";
var _t = core._t;
import { patch } from "@web/core/utils/patch";

patch(ListController.prototype, 'sh_backmate_theme_adv/static/src/js/list_controller.js', {
   
    _onClickRefreshView (ev) { 
        this.actionService.switchView('list');
    }
  
});


