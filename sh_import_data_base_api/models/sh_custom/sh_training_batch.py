# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class TrainingBatch(models.Model):
    _inherit = 'sh.training.batch'

    remote_sh_traing_batch_id = fields.Char("Remote Training Batch ID",copy=False)