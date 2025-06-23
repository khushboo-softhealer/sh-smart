# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields, api


class HrApplicant(models.Model):
    _inherit = "hr.applicant"

    sh_hr_placement_is_confirm = fields.Boolean(
        string="Is Confirm?", tracking=True)
    sh_hr_placement_schedule_datetime = fields.Datetime(
        string="Schedule", tracking=True)
    placement_id = fields.Many2one(comodel_name='sh.placement')
    college_id = fields.Many2one(comodel_name='sh.college')
    interview_ids = fields.Many2many(
        comodel_name='hr.employee', string='Interview Take By')
    reject_reason_id = fields.Many2one(
        string="Proposal Reject Reasons", comodel_name='sh.proposal.reject.reasons')
    interview_type = fields.Selection([('video', 'Video'), ('telephonic', 'Telephonic'), (
        'office', 'Office Location')], default='office', required=True)

    @api.onchange('job_id')
    def sh_job_id_onchange(self):
        domain = []
        if self.job_id and self.job_id.interviewer_ids:
            for users in self.job_id.interviewer_ids:
                emp_id = self.env['hr.employee'].sudo().search(
                    [('user_id', '=', users.id)])
                domain.append(emp_id.id)
        return {'domain': {'interview_ids': [('id', 'in', domain)]}}
