# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models, api


class CreateTaskWizard(models.TransientModel):

    _name = "sh.create.new.task.wizard"
    _description = "reshedule wizard details"

    def _get_default_note(self):
        text = "True"
        parent_id = self.env.context.get("active_id")
        parent_model = self.env.context.get("active_model")
        parent_record = self.env[parent_model].browse(parent_id)
        text_list = []
        for i in parent_record.invoice_line_ids:
            if i.product_id.sh_technical_name and  i.product_id.name  and i.name:
                text_list.append("<b>" + i.product_id.name + "</b>" + "  " +
                                 "(" + i.product_id.sh_technical_name + ")" +
                                 "<br/>" + i.name + "<br/>" + "<br/>")
            elif i.product_id.name and i.name  :
                text_list.append("<b>" + i.product_id.name + "</b>" + "<br/>" +
                                 i.name + "<br/>" + "<br/>")
        return text_list

    title = fields.Char(required=True)
    project_id = fields.Many2one('project.project', required=True)
    user_id = fields.Many2one("res.users", string="Assign To", required=True,domain=[('share', '=', False)])
    description = fields.Html(default=_get_default_note)
    sh_responsible_user_ids = fields.Many2many('res.users',string='Responsible Users',domain=[('share','=',False)])
    sh_deadline = fields.Date('Deadline')

    @api.model
    def default_get(self,fields_list):
        res = super(CreateTaskWizard, self).default_get(fields_list)
        parent_id = self.env.context.get("active_id")
        parent_model = self.env.context.get("active_model")
        parent_record = self.env[parent_model].browse(parent_id)
        if parent_record.invoice_date_due:
            res.update({
                'sh_deadline':parent_record.invoice_date_due
            })
        if parent_record.responsible_user_ids:
            res.update({
                'sh_responsible_user_ids':[(6, 0, parent_record.responsible_user_ids.ids)]
            })
        if parent_record.responsible_user_id:
            res.update({
                'user_id': parent_record.responsible_user_id.id
            })
        return res

    def create_task(self):
        project_task = self.env['project.task']
        parent_id = self.env.context.get("active_id")
        parent_model = self.env.context.get("active_model")
        parent_record = self.env[parent_model].browse(parent_id)
        project_task_id = project_task.create({
            'name':
            self.title,
            'project_id':
            self.project_id.id,
            'user_id':
            self.user_id.id,
            'description':
            self.description,
            'account_move_id':
            parent_record.id,
            'date_deadline':
            self.sh_deadline,
            "version_ids": [(6, 0, parent_record.version_ids.ids)],
            "user_ids": [(6, 0, self.sh_responsible_user_ids.ids)]
        })
        parent_record.write({'project_task_id': [(4, project_task_id.id)]})
