# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api


class ProductChangeLog(models.Model):
    _name = 'product.change.log'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "version desc"
    _description = "Product Change Log"

    product_id = fields.Many2one(
        'product.template', string='Product Id', tracking=True)
    product_variant_id = fields.Many2one(
        'product.product', string='Product Id ', tracking=True)
    project_task_id = fields.Many2one(
        'project.task', string="Task Id", tracking=True)
    version = fields.Char('Version', tracking=True)
    details = fields.Text('Details', tracking=True)
    date = fields.Date("Date", tracking=True)
    log_type = fields.Selection(
        [('fix', 'Fix'), ('add', 'Add'), ('update', 'Update')], string="Type", tracking=True)
    company_id = fields.Many2one('res.company', string='Company',
        default=lambda self: self.env.company)
    
    # @api.model_create_multi
    # def create(self, vals_list):
    #     res = super(ProductChangeLog, self).create(vals_list)
        # for vals in vals_list:
            # product_tmplt = res.product_variant_id.product_tmpl_id
            # templates = self.env['product.template'].search(
            #     [('individual_modules.id', '=', product_tmplt.id)])
            # tasks = templates.mapped('related_task')

            # # add to task as well
            # if res.product_variant_id.related_sub_task:
            #     res.sudo().write(
            #         {'project_task_id': res.product_variant_id.related_sub_task.id})

            # for task in tasks:
            #     # find subtask
            #     subtasks = self.env['project.task'].sudo().search(
            #         [('parent_id', '=', task.id)])
            #     for subtask in subtasks:
            #         for rec in res.product_variant_id.attribute_value_ids:
            #             if subtask.version_ids and subtask.version_ids[0].name == rec.name:

            #                 subtask.write({
            #                     'stage_id': self.env.user.company_id.sh_downgrade_task_stage_id.id
            #                 })
            #                 self.env['sh.task.upcoming.feature'].sudo().create({
            #                     'user_id': self.env.user.id,
            #                     'date': fields.Date.today(),
            #                     'description': "Please check in Individual module update.\n"+(res.product_variant_id.name or '')+':\n'+(res.version or '')+":\n" + (res.details or ''),
            #                     'task_id': subtask.id
            #                 })
            #                 self.env['mail.message'].sudo().create({
            #                     'subject': 'Please fix issue in downgrade versions.',
            #                     'date': fields.Datetime.now(),
            #                     'author_id': self.env.user.partner_id.id,
            #                     'record_name': subtask.name,
            #                     'model': 'project.task',
            #                     'res_id': subtask.id,
            #                     'message_type': 'comment',
            #                     'subtype_id': self.env.ref('mail.mt_note').id,
            #                     'body': "Please check in Individual module update. Module Name : " + res.product_variant_id.name+' , Details : ' + res.details,
            #                 })                                                        
        # return res
