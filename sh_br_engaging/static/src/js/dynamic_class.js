/** @odoo-module **/

import { View } from "@web/views/view";
import { patch } from "@web/core/utils/patch";
const { onWillStart } = owl;

patch(View.prototype, ' /sh_br_engaging/static/src/js/view_file.js', {
    setup() {
        this._super()
        onWillStart(async () => {
        if (this.props.resModel == "sh.check.in") {
            this.props.className = this.props.className + ' sh_checkIn_custom_class';
        }
        if (this.props.resModel == "sh.talking.points") {
            this.props.className = this.props.className + ' sh_talking_point_custom_class';
        }
        if (this.props.resModel == "sh.realtime.feedback") {
            this.props.className = this.props.className + ' sh_realtime_feedback_custom_class';
        }
        if (this.props.resModel == "sh.manage.questions") {
            this.props.className = this.props.className + ' sh_manage_questions_custom_class';
        }
        if (this.props.resModel == "sh.manage.agenda") {
            this.props.className = this.props.className + ' sh_manage_agenda_custom_class';
        }
        if (this.props.resModel == "sh.high.five") {
            this.props.className = this.props.className + ' sh_high_five_custom_class';
        }
        })
      },
});