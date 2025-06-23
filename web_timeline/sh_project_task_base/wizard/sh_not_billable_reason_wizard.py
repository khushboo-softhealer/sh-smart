# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ShNotBillableReason_wizard(models.TransientModel):
    _name = 'sh.not.billable.reason.wizard'
    _description = "Not Billable Reason Wizard"

    reason = fields.Char(string="Add a Reason")
    
    def save(self):
        
        if self.reason:
            task_id = self.env.context.get('task_id_not_billable_boolean_wizard')

            if task_id:
                task = self.env['project.task'].sudo().browse(task_id)
                task.write({'not_billable': True})
                reason = self.reason + " (Not Billable Reason)"
                task.message_post(body=reason)
                return {
                            'type': 'ir.actions.act_window',
                            'res_model': 'project.task',
                            'res_id': task.id,
                            'view_mode': 'form',
                            'views': [[False, 'form']],
                            'target': 'current',
                            }



        else:
            raise ValidationError(_("Add a Valid Reason."))
    
    def cancel(self):
        task_id = self.env.context.get('task_id_not_billable_boolean_wizard')
        if task_id:
            task = self.env['project.task'].sudo().browse(task_id)
            task.write({'not_billable': False})

            return {
                            'type': 'ir.actions.act_window',
                            'res_model': 'project.task',
                            'res_id': task.id,
                            'view_mode': 'form',
                            'views': [[False, 'form']],
                            'target': 'current',}

        