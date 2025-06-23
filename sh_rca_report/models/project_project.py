# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import _, api, fields, models

class ProjectProject(models.Model):
    _inherit = "project.project"

    sh_total_rca_report = fields.Integer(string='Total RCA Report',compute='_compute_sh_total_rca_report') 
    def show_project_rca_report(self):
         return {
                'name':'RCA Report',
                'res_model':'sh.rca.report',
                'view_mode':'list,form',
                'target':'current',
                'type':'ir.actions.act_window',
                "domain": [("project_id", "=", self.id)]
                }

    
    def _compute_sh_total_rca_report(self):
        for rec in self:
            reports = self.env['sh.rca.report'].search([('project_id','=',rec.id)])
            if reports:

                rec.sh_total_rca_report = len(reports)
            else:
                rec.sh_total_rca_report = 0