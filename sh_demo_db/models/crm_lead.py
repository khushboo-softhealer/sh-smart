# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def action_demo_ticket(self):
        self.ensure_one()
        ticket_vals = {}
        partner_id = False
        if self.partner_id:
            partner_id = self.partner_id
        else:
            if self.email_from:
                search_partner_id = self.env['res.partner'].sudo().search([('email','=',self.email_from)],limit=1)
                if partner_id:
                    partner_id = search_partner_id
                else:
                    partner_vals = {'type':'contact','customer':True,'company_type': 'person','email':self.email_from}
                    if self.contact_name:
                        partner_vals.update({
                            'name': self.contact_name,
                        })
                    else:
                        partner_vals.update({'name':self.email_from})
                    if self.function:
                        partner_vals.update({
                            'function':self.function
                        })
                    if self.phone:
                        partner_vals.update({
                            'phone':self.phone
                        })
                    if self.mobile:
                        partner_vals.update({
                            'mobile':self.mobile
                        })
                    if self.street:
                        partner_vals.update({
                            'street':self.street
                        })
                    if self.street2:
                        partner_vals.update({
                            'street2':self.street2
                        })
                    if self.city:
                        partner_vals.update({
                            'city':self.city
                        })
                    if self.state_id:
                        partner_vals.update({
                            'state_id':self.state_id.id
                        })
                    if self.country_id:
                        partner_vals.update({
                            'country_id':self.country_id.id
                        })
                    if self.zip:
                        partner_vals.update({
                            'zip':self.zip
                        })
                    if self.website:
                        partner_vals.update({
                            'website':self.website,
                        })
                    if partner_vals:
                        partner_id = self.env['res.partner'].sudo().create(partner_vals)
                        self.partner_id = partner_id.id
        if partner_id:
            ticket_vals.update({
                'partner_id':partner_id.id,
                'partner_ids':[(6,0,self.partner_id.ids)],
                'sh_lead_ids':[(6,0,self.ids)],
                'ticket_type':self.env.user.company_id.sh_demo_type_id.id,
                'stage_id':self.env.user.company_id.sh_demo_stage_id.id or self.env.ref('sh_demo_db.demo_request').id
            })    
            if self.description:
                ticket_vals.update({
                    'description':self.description
                })
            # if self.message_partner_ids:
            #     ticket_vals.update({
            #         'message_partner_ids':[(6,0,self.message_partner_ids.ids)]
            #     })
            if self.name:
                ticket_vals.update({
                    'email_subject':self.name
                })
            if ticket_vals:
                ticket_id = self.env['sh.helpdesk.ticket'].sudo().create(ticket_vals)
                if ticket_id:
                    if self.company_id and self.company_id.sh_close_crm_stage_id:
                        self.stage_id = self.company_id.sh_close_crm_stage_id.id
                    lead_attachment_ids = self.env['ir.attachment'].sudo().search([('res_model','=','crm.lead'),('res_id','=',self.id)])
                    if lead_attachment_ids:
                        for attachment in lead_attachment_ids:
                            attachment = self.env['ir.attachment'].create({
                                'name'   : attachment.name,
                                'type' : attachment.type,
                                'datas':  attachment.datas,
                                # 'datas_fname' : attachment.datas_fname ,
                                'res_model' :  'sh.helpdesk.ticket',
                                'res_id' :  ticket_id.id,
                                'mimetype' :  attachment.mimetype
                            })
                    self.type = 'opportunity'
                    ticket_id.onchange_partner_id()
                    return{
                        'name': 'Helpdesk Ticket',
                        'type': 'ir.actions.act_window',
                        'res_model': 'sh.helpdesk.ticket',
                        'view_mode': 'form',
                        'res_id':ticket_id.id,
                        'target': 'current'
                    }