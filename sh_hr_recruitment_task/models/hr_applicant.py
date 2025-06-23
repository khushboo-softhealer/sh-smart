# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import api, models, fields


class HrApplicant(models.Model):
    _inherit = "hr.applicant"

    hr_applicant_id = fields.Many2one('hr.applicant')
    hide_button_bool = fields.Boolean(default=False)

    @api.model_create_multi
    def create(self, vals_list):
        records = super(HrApplicant, self).create(vals_list)
        for res in records:
            users = res.env['res.users'].search([])
            listt = []
            for user in users:
                if user.has_group('hr.group_hr_manager') and user.sh_job_applicant_notification_on_off:
                    listt.append(user)
            base_url = self.env['ir.config_parameter'].sudo(
            ).get_param('web.base.url')
            self.env['user.push.notification'].push_notification(listt, 'Job Application Created', 'Job Application Ref : %s:' % (
                res.name), base_url+"/mail/view?model=hr.applicant&res_id="+str(res.id), 'hr.applicant', res.id, 'hr')
        return records

    def write(self, values):
        res = super(HrApplicant, self).write(values)
        for rec in self:
            project_task_ids = self.env['project.task'].search([('hr_applicant_id',
                                                                 '=', rec.id)])
            if project_task_ids:
                for tasks in project_task_ids:
                    tasks.int_sch_time = rec.sh_hr_placement_schedule_datetime
        return res

    def action_get_task_view(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Tasks",
            "view_mode": "tree,form",
            "res_model": "project.task",
            'domain': [('hr_applicant_id', '=', self.id)],
        }
