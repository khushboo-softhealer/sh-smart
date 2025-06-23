/** @odoo-module **/
import { CustomFilterItem } from "@web/search/filter_menu/custom_filter_item";
import { patch } from '@web/core/utils/patch';

patch(CustomFilterItem.prototype, 'sh_proejct_task_portal_customisation.CustomFilterItem', {

    setup() {
        this._super();
        if (['project.task'].includes(this.env.searchModel.resModel)) {
            var fields_to_be_hide = [
                'email_from',
                'active',
                'allow_timesheets',
                'allow_subtasks',
                'user_ids',
                'allow_billable',
                'is_closed',
                'commercial_partner_id',
                'color',
                'company_id',
                'displayed_image_id',
                'create_date',
                'partner_id',
                'date_deadline',
                'display_project_id',
                'has_late_and_unreached_milestone',
                'effective_hours',
                'planned_hours',
                'partner_is_company',
                'legend_blocked',
                'legend_normal',
                'legend_done',
                'milestone_id',
                'allow_milestones',
                'overtime',
                'portal_user_names',
                'progress',
                'project_id',
                'remaining_hours',
                'remaining_hours_so',
                'sale_order_id',
                'sale_line_id',
                'sequence',
                'kanban_state',
                'subtask_effective_hours',
                'timesheet_ids',
                'total_hours_spent'
            ];
            this.fields = this.fields.filter(function (field) {
                return fields_to_be_hide.indexOf(field.name) === -1;
            });
        }
    }

});