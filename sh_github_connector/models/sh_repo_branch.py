# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class ShRepoBranch(models.Model):
    _name = "sh.repo.branch"
    _description = "Repo Branch"

    name = fields.Char('Name')
    # Inverse Field
    repo_id = fields.Many2one('sh.git.repo', string='Git Repo Ref')
    module_line = fields.One2many(
        'sh.module', 'sh_branch_id', string='Module Line')

    # ====================================================
    #  Get New Products In Module Queue For A Branch
    # ====================================================
    def branch_sync_new_products(self, connector_obj, url):
        try:
            brnach_response = connector_obj.get_req(url)
            if brnach_response.status_code != 200:
                return brnach_response.text
            queue = failed = 0
            failed_list = []
            for data in brnach_response.json():
                if data.get('type') == 'dir':
                    if connector_obj.ignore_dir:
                        if data.get('name') in connector_obj.ignore_dir:
                            continue
                    module_obj = self.env['sh.module'].sudo().search([
                        ('name', '=', data.get('name')),
                        ('sh_branch_id', '=', self.id)
                    ])
                    if not module_obj:
                        if not data.get('url'):
                            failed += 1
                            failed_list.append(data.get('name'))
                            continue
                        module_obj = self.env['sh.module'].sudo().create({
                            'name': data.get('name'),
                            'sh_branch_id': self.id,
                            'sh_module_url':  data.get('url'),
                            'state': 'draft',
                            'sha': data.get('sha')
                        })
                        queue += 1
            message = ''
            if queue:
                message += f'{queue} module(s) added in the queue.\n'
            if failed:
                message += f'{failed} module(s) failed to sync cause not getting its url!\nFailed list:\n{failed_list}'
            return message
        except Exception as e:
            return f'Error: {e}'

    # ====================================================
    #  Add/Update Module Queue For A Branch
    # ====================================================
    def sync_branch(self, pop_up=True):
        try:
            connector_obj = self.env['sh.github.connector'].sudo().search(
                [('state', '=', 'success')], limit=1)
            if not connector_obj:
                message = 'Please Generate Access Token First To Sync Branch !'
                if pop_up:
                    return self.repo_id.popup_message('Sync Branch', message)
                return message

            if "/" not in self.repo_id.repo_link:
                message = f'Plsease Insert the Proper Repo({self.repo_id.name}) Link !'
                connector_obj.create_log('sync', 'branch', message)
                if pop_up:
                    return self.repo_id.popup_message('Sync Branch', message)
                return message
            repo_link_list = self.repo_id.repo_link.split("/")
            repo_owner = repo_link_list[-2]
            repo_name = repo_link_list[-1].replace(".git", "")
            branch_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents?ref={self.name}'
            brnach_response = connector_obj.get_req(branch_url)
            if brnach_response.status_code != 200:
                message = f'Failed to get branch response {self.name} ! Code: {brnach_response.status_code}, Error: {brnach_response.text}'
                if pop_up:
                    return self.repo_id.popup_message('Sync Branch', message)
                return message
            success = failed = queue = 0
            for data in brnach_response.json():
                if data.get('type') == 'dir':
                    if connector_obj.ignore_dir:
                        if data.get('name') in connector_obj.ignore_dir:
                            continue
                    #  If Module
                    module_obj = self.env['sh.module'].sudo().search([
                        ('name', '=', data.get('name')),
                        ('sh_branch_id', '=', self.id)
                    ])
                    if module_obj:
                        module_obj.sudo().write({
                            'state': 'draft',
                            'message': '',
                            'sha': data.get('sha')
                        })
                    else:
                        if not data.get('url'):
                            failed += 1
                            continue
                        module_obj = self.env['sh.module'].sudo().create({
                            'name': data.get('name'),
                            'sh_branch_id': self.id,
                            'sh_module_url':  data.get('url'),
                            'state': 'draft',
                            'sha': data.get('sha')
                        })
                    queue += 1

            message = ''
            if success:
                message += f'{success} Module(s) Sync Successfully.\n'
            if failed:
                message += f'{failed} Module(s) Failed To Sync!\n'
            if queue:
                message += f'{queue} Module(s) Added In Queue.\n'
            if not message:
                message = f"Modules Not Found For The Repo '{self.repo_id.name}', Branch '{self.name}'"
            # if message and self.env.context.get('pop_up'):
            if message and pop_up:
                # ========== Pop-Up Message ==========
                return self.repo_id.popup_message('Sync Branch', f'{message}')
            return message
        except Exception as e:
            message = f'{self.name} Branch Sync Error: {e}'
            if pop_up:
                return self.repo_id.popup_message('Sync Branch', message)
            return message
