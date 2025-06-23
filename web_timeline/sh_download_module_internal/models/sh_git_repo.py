# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, _


class ShGitRepo(models.Model):
    _inherit = 'sh.git.repo'

    def _can_acces_by_login_use(self, connector_obj):
        '''Check that login user has the Repo access'''
        github_username = self.env.user.sh_github_username
        if not github_username:
            return {'error': f"{self.env.user.name}, Please enter the github-username in your profile"}

        repo_api_link = self._get_api_link()
        if not repo_api_link:
            return {'error': f"Invalid repo '{self.name}' url !"}

        # /user
        # /repos/{owner}/{repo}/contributors
        # /users/{username}/repos

        # Make an API call to check that User can access the repo
        response = connector_obj.get_req(f"{repo_api_link}/collaborators/{github_username}/permission", '.json')
        if response.status_code != 200:
            return {'error': f"Error: {response.text} !"}

        json_data = response.json()
        if json_data.get('permission') and json_data['permission'] != 'none':
            return {}
        return {'error': f"You are not in the collaborators of the repo '{self.name}' !"}
