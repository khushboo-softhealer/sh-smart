# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields

class OdooHostedOn(models.Model):
    _name = 'sh.odoo.hosted.on'
    _description = 'Odoo Hosted On'

    name = fields.Char('Host Name',required=True)
    sh_edtion_id = fields.Many2one('sh.edition',string='Edition')
    active = fields.Boolean(default=True)
    sh_display_in_frontend = fields.Boolean('Display At Frontend ?')
    company_id = fields.Many2one('res.company', string='Company',
        default=lambda self: self.env.company)