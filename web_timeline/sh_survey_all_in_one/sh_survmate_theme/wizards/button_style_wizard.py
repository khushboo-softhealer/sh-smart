# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields


class ShSurvmateThemeButtonDesignWizard(models.TransientModel):
    _name = 'sh.survmate.theme.button.design.wizard'
    _description = 'Survmate Theme Button Design'
    _order = "id desc"
    
    img_src = fields.Char(string = "Image Src")