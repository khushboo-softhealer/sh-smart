# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import api, models, fields


class ProjectTask(models.Model):
    _inherit = "project.task"

    hr_applicant_id = fields.Many2one('hr.applicant')
    int_sch_time = fields.Datetime(string="Interview Schdule Time")

    check_bool_int_sch_time = fields.Boolean(
        default=True,
        compute="_compute_check_bool_interview_schedule",
    )

    @api.depends('project_id')
    def _compute_check_bool_interview_schedule(self):
        for rec in self:
            if rec.company_id.project_id:
                if rec.company_id.project_id.id == rec.project_id.id:
                    rec.check_bool_int_sch_time = True
                else:
                    rec.check_bool_int_sch_time = False
            else:
                rec.check_bool_int_sch_time = False

    def action_get_recruitment_view(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Recruitment",
            "view_mode": "tree,form",
            "res_model": "hr.applicant",
            'domain': [('hr_applicant_id', '=', self.hr_applicant_id.id)],
        }
