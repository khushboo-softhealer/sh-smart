/** @odoo-module **/
import { registry } from "@web/core/registry";
import { BooleanField } from "@web/views/fields/boolean/boolean_field";
import { useService } from '@web/core/utils/hooks';
const Dialog = require('web.Dialog');

const { Component, onWillUpdateProps } = owl;
class OpenWizard extends BooleanField {
    
    setup(){
        super.setup();
        this.orm = useService("orm");
        this.actionService = useService('action');
    }
    
    
    async onChange(newValue) {
        this.not_billable = this.props.record.data.not_billable

        this.not_billable = newValue
        if (this.not_billable ) {
            this.openWizard()
        }
        else{
            this.orm.call("project.task", "un_tick_not_billable",[this.props.record.data.id]);
        }
        
    }

    openWizard() {
        return new Promise((resolve) => {

            const recordId = this.props.record.data.id;
            if (!recordId) {
                Dialog.alert(this, _("Save the Current record"));
                return resolve(false);
            }

        var value = this.actionService.doAction(
                {
                    type: "ir.actions.act_window",
                    res_model: "sh.not.billable.reason.wizard",
                    view_mode: "form",
                    view_type: "form",
                    views: [[false, "form"]],
                    target: "new",
                    context : {
                        'task_id_not_billable_boolean_wizard': this.props.record.data.id
                    }
                },
                {
                    onClose: () => resolve(value),
                }
            );
        
        });
    };
    
}
OpenWizard.isUpgradeField = true;
OpenWizard.additionalClasses = [
    ...OpenWizard.additionalClasses || [],
    "o_field_boolean",
];

registry.category("fields").add("openWizard", OpenWizard);
