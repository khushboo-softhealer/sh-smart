# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class SHTrainingCourse(models.Model):
    _inherit = 'sh.training.course'

    remote_sh_traing_course_id = fields.Char("Remote Training Course ID",copy=False)