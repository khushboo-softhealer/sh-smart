# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields

class WizardGitRepo(models.TransientModel):
    _name = 'sh.update.git.repo.wizard'
    _description = "Wizard Git Repo"

    git_repo = fields.Many2one('sh.git.repo',string="Git Repo")
    product_ids = fields.Many2many('product.template')

    def update_repos(self):        
        for product in self.product_ids:
            product.git_repo = self.git_repo.id
