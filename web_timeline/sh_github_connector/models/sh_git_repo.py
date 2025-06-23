# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime


class ShGitRepo(models.Model):
    _inherit = 'sh.git.repo'

    branch_line = fields.One2many(
        'sh.repo.branch', 'repo_id', string='Branch Line')

    last_sync_date = fields.Datetime('Last Sync Date')
    other_responsible_user_ids = fields.Many2many(
        'res.users', string='Other Responsible Users')

    # ====================================================
    #  Unique Repo Link
    # ====================================================
    _sql_constraints = [('repo_link_uniq', 'unique (repo_link)',
                         "The field 'Repo Link' must be unique per repo!")]

    # ---------------------------------
    #  Sync Branch
    # ---------------------------------

    def _sync_branch(self, connector_obj, branch_obj, url):
        try:
            brnach_response = connector_obj.get_req(url)
            if brnach_response.status_code != 200:
                return 'Failed to get response from gitub !\n'
            queue = create = no_sha = upto_date = 0
            failed_list = []
            for data in brnach_response.json():
                if data.get('type') != 'dir':
                    continue
                if connector_obj.ignore_dir:
                    if data.get('name') in connector_obj.ignore_dir:
                        continue
                module_obj = self.env['sh.module'].sudo().search([
                    ('name', '=', data.get('name')),
                    ('sh_branch_id', '=', branch_obj.id)
                ])
                if module_obj:
                    if module_obj.sha:
                        if module_obj.sha != data.get('sha'):
                            # change in commit of module
                            # means module is updated (pushed something in it)
                            # so, state in draft
                            module_obj.sudo().write({
                                'state': 'draft',
                                'message': '',
                                'sha': data.get('sha')
                            })
                            queue += 1
                        else:
                            upto_date += 1
                    else:
                        # Module dosn't have the sha
                        no_sha += 1
                        module_obj.write({
                            'sha': data.get('sha'),
                            'state': 'draft',
                            'message': 'Missing comment id !',
                        })
                else:
                    if not data.get('url'):
                        failed_list.append(data.get('name'))
                        continue
                    module_obj = self.env['sh.module'].sudo().create({
                        'name': data.get('name'),
                        'sh_branch_id': branch_obj.id,
                        'sh_module_url':  data.get('url'),
                        'state': 'draft',
                        'sha': data.get('sha')
                    })
                    create += 1
            message = ''
            if create:
                message += f'{create} module(s) are created.\n'
            if queue:
                message += f'{queue} module(s) are added in the queue.\n'
            if no_sha:
                message += f"{no_sha} module(s) dosn't contain the sha.\n"
            if upto_date:
                message += f"{upto_date} module(s) are upto date.\n"
            if failed_list:
                message += f'{len(failed_list)} module(s) are failed to sync cause not getting its url!\nFailed list:\n{failed_list}\n'

            return message
        except Exception as e:
            return f'Error: {e}\n'

    # ---------------------------------
    #  Is Repo Changed
    # ---------------------------------

    def _is_repo_changed(self, owner, repo, connector):
        if not self.last_sync_date:
            self.last_sync_date = datetime.now()
            return True
        url = f'https://api.github.com/repos/{owner}/{repo}'
        response = connector.get_req(url)
        if response.status_code != 200:
            connector.create_log(
                'cron', 'repo', f'Failed to get the api response ! Code: {response.status_code}, Error: {response.text}')
            return False
        json_data = response.json()
        pushed_at = json_data.get('pushed_at')
        if not pushed_at:
            connector.create_log(
                'cron', 'repo', "Failed to get the 'pushed_at' from the api response !")
            return False
        pushed_at = datetime.strptime(pushed_at, '%Y-%m-%dT%H:%M:%SZ')
        if pushed_at > self.last_sync_date:
            # Repo is updated, so need to sync
            return True
        connector.create_log(
            'cron', 'repo', f'Repo({self.name}) is upto date.', 'success')
        self.last_sync_date = datetime.now()
        return False

    # ---------------------------------
    #  Sync Repo
    # ---------------------------------

    def _sync_repo(self, connector):

        if "/" not in self.repo_link:
            connector.create_log(
                'cron', 'repo', f'{self.name}: Plsease insert the proper repo link !')
            return

        if not self.branch_line:
            connector.create_log(
                'cron', 'repo', f'{self.name}: Import the branch first !')
            return

        repo_link_list = self.repo_link.split("/")
        repo_owner = repo_link_list[-2]
        repo_name = repo_link_list[-1].replace(".git", "")
        branch_url_tmpl = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents?ref=%s'
        repo_changed = self._is_repo_changed(repo_owner, repo_name, connector)
        if not repo_changed:
            return

        message = ''
        for branch in self.branch_line:
            branch_url = branch_url_tmpl % (branch.name)
            message += f'\n{branch.name}: '
            message += self._sync_branch(connector, branch, branch_url)
        self.last_sync_date = datetime.now()
        if message:
            message = f'{self.name}:\n{message}'
            connector.create_log('cron', 'repo', message, state='sync')
        else:
            connector.create_log(
                'cron', 'repo', f'{self.name} is upto date.', state='success')

    # ---------------------------------
    #  CRON: Sync All Repos
    # ---------------------------------

    def _cron_sync_all_repos(self):
        repos = self.env['sh.git.repo'].sudo().search([])
        connector = self.env['sh.github.connector'].sudo().search([
            ('state', '=', 'success')
        ], limit=1)
        if not repos:
            # connector.create_log(
            #     'cron', 'repo', "Can't find any repo to sync !")
            return False
        if not connector:
            connector.create_log(
                'cron', 'repo', 'Please generate access token first to sync with github !')
            return False
        for repo in repos:
            repo._sync_repo(connector)

    # ---------------------------------
    #  Sync New Products
    # ---------------------------------

    def action_get_new_products(self):
        try:
            connector_obj = self.env['sh.github.connector'].sudo().search(
                [('state', '=', 'success')], limit=1)
            if not connector_obj:
                raise UserError(
                    _('Please generate access token first to sync with github.'))
            message = ''
            for rec in self:
                repo_msg = rec.btn_sync_new_products(connector_obj, False)
                if repo_msg:
                    message += f"\nRepo: '{rec.name}':\n{repo_msg}\n"
            if not message:
                message = 'No found any new products.'
            return self.popup_message('Sync New Products', message)
        except Exception as e:
            return self.popup_message('Sync New Products', f'Error: {e}')

    # ====================================================
    #  Get New Products In Module Queue
    # ====================================================
    def btn_sync_new_products(self, connector_obj=False, show_message=True):
        try:
            message = ''
            if not connector_obj:
                connector_obj = self.env['sh.github.connector'].sudo().search(
                    [('state', '=', 'success')], limit=1)
                if not connector_obj:
                    message = 'Please generate access token first to sync with github.'
                    if show_message:
                        raise UserError(_(message))
                    else:
                        return message
            if "/" not in self.repo_link:
                message = f'Plsease Insert the Proper Repo({self.name}) Link!'
                connector_obj.create_log('sync', 'branch', message)
                if show_message:
                    raise UserError(_(message))
                else:
                    return message
            # Get Repo Name And Its Owner
            repo_link_list = self.repo_link.split("/")
            owner = repo_link_list[-2]
            repo = repo_link_list[-1].replace(".git", "")
            # Loop through all the branch
            for branch in self.branch_line:
                url = f'https://api.github.com/repos/{owner}/{repo}/contents?ref={branch.name}'
                branch_message = branch.branch_sync_new_products(
                    connector_obj, url)
                if branch_message:
                    message += f'\nFor Branch: \'{branch.name}\':\n{branch_message}'
            if not message:
                message = 'Not found any new products to sync.'
            if show_message:
                return self.popup_message('Sync New Products', message)
            else:
                return message
        except Exception as e:
            if show_message:
                return self.popup_message('Sync New Products', f'Error: {e}')
            else:
                return f'Error: {e}'

    # ====================================================
    #  Sync The Repo
    # ====================================================
    def sync_github(self):
        # repos = self.env['sh.git.repo'].sudo().browse(
        #     self.env.context.get('active_ids'))
        repos = self
        connector_obj = self.env['sh.github.connector'].sudo().search(
            [('state', '=', 'success')], limit=1)
        if not connector_obj:
            raise UserError(
                _('Please generate access token first to sync with github.'))
        # counter = 0
        message = ''
        for repo in repos:
            repo_messgae = connector_obj.sync_repo(repo)
            if repo_messgae:
                message += f'Repo: \'{repo.name}\'{repo_messgae}\n'
        if message:
            return self.popup_message('Sync Repo', message)
        return self.popup_message('Sync Repo', 'Nothing Find To Import!')

    def import_branch_action(self):
        try:
            log = {}
            for repo in self:
                log[repo.name] = repo.import_branch()
            if log:
                message = ''
                for repo_name, branch_count in log.items():
                    if not branch_count:
                        if branch_count == 0:
                            message += f'Not Find Any Branch or Its Already Imported For Repo \'{repo_name}\'.\nOr Generate Access Token First.\n'
                            continue
                        message += f'Failed To Get Branch(s) For Repo \'{repo_name}\'.\n'
                        continue
                    message += f'{branch_count} Branch(s) Imported For Repo \'{repo_name}\'.\n'
                # ==== Pop-Up Message ====
                return self.popup_message('Import Branch', message)
        except Exception as e:
            return self.popup_message('Import Branch', f'Error: {e}')

    # ========== Pop-Up Message ==========

    def popup_message(self, title, message):
        view = self.env.ref('sh_message.sh_message_wizard')
        context = dict(self._context or {})
        context['message'] = message
        return {
            'name': title,
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sh.message.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': context
        }

    def is_repo_changed(self, owner, repo, connector_obj):
        if not self.last_sync_date:
            self.last_sync_date = datetime.now()
            return True, ''
        url = f'https://api.github.com/repos/{owner}/{repo}'
        response = connector_obj.get_req(url)
        if response.status_code != 200:
            return False, f'Failed to get the api response ! Code: {response.status_code}, Error: {response.text}'
        json_data = response.json()
        pushed_at = json_data.get('pushed_at')
        if not pushed_at:
            return False, "Failed to get the 'pushed_at' from the api response !"
        pushed_at = datetime.strptime(pushed_at, '%Y-%m-%dT%H:%M:%SZ')
        if pushed_at > self.last_sync_date:
            # Repo is updated
            return True, ''
        self.last_sync_date = datetime.now()
        return False, 'Repo is upto date.'

    def sync_branch(self, connector_obj, branch_obj, url):
        try:
            brnach_response = connector_obj.get_req(url)
            if brnach_response.status_code != 200:
                # return f'Failed to get response from gitub for branch {branch_obj.name}'
                return []
            queue = failed = create = no_sha = 0
            failed_list = []
            module_list = []
            for data in brnach_response.json():
                if data.get('type') != 'dir':
                    continue
                if connector_obj.ignore_dir:
                    if data.get('name') in connector_obj.ignore_dir:
                        continue
                #  If Module
                module_obj = self.env['sh.module'].sudo().search([
                    ('name', '=', data.get('name')),
                    ('sh_branch_id', '=', branch_obj.id)
                ])
                if module_obj:
                    if module_obj.sha:
                        if module_obj.sha != data.get('sha'):
                            # change in commit of module
                            # means module is updated (pushed something in it)
                            # so, state in draft
                            # module_obj.sudo().write({
                            #     'state': 'draft',
                            #     'message': '',
                            #     'sha': data.get('sha')
                            # })
                            queue += 1
                            # ===================
                            module_list.append((0, 0, {
                                'name': data.get('name'),
                                'module_id': module_obj.id,
                                'sh_branch_id': branch_obj.id,
                                'sha': data.get('sha')
                            }))
                    else:
                        # Module dosn't have the sha
                        no_sha += 1
                        # module_obj.write({
                        #     'sha': data.get('sha')
                        # })
                        # ===================
                        module_list.append((0, 0, {
                            'name': data.get('name'),
                            'module_id': module_obj.id,
                            'sha': data.get('sha'),
                            'sh_branch_id': branch_obj.id,
                            'comment': 'Missing comment id !',
                        }))
                else:
                    if not data.get('url'):
                        failed += 1
                        failed_list.append(data.get('name'))
                        continue
                    # module_obj = self.env['sh.module'].sudo().create({
                    #     'name': data.get('name'),
                    #     'sh_branch_id': branch_obj.id,
                    #     'sh_module_url':  data.get('url'),
                    #     'state': 'draft',
                    #     'sha': data.get('sha')
                    # })
                    create += 1
                    # ===================
                    module_list.append((0, 0, {
                        'name': data.get('name'),
                        'sh_branch_id': branch_obj.id,
                        'sh_module_url': data.get('url'),
                        'sha': data.get('sha'),
                        'comment': 'New',
                    }))
            message = ''
            if create:
                message += f'{create} module(s) are created.\n'
            if queue:
                message += f'{queue} module(s) are added in the queue.\n'
            if no_sha:
                message += f"{no_sha} module(s) dosn't contain the sha.\n"
            if failed:
                message += f'{failed} module(s) are failed to sync cause not getting its url!\nFailed list:\n{failed_list}'

            # return message
            # ===================
            return module_list
        except Exception as e:
            # return e
            return []

    def _get_updated_modules(self, connector_obj=False):
        if not connector_obj:
            connector_obj = self.env['sh.github.connector'].sudo().search(
                [('state', '=', 'success')], limit=1)
        if not connector_obj:
            return 'Generate the credentials first !'

        if not self.branch_line:
            return 'Import the branch first !'

        if "/" not in self.repo_link:
            return f'Plsease insert the proper repo link !'

        repo_link_list = self.repo_link.split("/")
        repo_owner = repo_link_list[-2]
        repo_name = repo_link_list[-1].replace(".git", "")
        branch_url_tmpl = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents?ref=%s'
        message = ''
        repo_changed, message = self.is_repo_changed(
            repo_owner, repo_name, connector_obj)
        if not repo_changed:
            return message

        module_list = []
        for branch in self.branch_line:
            branch_url = branch_url_tmpl % (branch.name)
            module_list += self.sync_branch(
                connector_obj, branch, branch_url)
        if module_list:
            return module_list
        self.last_sync_date = datetime.now()
        return 'Repo is up to date.'

    def btn_sync_repo_wizard(self):
        return_val = self._get_updated_modules()
        if type(return_val) == str:
            return self.popup_message('Sync Repo', return_val)
        if type(return_val) == list:
            return {
                'name': 'Sync Repo',
                'type': 'ir.actions.act_window',
                'res_model': 'sh.repo.wizard',
                'view_type': 'form',
                'view_mode': 'form',
                'context': {
                    'repo': self.id,
                    'sh_repo_wizard_lines': return_val
                },
                'target': 'new',
                'view_id': self.env.ref('sh_github_connector.sh_sync_repo_wizard_view_form').id,
            }
        return self.popup_message('Sync Repo', f'Something went wrong !\n{return_val}')
