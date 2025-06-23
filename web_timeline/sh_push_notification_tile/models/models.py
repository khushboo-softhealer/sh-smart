from odoo import fields, models, api, _
from pyfcm import FCMNotification


class USerNotificationSubType(models.Model):
    _name = 'user.push.notification.sub.type'
    _description = "User Push Notification Sub Type"

    name = fields.Char("Subtype")


class USerNotification(models.Model):
    _name = 'user.push.notification'
    _description = "User Notification"
    _order = 'msg_read,id desc'
    
    active = fields.Boolean(default=True)
    user_id = fields.Many2one("res.users",string="User")
    name = fields.Char("Title")
    desc = fields.Text("Description")
    datetime = fields.Datetime("Time")
    res_model = fields.Char("Res Model")
    model_name = fields.Char("Model Name")
    res_id = fields.Integer("Res ID")
    msg_read = fields.Boolean("Read ?")
    type = fields.Selection([('sale','Sales'),('project','Project'),('support','Support'),('hr','Hr'),('assignment','Assignment')],string="Notification Type")
    subtype = fields.Many2one('user.push.notification.sub.type',string="Sub Type")


    def action_update_subtype(self):
        for rec in self:
            if rec.type == 'hr':
                if rec.name == 'Less Work Hours':
                    rec.write({'subtype':self.env.ref('sh_push_notification_tile.sh_less_work_hours').id})
                elif 'Modification Request' in rec.name:
                    rec.write({'subtype':self.env.ref('sh_push_notification_tile.sh_attendance_modification').id})
                elif 'Break Hour Extend' in rec.name:
                    rec.write({'subtype':self.env.ref('sh_push_notification_tile.sh_break_extend').id})
                elif 'Late Check in' in rec.name:
                    rec.write({'subtype':self.env.ref('sh_push_notification_tile.sh_late_coming').id})
                elif 'Early Check Out' in rec.name:
                    rec.write({'subtype':self.env.ref('sh_push_notification_tile.sh_early_going').id})





    def open_record(self):
        self.sudo().write({'msg_read':True})
        return {
                'name':self.name,
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': self.res_model,
                'res_id':self.res_id,
                'target': 'current',
            }

    def push_notification(self, list_of_user_ids, title, message, link, res_model, res_id, type):
        # super(WebPushNotification, self).push_notification(list_of_user_ids,title, message,link, res_model , res_id,type)
        for user in list_of_user_ids:
            type_dict = {'hr':user.employee_id.hr_notifications,
                         'project':user.employee_id.project_notifications,
                         'sale':user.employee_id.sales_notifications,
                         'assignment':user.employee_id.assignment_notifications,
                         'support':user.employee_id.support_notifications}
            if type_dict.get(type):

            #     if model.model == res_model:
            
                    self.env['bus.bus']._sendone(user.partner_id, 
                    'sh.push.notification', {})

                    self.env['user.push.notification'].sudo().create({
                    'user_id': user.id,
                    'name': title,
                    'desc': message,
                    'datetime': fields.Datetime.now(),
                    'res_model': res_model,
                    'model_name': res_model,
                    'res_id': res_id,
                    'msg_read': False,
                    'type': type,})

    def hr_push_notification(self, list_of_user_ids, title, message, link, res_model, res_id, type,subtype):
        # super(WebPushNotification, self).push_notification(list_of_user_ids,title, message,link, res_model , res_id,type)
        for user in list_of_user_ids:
            for model in user.notify_models.sudo():

                if model.model == res_model:

                    self.env['bus.bus']._sendone(user.partner_id, 
                    'sh.push.notification', {})

                    self.env['user.push.notification'].sudo().create({
                        'user_id': user.id,
                        'name': title,
                        'desc': message,
                        'datetime': fields.Datetime.now(),
                        'res_model': res_model,
                        'model_name': res_model,
                        'res_id': res_id,
                        'msg_read': False,
                        'type': type,
                        'subtype':subtype.id
                    })

    def high_five_realtime_update(self, user=''):
        self.env['bus.bus']._sendone(user.partner_id, 
        'new.high_five', {})
        
        
class res_users(models.Model):
    _inherit = "res.users"
    
    notify_models = fields.Many2many('ir.model',string="Notify Models")
    
    @api.model
    def systray_get_firebase_notifications(self):
        notifications = self.env['user.push.notification'].sudo().search([('user_id','=',self.env.uid)],limit=25, order='msg_read,id desc')
        unread_notifications = self.env['user.push.notification'].sudo().search([('user_id','=',self.env.uid),('msg_read','=',False)])
        data_notifications = []
        for notification in notifications:
            data_notifications.append({
                'id':notification.id,
                'desc':notification.desc,
                'name':notification.name,
                'user_id':notification.user_id,
                'datetime':notification.datetime,
                'uid':notification.user_id.id,
                'res_model':notification.res_model,
                'model_name':notification.model_name,
                'res_id':notification.res_id,
                'msg_read':notification.msg_read ,
                })
        
        return list(data_notifications), len(unread_notifications)

    @api.model
    def systray_get_firebase_all_notifications(self):
        notifications = self.env['user.push.notification'].search([('user_id','=',self.env.uid)],order='msg_read,id desc')
        unread_notifications = self.env['user.push.notification'].search([('user_id','=',self.env.uid),('msg_read','=',False)])
        data_notifications = []
        for notification in notifications:
            notification.sudo().write({
                'msg_read' : True
            })            
        
        return list(data_notifications), len(unread_notifications)

    @api.model
    def systray_get_firebase_notifications_type(self,kwargs):

        notifications = self.env['user.push.notification'].search([('user_id','=',self.env.uid),('type', '=', kwargs['type'])],order='msg_read,id desc',limit=70)
        unread_notifications = self.env['user.push.notification'].search([('user_id','=',self.env.uid),('msg_read','=',False)])
        data_notifications = []
        sale_type_noti_count = self.env['user.push.notification'].sudo().search_count([('type','=','sale'),('user_id','=',self.env.uid),('msg_read','=',False)],)
        project_type_noti_count = self.env['user.push.notification'].sudo().search_count([('type','=','project'),('user_id','=',self.env.uid),('msg_read','=',False)])
        support_type_noti_count = self.env['user.push.notification'].sudo().search_count([('type','=','support'),('user_id','=',self.env.uid),('msg_read','=',False)])
        hr_type_noti_count = self.env['user.push.notification'].sudo().search_count([('type','=','hr'),('user_id','=',self.env.uid),('msg_read','=',False)])
        assingment_noti_count = self.env['user.push.notification'].sudo().search_count([('type','=','assignment'),('user_id','=',self.env.uid),('msg_read','=',False)])

        for notification in notifications:
            data_notifications.append({
                'id':notification.id,
                'desc':notification.desc,
                'name':notification.name,
                'user_id':notification.user_id,
                'datetime':notification.datetime,
                'uid':notification.user_id.id,
                'res_model':notification.res_model,
                'model_name':notification.model_name,
                'res_id':notification.res_id,
                'msg_read':notification.msg_read ,
                })
        
        return list(data_notifications), len(unread_notifications) ,sale_type_noti_count , project_type_noti_count , support_type_noti_count , hr_type_noti_count, assingment_noti_count
