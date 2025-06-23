/** @odoo-module **/
import { KanbanController } from "@web/views/kanban/kanban_controller";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";

patch(KanbanController.prototype, 'sh_br_engaging/static/src/js/kanban_controller.js', {

    /**
     * @override
     */

    setup() {
        this._super();
        this.action = useService("action");
        this.is_talking_point_model = false
        if (this.props.resModel == 'sh.talking.points') {
            this.is_talking_point_model = true
            $("body").removeClass("sh_create_1o1s_wizard_class")
        }
    },

    _onClickCreateNew1on1Record (ev) { 
        $("body").addClass("sh_create_1o1s_wizard_class")
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: this.env._t('Manage Questions Setting'),
            target: 'new',
            res_model: 'sh.create.1on1s.wizard',
            views: [[false, 'form']],
        });    }
  
});
