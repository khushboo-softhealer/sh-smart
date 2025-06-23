# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class HelpdeskTicketCrm(models.Model):
    _inherit = 'sh.helpdesk.ticket'

    sh_lead_ids = fields.Many2many("crm.lead", string="Leads/Opportunities")
    lead_count = fields.Integer(
        'Lead', compute='_compute_lead_count_helpdesk')
    opportunity_count = fields.Integer(
        'Opportunity', compute='_compute_opportunity_count_helpdesk')

    def action_create_lead(self):
        context = {'default_type': 'lead'}
        if self.partner_id:
            context.update({
                'default_partner_id': self.partner_id.id,
            })
        if self.user_id:
            context.update({
                'default_user_id': self.user_id.id,
            })
        if self:
            context.update({
                'default_sh_ticket_ids': [(6, 0, self.ids)],
            })
        return{
            'name': 'Lead',
            'type': 'ir.actions.act_window',
            'res_model': 'crm.lead',
            'view_mode': 'form',
            'context': context,
            'target': 'current'
        }

    def action_create_opportunity(self):
        context = {'default_type': 'opportunity'}
        if self.partner_id:
            context.update({
                'default_partner_id': self.partner_id.id,
            })
        if self.user_id:
            context.update({
                'default_user_id': self.user_id.id,
            })
        if self:
            context.update({
                'default_sh_ticket_ids': [(6, 0, self.ids)],
            })
        return{
            'name': 'Opportunity',
            'type': 'ir.actions.act_window',
            'res_model': 'crm.lead',
            'view_mode': 'form',
            'context': context,
            'target': 'current'
        }

    def _compute_lead_count_helpdesk(self):
        for record in self:
            record.lead_count = 0
            leads = self.env['crm.lead'].search(
                [('id', 'in', record.sh_lead_ids.ids), '|', ('type', '=', 'lead'), ('type', '=', False)], limit=None)
            if leads:
                record.lead_count = len(leads.ids)

    def _compute_opportunity_count_helpdesk(self):
        for record in self:
            record.opportunity_count = 0
            opporunities = self.env['crm.lead'].search(
                [('id', 'in', record.sh_lead_ids.ids), ('type', '=', 'opportunity')], limit=None)
            if opporunities:
                record.opportunity_count = len(opporunities.ids)

    def lead_counts(self):
        self.ensure_one()
        leads = self.env['crm.lead'].sudo().search(
            [('id', 'in', self.sh_lead_ids.ids), '|', ('type', '=', 'lead'), ('type', '=', False)])
        action = self.env.ref(
            "crm.crm_lead_all_leads").read()[0]
        if len(leads) > 1:
            action['domain'] = [('id', 'in', leads.ids), '|',
                                ('type', '=', 'lead'), ('type', '=', False)]
        elif len(leads) == 1:
            form_view = [
                (self.env.ref('crm.crm_lead_view_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + \
                    [(state, view)
                     for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = leads.id
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    def opportunity_counts(self):
        self.ensure_one()
        opportunities = self.env['crm.lead'].sudo().search(
            [('id', 'in', self.sh_lead_ids.ids), ('type', '=', 'opportunity')])
        action = self.env.ref(
            "crm.crm_lead_action_pipeline").read()[0]
        if len(opportunities) > 1:
            action['domain'] = [('id', 'in', opportunities.ids),
                                ('type', '=', 'opportunity')]
        elif len(opportunities) == 1:
            form_view = [
                (self.env.ref('crm.crm_lead_view_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + \
                    [(state, view)
                     for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = opportunities.id
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
    
    @api.model_create_multi
    def create(self,vals_list):
        for vals in vals_list:
            
            if not vals.get('partner_id') and self.env.context.get('to_be_ignored'):                                               
                blank_helpdesk_records = self.env['sh.helpdesk.ticket'].browse() 
                return blank_helpdesk_records

        res = super(HelpdeskTicketCrm,self).create(vals_list)
        for vals in vals_list:
            if res.sh_lead_ids:
                ticket_message_ids = []
                for lead in res.sh_lead_ids:
                    if lead.message_ids:
                        message_ids = self.env['mail.message'].sudo().search([('id','in',lead.message_ids.ids)],order='id asc')
                        for msg in message_ids:
                            message_vals = {
                                'subject':msg.subject,
                                'date':msg.date,
                                'email_from':msg.email_from,
                                'author_id':msg.author_id.id,
                                'record_name':msg.record_name,
                                # 'moderator_id':msg.moderator_id.id,
                                'parent_id':msg.parent_id.id,
                                'model':'sh.helpdesk.ticket',
                                'res_id':res.id,
                                'message_type':msg.message_type,
                                'subtype_id':msg.subtype_id.id,
                                'body':msg.body,
                            }
                            ticket_message_ids.append((0,0,message_vals))
                    lead_attachment_ids = self.env['ir.attachment'].sudo().search([('res_model','=','crm.lead'),('res_id','=',lead.id)])
                    if lead_attachment_ids:
                        for attachment in lead_attachment_ids:
                            attachment = self.env['ir.attachment'].create({
                                'name'   : attachment.name,
                                'type' : attachment.type,
                                'datas':  attachment.datas,
                                # 'datas_fname' : attachment.datas_fname ,
                                'res_model' :  'sh.helpdesk.ticket',
                                'res_id' :  res.id,
                                'public' :  True,
                                'mimetype' :  attachment.mimetype
                            })
                res.message_ids = ticket_message_ids
        return res
