# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields


class SlideSurveyProctor(models.Model):
    _inherit = 'survey.survey'

    is_proctoring = fields.Boolean(string="Proctoring")
    proctoring_passing_score = fields.Float("Proctor Passing Score (%)")


class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    proctor_scoring_percentage = fields.Float("Proctor Score (%)", store=True, compute_sudo=True)
    evidence_ids = fields.One2many('survey.autoproctor_evidence','proctor_id', string="Survey Proctor User Evidence")
    proctoring_passing_score = fields.Float("Proctor Passing Score (%)", related='survey_id.proctoring_passing_score', store=True)

class SurveyProctorEvidence(models.Model):
    _name = 'survey.autoproctor_evidence'

    proctor_id = fields.Many2one('survey.user_input', ondelete='cascade', string="Evidence Entry")
    evidence_url = fields.Char('Evidence URL')
    message = fields.Char('Evidence Message')
    violation = fields.Char('Violation')
    label = fields.Char('Evidence Label')
    # occurred_at = fields.Datetime('Occurred At')
