# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields, api, _
from datetime import timedelta

class ShTrainingMaster(models.Model):
    _name = 'sh.training.master'
    _description = 'Softhealer Training Master'
    _rec_name = 'sh_course_id'

    name = fields.Text("Note")
    sequence = fields.Integer(string="Sequence", default=10)
    sr_no = fields.Integer()
    sh_course_id = fields.Many2one(
        comodel_name='sh.training.course', string='Course')
    state = fields.Selection(selection=[('in_progress', 'In Progress'), 
                                        ('done', 'Done')])
    responsible_user_ids = fields.Many2many(related='sh_course_id.responsible_user_ids', string='Responsible', domain=[('share', '=', False)])
    start_date = fields.Date()
    end_date = fields.Date()
    deadline = fields.Date()
    approx_days = fields.Integer()
    company_id = fields.Many2one('res.company', string='Company',default=lambda self: self.env.company)
    
    training_batch_id = fields.Many2one(
        comodel_name='sh.training.batch', string="Batch Reference", 
        ondelete='cascade', index=True, copy=False)
    sh_trainee_ids = fields.Many2many(related='training_batch_id.sh_trainee_ids')
    sh_training_course_ids = fields.Many2many(related='training_batch_id.sh_training_course_ids')
    
    display_type = fields.Selection(
        selection=[
            ('line_section', "Section"),
            ('line_note', "Note"),
        ],
        default=False)
    
    trainee_ratings_line = fields.One2many(
        comodel_name='sh.trainee.ratings',
        inverse_name='training_master_id',
        string="Rating Lines",
        auto_join=True)

    
    @api.model_create_multi
    def create(self, vals_list):
        res = super(ShTrainingMaster, self).create(vals_list)
        for rec in res:
            if not rec.display_type:
                for trainee_id in rec.training_batch_id.sh_trainee_ids:
                    if trainee_id.id not in rec.trainee_ratings_line.mapped('sh_trainee_id').ids:
                        self.env['sh.trainee.ratings'].create({
                            'training_master_id' : rec.id,
                            'sh_trainee_id' : trainee_id.id,
                        })
        return res

    def action_open_trainee_ratings(self):
        view_id = self.env.ref('sh_training.sh_training_master_view_form').id
        return {
            'name': _('Trainee Ratings'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'sh.training.master',
            'view_id': view_id,
            'views': [[view_id, 'form']],
            'res_id': self.id,
            'target': 'new',
        }
    
    def _notify_responsible_for_missed_course_deadline(self):
        today = fields.Date.today()
        incomplete_training_master_ids = self.env['sh.training.master'].sudo().search([('state','!=','done')])
        
        for line in incomplete_training_master_ids:
            if line.deadline:
                next_day_of_deadline = line.deadline + timedelta(days=1)
                if next_day_of_deadline == today:
                    base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                    self.env['user.push.notification'].push_notification(
                        list_of_user_ids = line.responsible_user_ids,
                        title="Training : Deadline Missed",
                        message=f"Deadline Missed For Course {line.sh_course_id.name} of Training Batch {line.training_batch_id.name}",
                         link=f'{base_url}/mail/view?model=sh.training.batch&_id={str(line.training_batch_id.id)}',
                        res_model='sh.training.batch',
                        res_id=line.training_batch_id.id,
                        type='hr')


class ShTraineeRatings(models.Model):
    _name = 'sh.trainee.ratings'
    _description = 'Softhealer Trainee Ratings'
    _rec_name = 'sh_trainee_id'

    training_master_id = fields.Many2one(
        comodel_name='sh.training.master', string="Master Reference", 
        ondelete='cascade', index=True, copy=False)
    
    sh_trainee_ids = fields.Many2many(related='training_master_id.sh_trainee_ids')
    sh_trainee_id = fields.Many2one(comodel_name='res.users', string='Trainee', domain=[('share', '=', False)])
    ratings = fields.Selection([('0', '0'),('1', '1'),('2', '2'),('3', '3'),('4', '4'),('5', '5')])
    note = fields.Text('Remarks')