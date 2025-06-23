/** @odoo-module **/

import { ListController } from "@web/views/list/list_controller";
import { patch } from "@web/core/utils/patch";

// patch(ListController.prototype, 'sh_backmate_theme/static/src/js/list_controller.js', {
patch(ListController.prototype, 'sh_helpdesk/static/src/js/product_refresh.js', {
   
    _onClickListRefreshView (ev) { 
        this.actionService.switchView('list');
    }
  
});