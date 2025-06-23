# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models


class SyncBranch(models.Model):
    _inherit = "sh.git.repo"

    def _get_api_link(self):
        try:
            if "/" not in self.repo_link:
                return False
            repo_link_list = self.repo_link.split("/")
            repo_owner = repo_link_list[-2]
            repo_name = repo_link_list[-1].replace(".git", "")
            return f'https://api.github.com/repos/{repo_owner}/{repo_name}'
        except Exception as e:
            return False

    # ====================================================
    #  Import Branch(s)
    # ====================================================
    def import_branch(self):
        connector_obj = self.env['sh.github.connector'].sudo().search(
            [('state', '=', 'success')], limit=1)
        if not connector_obj:
            return False
        if not connector_obj.access_token:
            connector_obj.create_log('import', 'branch',
                                     'Plsease Generate Access Token First!')
            return False

        # Sync Branch
        repo_link = self._get_api_link()
        if not repo_link:
            connector_obj.create_log('import', 'branch', f'Plsease Insert the Proper Repo({self.name}) Link!')
            return False
        response = connector_obj.get_req(f'{repo_link}/branches', '.json')
        if response.status_code != 200:
            connector_obj.create_log('import', 'branch', response.text)
        else:
            counter = 0
            if not len(response.json()) > 0:
                connector_obj.create_log(
                    'import', 'branch', 'Branch(s) Not Found fot This Repo({self.name}).')
                return False
            for branch in response.json():
                try:
                    float(branch.get('name'))
                except ValueError:
                    continue
                find_branch = self.env['sh.repo.branch'].sudo().search([
                    ('name', '=', branch.get('name')),
                    ('repo_id', '=', self.id)
                ])
                if not find_branch:
                    # counter += 1
                    counter += self.sudo().write({
                        'branch_line': [(0, 0, {'name': branch.get('name')})]
                    })

            if counter > 0:
                connector_obj.create_log(
                    'import', 'branch', f'{counter} Branch(s) Imported/Edited Successfully for Repo({self.name}).', 'success')
                return counter
            else:
                connector_obj.create_log(
                    'import', 'branch', f'Branch(s) Already Imported for Repo({self.name}).', 'success')
                return 0
