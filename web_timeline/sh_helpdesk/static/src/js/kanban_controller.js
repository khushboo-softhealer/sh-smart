/** @odoo-module **/

import { KanbanController } from "@web/views/kanban/kanban_controller";
import { patch } from "@web/core/utils/patch";

patch(KanbanController.prototype, 'sh_helpdesk/static/src/js/kanban_controller.js', {
   
    _onClickKanbanRefreshView (ev) { 
        this.actionService.switchView('kanban');
    }
  
});
