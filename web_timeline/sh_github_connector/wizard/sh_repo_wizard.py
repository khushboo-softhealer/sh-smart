# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields
from datetime import datetime


class ShSyncRepoWizard(models.TransientModel):
    _name = 'sh.repo.wizard'
    _description = 'Repo Wizard'
    _rec_name = 'repo'

    repo = fields.Many2one('sh.git.repo', string='Repo')
    sh_repo_wizard_lines = fields.One2many('sh.repo.wizard.lines', 'sh_repo_wizard_id', string='Module Line')

    def default_get(self, fields_list):
        vals = super().default_get(fields_list)
        context = self.env.context
        vals.update({
            'repo': context.get('repo'),
            'sh_repo_wizard_lines': context.get('sh_repo_wizard_lines')
        })
        return vals

    def btn_add_to_queue(self):
        self.repo.last_sync_date = datetime.now()
        created = queue = 0
        not_sha_list = []
        not_url_list = []
        for line in self.sh_repo_wizard_lines:
            if not line.sha:
                not_sha_list.append(line.name)
                continue
            if line.module_id:
                line.module_id.sudo().write({
                    'sha': line.sha,
                    'state': 'draft',
                    'message': ''
                })
                queue += 1
            else:
                if not line.sh_module_url:
                    not_url_list.append(line.name)
                    continue
                self.env['sh.module'].sudo().create({
                    'name': line.name,
                    'sh_branch_id': line.sh_branch_id.id,
                    'sh_module_url':  line.sh_module_url,
                    'state': 'draft',
                    'sha': line.sha
                })
                created += 1
        message = ''
        if queue:
            message += f'{queue} module(s) added in the queue.'
        if created:
            message += f'\n{created} module(s) are created.'
        if not message:
            message += "Can't find any module !"
        message = f'{self.repo.name}: {message}'
        self.env['sh.git.repo'].popup_message('Module In Queue', message)
        connector_obj = self.env['sh.github.connector']
        connector_obj.create_log('sync', 'repo', message, 'success')
        message = ''
        if not_sha_list:
            message += f'Not found sha for {not_sha_list} !\n'
        if not_url_list:
            message += f'Not found url for {not_url_list} !'
        if message:
            message = f'{self.repo.name}: {message}'
            connector_obj.create_log('sync', 'repo', message)


class ShSyncRepoWizard(models.TransientModel):
    _name = 'sh.repo.wizard.lines'
    _description = 'Module Line'

    name = fields.Char('Name')
    module_id = fields.Many2one('sh.module', string='Module')
    sh_module_url = fields.Char('Url')
    sh_branch_id = fields.Many2one("sh.repo.branch", string="Branch")
    sha = fields.Char('Sha')
    comment = fields.Char('Comment')
    # inverse field
    sh_repo_wizard_id = fields.Many2one(
        'sh.repo.wizard', string='Repo Wizard Id')
