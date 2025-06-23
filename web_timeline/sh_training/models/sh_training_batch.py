# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ShTrainingBatch(models.Model):
    _name = 'sh.training.batch'
    _description = 'Softhealer Training Batch'
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(required=True)
    stage = fields.Selection(selection=[(
        'new', 'New'), ('in_progress', 'In Progress'), ('done', 'Done'), ('cancel', 'Cancel')], default='new', tracking=True)
    sh_training_course_ids = fields.Many2many(
        comodel_name='sh.training.course', string='Training Course', tracking=True)
    sh_trainee_ids = fields.Many2many(
        comodel_name='res.users', string='Trainee', tracking=True)
    from_date = fields.Date(tracking=True)
    to_date = fields.Date(tracking=True)
    company_id = fields.Many2one('res.company', string='Company',
        default=lambda self: self.env.company, tracking=True)
    
    training_master_line = fields.One2many(
        comodel_name='sh.training.master',
        inverse_name='training_batch_id',
        string="Master Lines",
        auto_join=True)
    
    @api.onchange('sh_training_course_ids','sh_trainee_ids')
    def onchange_field(self):
        if self.training_master_line:
            self.action_generate_training_master()
    
    @api.onchange('training_master_line')
    def _onchange_training_master_line(self):
        count = 0
        for line in self.training_master_line:
            if not line.display_type:
                count += 1
                line.sr_no = count
    
    def action_generate_training_master(self):
        master_lines = []
        sr_no = 0
        for course_id in self.sh_training_course_ids:
            sr_no += 1
            vals = {
                'sr_no' : sr_no,
                'sh_course_id' : course_id.id,
            }
            if course_id.id not in self.training_master_line.mapped('sh_course_id').ids:
                master_lines.append((0,0,vals))

        self.write({'training_master_line' : master_lines})
        self._onchange_training_master_line()
    
    def write(self, vals):
        for rec in self:
            if vals.get('stage') == 'done':
                for line in rec.training_master_line:
                    if line.state != 'done':
                        raise UserError(_("All courses training must be completed/Done first."))
                
                group = self.env.ref('sh_training.group_manager')
                training_managers = self.env['res.users'].search([('groups_id', 'in', group.id)])
                if training_managers:
                    base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                    self.env['user.push.notification'].push_notification(
                        list_of_user_ids = training_managers,
                        title=f"Training : Completed",
                        message=f"Training Completed For Batch - {self.name}",
                        link=f'{base_url}/mail/view?model=sh.training.batch&_id={str(self.id)}',
                        res_model='sh.training.batch',
                        res_id=self.id,
                        type='hr')
                        
        return super(ShTrainingBatch, self).write(vals)