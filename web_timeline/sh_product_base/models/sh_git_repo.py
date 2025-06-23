# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields

class GitRepo(models.Model):
    _name = 'sh.git.repo'
    _description = "Manage Git Respos"

    name = fields.Char("Name")
    repo_link = fields.Char("Repo Link")
    responsible_user = fields.Many2one("res.users")
    company_id = fields.Many2one('res.company', string='Company',
        default=lambda self: self.env.company)