# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models, api, _
# from pyfcm import FCMNotification

class BrEngagePushNotification(models.Model):
    _name = 'sh.br.engage.push.notification'
    _description = "User Push Notification"
    _order = 'msg_read,id desc'
    
    user_id = fields.Many2one("res.users",string="User")
    name = fields.Char("Title")
    description = fields.Text("Description")
    datetime = fields.Datetime("Time")
    res_model = fields.Char("Res Model")
    res_id = fields.Integer("Res ID")
    msg_read = fields.Boolean("Read ?")


    def open_record(self):
        self.write({'msg_read':True})
        if self.res_model:
            return {
                'name':self.name,
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': self.res_model,
                'res_id':self.res_id,
                'target': 'current',
            }

    def create_br_engage_push_notification(self,user='',name='',description='',res_model='',res_id=''):
        # if self.env.company.enable_bell_notification:
        self.env['bus.bus']._sendone(user.partner_id, 
        'sh.br.engage.push.notification', {})
        self.env['sh.br.engage.push.notification'].sudo().create({
            'user_id': user.id,
            'name':name,
            'description':description,
            'datetime':fields.Datetime.now(),
            'res_model':res_model,
            'res_id':res_id,
            'msg_read':False,
        })

    def realtime_update_method_for_feedback(self, user=''):
        self.env['bus.bus']._sendone(user.partner_id, 
        'new.feedback', {})


    def high_five_realtime_update(self, user=''):
        self.env['bus.bus']._sendone(user.partner_id, 
        'new.high_five', {})

