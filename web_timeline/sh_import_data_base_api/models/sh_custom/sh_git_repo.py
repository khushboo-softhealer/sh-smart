# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class ShGitRepo(models.Model):
    _inherit = 'sh.git.repo'

    remote_sh_git_repo_id = fields.Char("Remote Git Repo ID",copy=False)







