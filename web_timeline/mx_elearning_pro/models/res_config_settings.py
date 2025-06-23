# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettingPro(models.TransientModel):
    _inherit = 'res.config.settings'

    proctoring_selection = fields.Selection([
        ('autoproctor', 'AutoProctor'),
        ('proctoredu', 'ProctorEdu'),
        ('mettl', 'Mettl'),
        ('proctortrack', 'ProctorTrack')], string="Proctoring",
         default='autoproctor',
         config_parameter='mx_elearning_pro.proctoring_selection')
    autoproctor_client_id = fields.Char('Client ID', config_parameter='mx_elearning_pro.autoproctor_client_id')
    autoproctor_client_secret = fields.Char('Client Secret', config_parameter='mx_elearning_pro.autoproctor_client_secret')
