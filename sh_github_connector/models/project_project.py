# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from datetime import datetime
from odoo import models, fields, api


class ShProjectGithub(models.Model):
    _inherit = "project.project"

    sh_git_send_invitation = fields.Boolean(string="Send Git Repo Invitation", copy=False)
    sh_git_repo_link = fields.Char("Repo Link", copy=False)
    sh_git_log_line = fields.One2many("sh.connector.log", "project_id", string="Git Invitation Log")
    sh_git_invitation_line = fields.One2many("sh.git.invitation", "project_id", string="Git Invitation Line")

    # -------------------------------------------------
    #  ORM Methods
    # -------------------------------------------------

    @api.model_create_multi
    def create(self, vals_list):
        created_projects = super().create(vals_list)
        for project in created_projects:
            if project.sh_git_send_invitation:
                project._repo_invitation()
        return created_projects

    def write(self, vals):
        send_invitation = vals.get('sh_git_send_invitation') or vals.get('sh_git_repo_link') or vals.get('responsible_user_ids')
        status = super().write(vals)
        for project in self:
            if send_invitation:
                    project._repo_invitation()
        return status

    # -------------------------------------------------
    #  Custom Methods
    # -------------------------------------------------

    def _log(self, message, state='error'):
        self.env['sh.connector.log'].create({
            'project_id': self.id,
            'field_type': 'project',
            'operation': 'invitation',
            'datetime': datetime.now(),
            'state': state,
            'message': message
        })

    def _create_repo(self, git_app):
        json_data,reason = git_app.post({
            'name': self.name.replace(' ', '_'),
            'visibility': 'private',
            'private': True
        })
        if not json_data:
            self._log(f'Failed to create the repo ! {reason}')
            return False
        if not json_data.get('clone_url'):
            self._log(f"Repo '{json_data['name']}' created but, Failed to get the clone url !")
            return False
        self.sh_git_repo_link = json_data['clone_url']
        self._log(f"Repo '{json_data['name']}' is created.", "success")
        return True

    def _get_start_point(self):
        clon_link = self.sh_git_repo_link.replace('.git', '')
        return clon_link.replace('github.com', 'api.github.com/repos')

    def _repo_invitation(self):
        if not self.sh_git_send_invitation:
            return
        if not self.responsible_user_ids:
            self._log('Please add the responsible_user_ids to send them invitation !')
            return
        git_app = self.env['sh.github.connector'].search([
            ('state', '=', 'success')
        ], limit=1)
        if not git_app:
            self._log('Git App not found !')
            return
        if not self.sh_git_repo_link:
            if not self._create_repo(git_app):
                return
        if '.git' not in self.sh_git_repo_link:
            self._log('Please enter a proper repo link !')
            return
        # ------------------------------------------------------
        #  Send Invitations To The Users
        # ------------------------------------------------------
        clon_link = self._get_start_point()

        if self.sh_git_invitation_line:
            for user in self.responsible_user_ids:
                if user.id not in self.sh_git_invitation_line.user_id.ids:
                    self.env["sh.git.invitation"].create({
                        'project_id': self.id,
                        'user_id': user.id
                    })
        else:
            for user in self.responsible_user_ids:
                self.env["sh.git.invitation"].create({
                    'project_id': self.id,
                    'user_id': user.id
                })

        self.sh_git_invitation_line._check_invitation(git_app, clon_link)
