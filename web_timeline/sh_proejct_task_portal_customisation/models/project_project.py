# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models,api,_
from odoo.exceptions import UserError, ValidationError, AccessError

PROJECT_TASK_READABLE_FIELDS = {
    'id',
    'active',
    'priority',
    'kanban_state_label',
    'project_id',
    'display_project_id',
    'color',
    'partner_is_company',
    'commercial_partner_id',
    'allow_subtasks',
    'subtask_count',
    'child_text',
    'is_closed',
    'email_from',
    'create_date',
    'write_date',
    'company_id',
    'displayed_image_id',
    'display_name',
    'portal_user_names',
    'legend_normal',
    'legend_blocked',
    'legend_done',
    'user_ids',
    'display_parent_task_button',
    'allow_milestones',
    'milestone_id',
    'has_late_and_unreached_milestone',
}

PROJECT_TASK_WRITABLE_FIELDS = {
    'name',
    'description',
    'partner_id',
    'date_deadline',
    'tag_ids',
    'sequence',
    'stage_id',
    'kanban_state',
    'child_ids',
    'parent_id',
    'priority',
    'stage_history_line',
    'user_ids',
    'date_assign',
    'legend_done',
    'is_closed',
}

class ProjectTask(models.Model):
    _inherit = 'project.task'
    

    def _ensure_fields_are_accessible(self, fields, operation='read', check_group_user=True):
        """" ensure all fields are accessible by the current user

            This method checks if the portal user can access to all fields given in parameter.
            By default, it checks if the current user is a portal user and then checks if all fields are accessible for this user.

            :param fields: list of fields to check if the current user can access.
            :param operation: contains either 'read' to check readable fields or 'write' to check writable fields.
            :param check_group_user: contains boolean value.
                - True, if the method has to check if the current user is a portal one.
                - False if we are sure the user is a portal user,
        """
        assert operation in ('read', 'write'), 'Invalid operation'
        if fields and (not check_group_user or self.env.user.has_group('base.group_portal')) and not self.env.su:
            unauthorized_fields = set(fields) - (self.SELF_READABLE_FIELDS if operation == 'read' else self.SELF_WRITABLE_FIELDS)
            if 'description' in unauthorized_fields:
                unauthorized_fields.remove('description')
            if 'stage_history_line' in unauthorized_fields:
                unauthorized_fields.remove('stage_history_line')
            if 'user_ids' in unauthorized_fields:
                unauthorized_fields.remove('user_ids')
            if 'date_assign' in unauthorized_fields:
                unauthorized_fields.remove('date_assign')
            if unauthorized_fields:
                if operation == 'read':
                    error_message = _('You cannot read %s fields in task.', ', '.join(unauthorized_fields))
                else:
                    error_message = _('You cannot write on %s fields in task.', ', '.join(unauthorized_fields))
                raise AccessError(error_message)
    
    @api.model_create_multi
    def create(self,vals_list):
        res = super(ProjectTask, self).create(vals_list)
        for rec in res:
            if self.env.user.has_group('base.group_portal') and rec.project_id.sudo().user_id.sudo():
                base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                self.env['user.push.notification'].push_notification([rec.project_id.sudo().user_id.sudo()], 'New Task Created By ' +str(self.env.user.name)+' !', 'Task : %s:' % (
                                rec.name), base_url+"/mail/view?model=project.task&res_id="+str(rec.id), 'project.task', rec.id,'project')
        return res

    def write(self,vals):
        for rec in self:
            if vals.get('stage_id') and self.env.user.has_group('base.group_portal') and rec.project_id.sudo().user_id.sudo():
                base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                self.env['user.push.notification'].sudo().push_notification([rec.project_id.sudo().user_id.sudo()], 'Stage Changed By ' +str(self.env.user.name)+' !', 'Task : %s:' % (
                                rec.name), base_url+"/mail/view?model=project.task&res_id="+str(rec.id), 'project.task', rec.id,'project')
        return super(ProjectTask,self).write(vals)


    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):
        if self._name == 'project.task' and 'author_id' in kwargs and kwargs.get('author_id'):
            user_id = self.env['res.users'].sudo().search([('partner_id','=',kwargs.get('author_id'))],limit=1)
            if user_id.has_group('base.group_portal'):
                base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                self.env['user.push.notification'].push_notification([self.project_id.user_id], str(self.env.user.name)+' Replied !', 'Task : %s:' % (
                                self.name), base_url+"/mail/view?model=project.task&res_id="+str(self.id), 'project.task', self.id,'project')
        return super(ProjectTask, self.with_context(mail_post_autofollow=True)).message_post(**kwargs)

    def action_preview_task_portal(self):
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url') + '/my/projects/'+str(self.project_id.id)
        return {
            "type": "ir.actions.act_url",
            "target": 'current',
            "url": base_url,
        }

