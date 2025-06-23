/** @odoo-module **/

import { GroupByMenu } from "@web/search/group_by_menu/group_by_menu";
import { patch } from 'web.utils';
patch(GroupByMenu.prototype, 'sh_proejct_task_portal_customisation.CustomFilterItem', {
    validateField(fieldName, field) {
        // Corrected model check
        if (['project.task'].includes(this.env.searchModel.resModel)) {
            const fields_to_be_hide = [
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

            if (fields_to_be_hide.includes(fieldName)) {
                return false;
            }

            // Correctly delegate to the original method
            return this._super(fieldName, field);
        } else {
            // Correctly delegate to the original method when the model doesn't match
            return this._super(fieldName, field);
        }
    }
});
