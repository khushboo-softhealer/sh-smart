# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

import logging
from odoo.exceptions import UserError
from odoo import models, fields, api
_logger = logging.getLogger(__name__)
from markupsafe import Markup

class HelpdeskTicketCustomisation(models.Model):
    _inherit = 'sh.helpdesk.ticket'
    
    sh_email_from = fields.Char(string='Email From')
    sh_ticket_type_ids = fields.Many2many('sh.helpdesk.ticket.type','sh_ticket_type_helpdesk_ticket_rel','ticket_type_id','ticket_id',string="Ticket Types")
    
    def common_action_manual_update_tracking_manytwomany_field(self,vals):
        try:
            certain_fields = ['sh_user_ids']
            available_fields = [field for field in certain_fields if field in vals]
            
            if available_fields:
                for field in available_fields:
                    field_record = self.env['ir.model.fields'].sudo().search([('name','=',field),('model','=',self._name)])
                    if field_record:
                        new_records = ''
                        if field  == 'sh_user_ids':
                            if len(vals.get(field)) == 1:
                                new_records = self.env[field_record.relation].sudo().browse(vals.get(field)[0][2]).mapped('name')
                            elif len(vals.get(field)) > 1:
                                new_records = self.env[field_record.relation].sudo().browse([t[1] for t in vals.get(field)]).mapped('name')
                            old_records = getattr(self, field).mapped('name')
                            body = Markup('''<b>%s</b>
                                <ul class="o_Message_trackingValues mb-0 ps-4">
                                <li>
                                    <div class="o_TrackingValue d-flex align-items-center flex-wrap mb-1" role="group">
                                        <span class="o_TrackingValue_oldValue me-1 px-1 text-muted fw-bold">%s</span>
                                        <i class="o_TrackingValue_separator fa fa-long-arrow-right mx-1 text-600" title="Changed" role="img"
                                            aria-label="Changed"></i>
                                        <span class="o_TrackingValue_newValue me-1 fw-bold text-info">%s</span>
                                        <span class="o_TrackingValue_fieldName ms-1 fst-italic text-muted">(by %s)</span>
                                    </div>
                                </ul>''' % (field_record.field_description,', '.join(old_records) if old_records else 'None', ', '.join(new_records) if new_records else 'None', self.env.user.name))

                            message = self.env['mail.message'].sudo().create(
                            {
                                'message_type': 'comment',
                                'subtype_id': self.env.ref('mail.mt_note').id,
                                'model': 'sh.helpdesk.ticket',
                                'res_id': self.id,
                                'record_name': self.name,
                                'body': body
                            }
                        )
        except Exception as e:
            _logger.info("#001 converting log note fot M2M field in Contact: %s" % e)

    @api.model_create_multi
    def create(self, values):
        for vals in values:
            fetchmail_server_id = self.env.context.get('default_fetchmail_server_id')
            if fetchmail_server_id:
                fetchmail_server_record = self.env['fetchmail.server'].browse(fetchmail_server_id)
                vals['sh_email_from'] = fetchmail_server_record.user
        return super(HelpdeskTicketCustomisation, self).create(values)

    def write(self,vals):
        
        for rec in self:
            
            if 'sh_user_ids' in vals:
                rec.common_action_manual_update_tracking_manytwomany_field(vals)
            if vals.get('stage_id'):
                users = []
                old_users = []
                if rec.sh_user_ids:
                    old_users = rec.sh_user_ids.ids
                
                stage_record = self.env['sh.helpdesk.stages'].browse(vals.get('stage_id'))
                if stage_record.sh_res_users_ids:
                    users = stage_record.sh_res_users_ids.ids
                if stage_record.sh_helpdesk_ticket_type_id:
                    vals.update({
                        'ticket_type':stage_record.sh_helpdesk_ticket_type_id.id,
                        'sh_ticket_type_ids':[(4,stage_record.sh_helpdesk_ticket_type_id.id)]
                    })
                    # self.env.cr.execute("update sh_helpdesk_ticket set ticket_type="+str(stage_record.sh_helpdesk_ticket_type_id.id)+" where id="+str(rec.id))
                if stage_record.sh_remove_responsible_user:
                    if old_users:
                        final_users = [x for x in old_users if x not in users]
                        if final_users:
                            delete_query = """delete from res_users_sh_helpdesk_ticket_rel where sh_helpdesk_ticket_id in %s and res_users_id in %s"""
                            self.env.cr.execute(delete_query,(tuple([rec.id]),tuple(final_users),))
                if users:
                    vals.update({'sh_user_ids': [(4, user) for user in users],}) 
                
                    # for user in users:
                    #     select_query = """select * from res_users_sh_helpdesk_ticket_rel where sh_helpdesk_ticket_id in %s and res_users_id in %s"""
                    #     self.env.cr.execute(select_query,(tuple([rec.id]),tuple([user]),))
                    #     data = self._cr.dictfetchall()
                    #     if not data:
                    #         user_columns = ['sh_helpdesk_ticket_id','res_users_id']
                    #         user_values = [str(rec.id),str(user)]
                    #         insert_query = 'insert into res_users_sh_helpdesk_ticket_rel(' + ','.join(user_columns)+')'+'values' + \
                    #                 str(tuple(user_values))
                    #         self.env.cr.execute(insert_query)
                    #         base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                    #         product_name = ''
                    #         if record.product_ids:
                    #             product_name = ' (' + str(record.product_ids[0].sh_technical_name)+')'
                    #         self.env['user.push.notification'].push_notification(list(set(self.env['res.users'].sudo().browse(user))), 'Ticket Assigned', 'Ticket Ref %s:' % (
                    #             record.name+product_name), base_url+"/mail/view?model=helpdesk.ticket&res_id="+str(record.id), 'sh.helpdesk.ticket', record.id,'support')
        return super(HelpdeskTicketCustomisation, self).write(vals)

    # def write(self, vals):
    #     try:
    #         current_values = []
            
    #         for record in self:
    #             current_values = record.sh_user_ids.ids
    #             # if 'sh_user_ids' in vals and self.env.user.id != 1 and self.env.user.has_group('base.group_user') and not self.env.context.get('default_fetchmail_server_id'):
    #             #     record.common_action_manual_update_tracking_manytwomany_field(vals)
            
    #         res = super(HelpdeskTicketCustomisation, self).write(vals)
    #         for rec in self:
    #             if vals.get('stage_id'):
    #                 stage_record = self.env['sh.helpdesk.stages'].browse(vals.get('stage_id'))
    #                 users = stage_record.sh_res_users_ids.ids
                    
    #                 if stage_record.sh_remove_responsible_user:
    #                     # delete_query = """delete from res_users_sh_helpdesk_ticket_rel where sh_helpdesk_ticket_id in %s and res_users_id in %s"""
    #                     # self.env.cr.execute(delete_query,(tuple([rec.id]),tuple(current_values),))
    #                     rec.update({'sh_user_ids': [(3, u_id) for u_id in current_values]}) 
    #                     if users:
    #                         # user_columns = ['sh_helpdesk_ticket_id','res_users_id']
    #                         # for user in users:
    #                         #     user_values = [str(rec.id),str(user)]
    #                         #     insert_query = 'insert into res_users_sh_helpdesk_ticket_rel(' + ','.join(user_columns)+')'+'values' + \
    #                         #             str(tuple(user_values))
    #                         #     self.env.cr.execute(insert_query)
    #                         rec.update({
    #                             'sh_user_ids': [(4, user) for user in users],
    #                         }) 
    #                     if stage_record.sh_helpdesk_ticket_type_id:
    #                         # self.env.cr.execute("update sh_helpdesk_ticket set ticket_type="+str(stage_record.sh_helpdesk_ticket_type_id.id)+" where id="+str(rec.id))
    #                         rec.update({
    #                             'ticket_type':stage_record.sh_helpdesk_ticket_type_id.id
    #                         }) 
    #                 else:
    #                     if users:
    #                         # user_columns = ['sh_helpdesk_ticket_id','res_users_id']
    #                         # for user in users:
    #                         #     user_values = [str(rec.id),str(user)]
    #                         #     insert_query = 'insert into res_users_sh_helpdesk_ticket_rel(' + ','.join(user_columns)+')'+'values' + \
    #                         #             str(tuple(user_values))
    #                         #     self.env.cr.execute(insert_query)
    #                         rec.update({
    #                             'sh_user_ids': [(4, user) for user in users],
    #                         }) 
    #                     if stage_record.sh_helpdesk_ticket_type_id:
    #                         # self.env.cr.execute("update sh_helpdesk_ticket set ticket_type="+str(stage_record.sh_helpdesk_ticket_type_id.id)+" where id="+str(rec.id))
    #                         rec.update({
    #                             'ticket_type':stage_record.sh_helpdesk_ticket_type_id.id
    #                         })
    #         return res
    #     except Exception as e:
    #             _logger.exception("Responsible Users not update on write: %s" % e)
    #             return super(HelpdeskTicketCustomisation, self).write(vals)

    def action_add_responsible_users(self):
        try:
            product_responsible_user = []
            if self.product_ids:
                for product in self.product_ids:
                    if product.git_repo and product.git_repo.responsible_user:
                        product_responsible_user.append(product.git_repo.responsible_user.id)
                    
                    if product.git_repo and product.git_repo.other_responsible_user_ids:
                        for other_users in product.git_repo.other_responsible_user_ids:
                            product_responsible_user.append(other_users.id)
                            
            if product_responsible_user:
                self.sh_user_ids = [(4, user) for user in product_responsible_user]
            
        except Exception as e:
             _logger.exception("Responsible User not added on button click: %s" % e)
                
    def action_add_users_to_task(self):
        self.ensure_one()
        return{
            'name': "Add/Remove Users",
            'res_model': 'sh.add.user.to.task',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'target': 'new',
        }

    def action_update_edition_detalis_in_ticket(self):
        try:
            edition_id = self.env['sh.edition'].search([('name','=','Enterprise')])
            if edition_id:
                hosted_id = self.env['sh.odoo.hosted.on'].search([('name','ilike','odoo.sh'),('sh_edtion_id','=',edition_id.id)])
            else:
                hosted_id = False
                
            for rec in self:
                if rec.sh_edition_id.name == 'Odoo.sh': 
                    rec.write({
                        'sh_edition_id':edition_id.id,
                        'sh_odoo_hosted_id':hosted_id.id
                    })
        except Exception as e:
            _logger.exception("When Update Edition and Hosted on field using mass Action Button: %s" % e)