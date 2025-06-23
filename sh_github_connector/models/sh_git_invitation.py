# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields


class ShGitInvitation(models.Model):
    _name = "sh.git.invitation"
    _description = "Git Invitation"

    project_id = fields.Many2one("project.project")
    user_id = fields.Many2one("res.users")
    is_invitation_send = fields.Boolean("Is Invitation Send?", default=False)

    def _check_invitation(self, git_app=False, clon_link=False):
        if not git_app:
            git_app = self.env['sh.github.connector'].search([
                ('state', '=', 'success')
            ], limit=1)
            if not git_app:
                for line in self:
                    line.project_id._log(f"'{line.user_id.name}' user added the Github Username, But Git app not found !")
                return

        for line in self:
            if line.is_invitation_send:
                continue
            git_username = line.user_id.sh_github_username
            if not git_username:
                line.project_id._log(f"Enter the Github Username for the user '{line.user_id.name}' !")
                continue
            start_point = clon_link
            if not start_point:
                start_point = line.project_id._get_start_point()
            if git_username in start_point:
                # Repo Owner
                line.is_invitation_send = True
                continue
            response = git_app._send_invitation(start_point, git_username)
            if response == True:
                line.project_id._log(f"Invitation sent successfully to '{git_username}'.", 'success')
                line.is_invitation_send = True
            else:
                line.project_id._log(response)
