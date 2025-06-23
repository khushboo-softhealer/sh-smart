# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import _, api, fields, models

class ProjectTask(models.Model):
    _inherit="project.task"
    _description="Project Task"

    def create_rca_report(self):
        return {
                'name':'RCA Report',
                'res_model':'sh.rca.report',
                'view_mode':'form',
                'view_id': self.env.ref('sh_rca_report.view_sh_rca_report_form').id,
                'target':'new',
                'type':'ir.actions.act_window',
                'context':{'default_task_id':self.id,
                            "default_project_id":self.project_id.id}
            }

    def show_task_rca_report(self):
        return {
                'name':'RCA Report',
                'res_model':'sh.rca.report',
                'view_mode':'list,form',
                'target':'current',
                'type':'ir.actions.act_window',
                "domain": [("task_id", "=", self.id)],
            }
