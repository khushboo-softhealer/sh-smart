# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import _, api, fields, models

class ShRcaReport(models.Model):
    _name = 'sh.rca.report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Sh RCA Report'

    name = fields.Char(string='name',default='New')
    issue_owner = fields.Char(string='Issue Owner Name',tracking=True)
    email = fields.Char(string='Email',tracking=True)
    report_date = fields.Datetime(string="Issue Report Date",tracking=True)
    issue_priority = fields.Selection([('very_low','Very Low'),('low','Low'),('medium','Medium'),('high','High'),('very_high','Very High')],tracking=True)
    description = fields.Html(string='Description',tracking=True)
    step_to_reproduce = fields.Html(string="Step to Reproduce",tracking=True)
    expected_outcome = fields.Html(string='Expected Outcome',tracking=True)
    actual_out_come = fields.Html(string='Actual Outcome',tracking=True)
    bug_logs = fields.Html(string='Bug Logs',tracking=True)
    attachment = fields.Binary(string='Attachments',tracking=True)
    root_cause = fields.Html(string='Root Cause',tracking=True)
    corrective_action = fields.Html(string='Corrective Action',tracking=True) 
    preventive_action = fields.Html(string='Preventive Action',tracking=True)
    issue_resolved_datetime = fields.Datetime(string='Issue Resolved Date(Test Server)',tracking=True)
    issue_resolved_datetime_in_main = fields.Datetime(string="Issue Resolved Date(Main Server)",tracking=True)
    project_id = fields.Many2one('project.project',string='Project Name',tracking=True)
    task_id = fields.Many2one('project.task',string='Task Name',tracking=True)
    issue_resolve_duration = fields.Float(string='Duration',compute="_compute_issue_resolve_duration")
    state = fields.Selection([('draft','Draft'),('done','Done')], default='draft',tracking=True) 

    @api.model
    def create(self, vals):        
        vals['name'] = self.env['ir.sequence'].next_by_code('sh.rca.report') or _("New")
        return super().create(vals)
    
    @api.depends('report_date','issue_resolved_datetime_in_main')
    def _compute_issue_resolve_duration(self):
        for rec in self:
            if rec.report_date and rec.issue_resolved_datetime_in_main:
                delta = rec.issue_resolved_datetime_in_main - rec.report_date
                rec.issue_resolve_duration = delta.total_seconds() / 3600.0
            else:
                rec.issue_resolve_duration = 0.0

    def lock_rca(self):
        self.state = 'done'

    def rest_to_draft_rca(self):
        self.state = 'draft'

    def action_print_rca_report(self):
        return self.env.ref('sh_rca_report.report_sh_rca_report').report_action(self)