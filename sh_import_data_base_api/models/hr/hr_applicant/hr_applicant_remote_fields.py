# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class HrRecruitmentStage(models.Model):
    _inherit = 'hr.recruitment.stage'
    remote_recruitment_stage_id = fields.Char("Remote Recruitment Stage ID",copy=False)


class HrApplicantCategory(models.Model):
    _inherit = 'hr.applicant.category'
    remote_category_id = fields.Char("Remote Category ID",copy=False)


class UtmMedium(models.Model):
    _inherit = 'utm.medium'
    remote_medium_id = fields.Char("Remote Medium ID",copy=False)


class UtmSource(models.Model):
    _inherit = 'utm.source'
    remote_source_id = fields.Char("Remote Source ID",copy=False)


class HrRecruitmentDegree(models.Model):
    _inherit = 'hr.recruitment.degree'
    remote_degree_id = fields.Char("Remote Degree ID",copy=False)


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'
    remote_hr_applicant_id = fields.Char("Remote Applicant ID",copy=False)


class ShPlacement(models.Model):
    _inherit = 'sh.placement'
    remote_sh_placement_id = fields.Char("Remote placement ID",copy=False)


class ShPlacementLine(models.Model):
    _inherit = 'sh.placement.line'
    remote_sh_placement_line_id = fields.Char("Remote Placement Line ID",copy=False)


class ShCollege(models.Model):
    _inherit = 'sh.college'
    remote_sh_college_id = fields.Char("Remote College ID",copy=False)


class ShCollegeStages(models.Model):
    _inherit = 'sh.college.stages'
    remote_sh_college_stage_id = fields.Char("Remote College Stages ID",copy=False)


class ShProposalRrejectReasons(models.Model):
    _inherit = 'sh.proposal.reject.reasons'
    remote_sh_proposal_reject_reason_id = fields.Char(
        "Remote Proposal Reject Reason ID",copy=False)
