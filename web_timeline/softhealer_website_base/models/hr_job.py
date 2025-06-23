# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import _, fields, models


class HrJobs(models.Model):
    _inherit = 'hr.job'

    sh_position = fields.Char(string="Position")
    sh_custom_description=fields.Text(string="Position Description")
    sh_urgent = fields.Boolean('Urgent ?')
    sh_job_image = fields.Binary(string='Image')
    sh_job_location = fields.Char(string="Work Location")

    def action_code_job_position_website_description(self):
        self.ensure_one()
        code_form = self.env.ref('softhealer_website_base.sh_website_editor_hr_job_form_wizard_code_view')
        return {
            'name': _('Job Positions'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'hr.job',
            'res_id':self.id,
            'views': [(code_form.id, 'form')],
            'view_id': code_form.id,
            'target': 'new',
        }