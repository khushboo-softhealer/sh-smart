# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models, api


class CreateTaskWizard(models.TransientModel):
    _name = "sh.create.task.wizard"
    _description = "Create Wizard"

    name = fields.Char(required=True)
    project_id = fields.Many2one("project.project", string="Project")
    responsible_user = fields.Many2many("res.users", string="Responsible User")
    schedule = fields.Datetime(string="Schedule")

    @api.model
    def default_get(self, fields):
        res = super(CreateTaskWizard, self).default_get(fields)
        parent_id = self.env.context.get("active_id")
        parent_model = self.env.context.get("active_model")
        parent_record = self.env[parent_model].browse(parent_id)
        res.update({
            'name':
            parent_record.name,
            'project_id':
            parent_record.company_id.project_id.id,
            'responsible_user':
            [(6, 0, parent_record.job_id.interviewer_ids.ids)],
            'schedule':
            parent_record.sh_hr_placement_schedule_datetime,
        })
        return res

    def create_task(self):
        parent_id = self.env.context.get("active_id")
        parent_model = self.env.context.get("active_model")
        parent_record = self.env[parent_model].browse(parent_id)

        parent_record.hr_applicant_id = parent_record.id
        vals = {
            "sh_hr_placement_schedule_datetime": self.schedule,
            "hide_button_bool": True
        }
        parent_record.write(vals)
        created_task = self.env['project.task'].sudo().create({
            'name':
            self.name,
            'project_id':
            self.project_id.id,
            "user_ids": [(6, 0, self.responsible_user.ids)],
            "hr_applicant_id":
            parent_record.id,
            "description":
            parent_record.description,
            "int_sch_time":
            self.schedule
        })
        if created_task:
            for attachments in parent_record.attachment_ids:
                default = {
                    'res_id': created_task.id,
                    'res_model': "project.task"
                }
                attachments.copy(default=default)
