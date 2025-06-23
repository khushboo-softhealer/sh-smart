# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields, api, _

class CronJob(models.Model):

    _name = 'ir.cron'
    _inherit = ['ir.cron', 'mail.thread','mail.activity.mixin']
    
    res_model_id = fields.Integer('Res Model ')
    # temp
    res_model = fields.Integer()

    # @api.multi
    # @api.model
    # def method_direct_trigger(self):
    #     try:
    #         super(CronJob,self).method_direct_trigger()
    #     except Exception as e:

    #         activity_type = self.env['mail.activity.type'].search(
    #         [('name', '=', 'Exception')], limit=1)

    #         self.act1 = self.env['mail.activity'].create({
    #             'activity_type_id': activity_type.id,
    #             'res_id': self.id,
    #             'res_model_id': self.env['ir.model']._get('ir.cron').id,
    #             # temp
    #             'res_model': self.env['ir.model']._get('ir.cron').id,
    #             'user_id': self.user_id.id,
    #             'date_deadline': fields.date.today(),
    #             'summary': 'Schedular Fail',
    #             'note' : e
    #         })
