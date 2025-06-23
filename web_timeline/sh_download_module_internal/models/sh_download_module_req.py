# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from datetime import datetime, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ShDownloadModuleReq(models.Model):
    _name = "sh.download.module.req"
    _description = "Download Module Req"
    _order = "create_date desc"
    _rec_name="create_date"

    active = fields.Boolean('Active', default=True)
    module_ids = fields.Many2many('sh.module', string='Modules')
    for_which = fields.Selection([
        ('project', 'Project'),
        ('ticket', 'Ticket')
    ], string='For Which')
    project_id = fields.Many2one('project.project', string='Project')
    task_id = fields.Many2one('project.task', string='Task')
    is_tl = fields.Boolean('Is TL', compute='_compute_is_login_user_is_tl')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('granted', 'Granted'),
        ('denied', 'Denied')
    ], string='State', default='draft')
    ticket_id = fields.Many2one('sh.helpdesk.ticket', string='Ticket')
    request_token = fields.Char('Request Token')
    # wizard_ref = fields.Char('Wizard Reference')
    approved_by_id = fields.Many2one('res.users', string='Approved By')

    def _compute_is_login_user_is_tl(self):
        for req in self:
            is_login_user_tl = False
            # If project is app store
            if req.project_id.id == self.env.company.appstore_project_id.id:
                is_login_user_tl = self.env.user.has_group('sh_download_module_internal.sh_appstore_module_req_manager')
            else:
                is_login_user_tl = self.env.user.has_group('sh_project_task_base.group_project_officer')
            req.is_tl = is_login_user_tl

    def _create_bell_notification(self, title):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        self.env['user.push.notification'].push_notification(
            list_of_user_ids=[self.create_uid],
            title=title,
            message=f"For Modules: {', '.join([module.name for module in self.module_ids])}",
            link=f'{base_url}/mail/view?model=sh.download.module.req&res_id={str(self.id)}',
            res_model='sh.download.module.req',
            res_id=self.id,
            type='project'
        )

    def btn_req_granted(self):
        self.write({
            'state': 'granted',
            'approved_by_id': self.env.user.id
        })

        self._create_bell_notification("Module Request Accepted")

    def btn_req_denied(self):
        self.write({
            'state': 'denied',
            'approved_by_id': self.env.user.id
        })
        self._create_bell_notification("Module Request Denied")

    def btn_download_modules(self):
        if not self.module_ids:
            return False

        # Manage the log when downloading the modules
        self.env['sh.download.module.log'].create({
            'module_ids': [(6, 0, self.module_ids.ids)],
            'for_which': self.for_which,
            'project_id': self.project_id.id,
            'task_id': self.task_id.id,
            'ticket_id': self.ticket_id.id
        })
        return {'type': 'ir.actions.act_url', 'url': f"/github/sh_download_module_internal?request_token={self.request_token}", 'target': 'self'}


    def cron_delete_download_requests(self):
        records = self.search([
            ('create_date', '<', datetime.now() - timedelta(1))
        ])
        if records:
            records.write({
                'active': False
            })

    @api.model_create_multi
    def create(self, vals_list):
        if not self.env.context.get('from_wizard'):
            raise UserError(_("Something want wrong !"))
        return super().create(vals_list)
    
