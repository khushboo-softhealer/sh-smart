# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

class ShsopStages(models.Model):
    _name = 'sh.sop.stages'
    _description = 'Stages'   

    name= fields.Char(string="Stage Name",required=True)
    sh_seq = fields.Integer(string="Sequence",compute="_get_seq")
    
    @api.depends("name")
    def _get_seq(self):
        no=0
        for rec in self:
            no+=1
            rec.sh_seq = no