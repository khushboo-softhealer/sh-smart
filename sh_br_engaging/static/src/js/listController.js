/** @odoo-module **/

import { ListController } from "@web/views/list/list_controller";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";

patch(ListController.prototype, ' /sh_br_engaging/static/src/js/listController.js', {
    setup() {
        this._super()
        this.action = useService("action");
        if (this.props.resModel == "sh.manage.questions") {
            this.sh_is_manage_question_model = true
        }
        if (this.props.resModel == "sh.talking.points") {
            this.is_talking_point_model = true
            $("body").removeClass("sh_create_1o1s_wizard_class")
        }
        if (this.props.resModel == "sh.realtime.feedback") {
            this.sh_is_realtime_feedback_model = true
        }
      },
    _onClickSettingButton() { 
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: this.env._t('Manage Questions Setting'),
            target: 'current',
            res_model: 'res.config.settings',
            views: [[false, 'form']],
            context: {'module' : 'br_engage', 'bin_size': false},
        });
    },

    onClickGiveFeedback(ev) {
        $("body").addClass("sh_givefeedback")
        this.actionService.doAction({
            name: "Give Feedback Wizard",
            res_model: "sh.give.feedback.wizard",
            // res_id: this.actionId,
            views: [[false, "form"]],
            type: "ir.actions.act_window",
            view_mode: "form",
            target: "new",
        });
    },

    onClickRequestFeedback(){
        $("body").addClass("sh_requestfeedback")
        this.actionService.doAction({
            name: "Request Feedback Wizard",
            res_model: "sh.request.feedback.wizard",
            // res_id: this.actionId,
            views: [[false, "form"]],
            type: "ir.actions.act_window",
            view_mode: "form",
            target: "new",
        });
    },


    _onClickCreateNew1on1Record() {
        $("body").addClass("sh_create_1o1s_wizard_class")
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: this.env._t('Manage Questions Setting'),
            target: 'new',
            res_model: 'sh.create.1on1s.wizard',
            views: [[false, 'form']],
        });    
    }
  
});