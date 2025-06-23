# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models


class ShCollegeChangeStagesWizard(models.TransientModel):
    _name = 'sh.college.change.stages.wizard'
    _description = 'Change Stage of College'

    stage_id = fields.Many2one(
        'sh.college.stages', string="Stage", required=True)
    college_ids = fields.Many2many('sh.college')

    def change_state_action(self):
        self.college_ids.write({
            'stage_id': self.stage_id.id
        })
