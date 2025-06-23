# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class ShCommonMailDomains(models.Model):
    _name = 'sh.common.mail.domains'
    _description = 'Common mail domains'
    
    name = fields.Char("Mail Domain")