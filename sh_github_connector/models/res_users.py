# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class ShGitUsers(models.Model):
    _inherit = "res.users"

    sh_github_username = fields.Char("Github Username")
    # sh_git_invitation_line = fields.One2many("sh.git.invitation", "user_id", string="Git Invitation Line")

    # def write(self, vals):
    #     status = super().write(vals)
    #     if vals.get('sh_github_username'):
    #         for user in self:
    #             if user.sh_git_invitation_line:
    #                 user.sh_git_invitation_line._check_invitation()
    #     return status
