# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models
from odoo.fields import Command

# For project stages

class sh_project_project(models.Model):
    _name = 'project.project'
    _inherit = ['project.project','mail.thread','mail.activity.mixin']

    project_type_selection = fields.Selection([("internal", "Internal"),
                            ("external", "External")],
                            tracking=True,
                            required=True
                        )
    
    stage_id = fields.Many2one('project.project.stage', string='Stage',
                               ondelete='restrict', tracking=True, index=True, copy=False)

    # for project stages

    sh_stage_ids = fields.Many2many('project.task.type',
                                    'project_task_type_rel',
                                    'project_id',
                                    'type_id',
                                    string="Stages")
    responsible_user_ids = fields.Many2many('res.users',
                                            string="Default Responsible User",tracking=True)
    sh_stage_template_id = fields.Many2one(
        'sh.project.stage.template',string="Stage Template",tracking=True)
    
    sh_technical_head = fields.Many2one("res.users",string="Technical Head",domain=[('share', '=', False)],tracking=True)
    sh_designing_head = fields.Many2one("res.users",string="Designing Head",domain=[('share', '=', False)],tracking=True)
    sh_deadline_n_estimated_hours_mendatory = fields.Boolean("Deadline & Estimated Hours field mandatory?", default=True,tracking=True)
    is_task_editable_in_done_stage = fields.Boolean("Is Task Editable In Done Stage?",default=False,tracking=True)
    sl_can_create_task = fields.Boolean("SL Can create Task?",default=False,tracking=True)
    support_start_date = fields.Date("Support Start Date",tracking=True)
    support_end_date = fields.Date("Support End Date",tracking=True)

    def write(self, vals):
        for rec in self:
            # To Close all tasks of project when project is closed
            if rec.company_id.close_project_stage_ids and rec.company_id.done_project_stage_id and rec.task_ids:
                if vals.get('stage_id') and vals.get('stage_id') in rec.company_id.close_project_stage_ids.ids:
                    for task in rec.task_ids:
                        task.write({'stage_id':rec.company_id.done_project_stage_id.id })
                        if task.child_ids:
                            task.child_ids.write({'stage_id':rec.company_id.done_project_stage_id.id })
                        
        return super(sh_project_project, self).write(vals)

    # def write(self, vals):
    #     for rec in self:
    #         # To Close all tasks of project when project is closed
    #         if self.company_id.close_project_stage_ids and self.company_id.done_project_stage_id and rec.task_ids:
    #             if vals.get('stage_id') and vals.get('stage_id') in self.company_id.close_project_stage_ids.ids:
    #                 for task in rec.task_ids:
    #                     task.write({'stage_id':self.company_id.done_project_stage_id.id })
    #                     if task.child_ids:
    #                         task.child_ids.write({'stage_id':self.company_id.done_project_stage_id.id })
                        
    #     return super(sh_project_project, self).write(vals)

    def _mail_track(self, tracked_fields, initial_values):
        """Override to add tracking for Many2many fields."""
        changes, tracking_value_ids = super()._mail_track(tracked_fields, initial_values)

        # Handle tracking for custom_m2m_field
        if 'responsible_user_ids' in changes:
            field = self.env['ir.model.fields']._get(self._name, 'responsible_user_ids')
            old_values = initial_values.get('responsible_user_ids', self.env['res.users'])
            new_values = self.responsible_user_ids
            old_value_names = ', '.join(old_values.mapped('name')) if old_values else 'None'
            new_value_names = ', '.join(new_values.mapped('name')) if new_values else 'None'

            if old_value_names != new_value_names:
                tracking_value_ids.append(Command.create({
                    'field': field.id,
                    'field_desc': field.field_description,
                    'field_type': field.ttype,
                    'tracking_sequence': field.tracking,
                    'old_value_char': old_value_names,
                    'new_value_char': new_value_names,
                }))

        return changes, tracking_value_ids