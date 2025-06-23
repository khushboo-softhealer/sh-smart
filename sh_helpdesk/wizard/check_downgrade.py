# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api


class CheckDowngradeVersions(models.TransientModel):
    _name = 'sh.check.downgrade'
    _description = 'Check Downgrade'

    sh_task_ids = fields.Many2many('project.task', string="Tasks", domain=[
                                   ('parent_id', '!=', False)])
    sh_description = fields.Html('Description')

    @api.model
    def default_get(self, fields_list):
        res = super(CheckDowngradeVersions, self).default_get(fields_list)
        if self.env.context.get('active_id'):
            ticket_id = self.env[self.env.context.get('active_model')].sudo().browse(
                self.env.context.get('active_id'))
            if ticket_id and ticket_id.product_ids:
                all_products = ticket_id.product_ids
                all_task = []
                
                for product in all_products:
                    if product.product_tmpl_id:
                        main_task_id = self.env['project.task'].sudo().search(
                            [('product_template_id', '=', product.product_tmpl_id.id)])
                        if main_task_id:
                            sub_task_ids = self.env['project.task'].sudo().search([('parent_id', '!=', False), ('sh_product_id', '!=', product.id), (
                                'parent_id.product_template_id', '=', product.product_tmpl_id.id)])
                            all_task = all_task + sub_task_ids.ids
                
                if all_task:
                    res.update({
                        'sh_task_ids': [(6, 0, all_task)]
                    })
        return res

    def action_downgrade(self):
        self.ensure_one()
        if self.env.context.get('active_id'):
            ticket_id = self.env[self.env.context.get('active_model')].sudo().browse(
                self.env.context.get('active_id'))
            if ticket_id:
                for product in ticket_id.product_ids:
                    if product.product_tmpl_id and ticket_id.sh_version_id and ticket_id.sh_check_downgrade:

                        if ticket_id.company_id.done_project_stage_id:

                            current_task_id = self.env['project.task'].sudo().search(
                                [('parent_id', '!=', False), ('sh_product_id', '=', product.id)])
                            if current_task_id:
                                current_task_id.write(
                                    {'stage_id': ticket_id.company_id.done_project_stage_id.id})

                        if ticket_id.company_id.sh_downgrade_task_stage_id:
                            if self.sh_task_ids:
                                for task in self.sh_task_ids:
                                    task.write(
                                        {'stage_id': ticket_id.company_id.sh_downgrade_task_stage_id.id})
                                    self.env['mail.message'].sudo().create({
                                        'subject': 'Please fix issue in downgrade versions.',
                                        'date': fields.Datetime.now(),
                                        'author_id': self.env.user.partner_id.id,
                                        'record_name': task.name,
                                        'model': 'project.task',
                                        'res_id': task.id,
                                        'message_type': 'comment',
                                        'subtype_id': self.env.ref('mail.mt_note').id,
                                        'body': self.sh_description,
                                    })
                                ticket_id.sh_click_downgrade = True
