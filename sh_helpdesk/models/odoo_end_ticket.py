# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api
from odoo.tools import email_re, email_split, email_escape_char
import re

class OdooEndTicket(models.Model):
    _name = 'sh.odoo.end.ticket'
    _rec_name='email_subject'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _order = 'create_date DESC'
    _description = 'Odoo End Ticket'

    sh_user_ids = fields.Many2many('res.users',string='Assign Users',domain=[('share','=',False)],tracking=True)
    state = fields.Selection([('new','New'),('progress','In Progress'),('waiting','Waiting'),('done','Done'),('cancel','Cancelled')],default='new',string='Status',tracking=True)
    description = fields.Html('Description')
    email_subject = fields.Text('Email Subject')
    partner_id = fields.Many2one('res.partner',string="Partner")
    email = fields.Char('Email')
    sh_ticket_id = fields.Many2one('sh.helpdesk.ticket',string='Ticket')
    sh_ticket_created = fields.Boolean('Ticket Created')
    active = fields.Boolean(default=True,tracking=True)
    ticket_count = fields.Integer(compute='_compute_ticket_count')
    sh_store_link = fields.Char('Store URL',compute='_compute_store_link')
    sh_tech_name = fields.Char('Technical Name')
    sh_responsible_user_id = fields.Many2one('res.users',string='Responsible',domain=[('share','=',False)])

    @api.model_create_multi
    def create(self,vals):
        res = super(OdooEndTicket,self).create(vals)
        if res.description:
            description = str(res.description)
            regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
            url = re.findall(regex,description)
            if url:      
                store_url =  [x[0] for x in url]
                for x_url in store_url:
                    if 'https://apps.odoo.com' in x_url:
                        url_split = re.compile(r'[\:/?=\-&]+',re.UNICODE).split(x_url)
                        if url_split:
                            for tech_name in url_split:
                                if 'sh_' in tech_name:
                                    res.sh_tech_name = tech_name
                                    if tech_name:
                                        product_id = self.env['product.template'].sudo().search([('sh_technical_name','=',tech_name)],limit=1)
                                        if product_id:
                                            res.sh_responsible_user_id = product_id.resposible_user_id.id
                    elif 'https://apps.openerp.com' in x_url:
                        url_split = re.compile(r'[\:/?=\-&]+',re.UNICODE).split(x_url)
                        if url_split:
                            for tech_name in url_split:
                                if 'sh_' in tech_name:
                                    res.sh_tech_name = tech_name
                                    if tech_name:
                                        product_id = self.env['product.template'].sudo().search([('sh_technical_name','=',tech_name)],limit=1)
                                        if product_id:
                                            res.sh_responsible_user_id = product_id.resposible_user_id.id
        return res
    
    def _compute_store_link(self):
        for rec in self:
            rec.sh_tech_name = ''
            if rec.description:
                description = str(rec.description)
                regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
                url = re.findall(regex,description)
                if url: 
                    store_url =  [x[0] for x in url]
                    for x_url in store_url:
                        if 'https://apps.odoo.com' in x_url:
                            rec.sh_store_link = x_url
                        elif 'https://apps.openerp.com' in x_url:
                            rec.sh_store_link = x_url

    def action_assign_to_me(self):
        self.ensure_one()
        self.sh_user_ids = [(4, self.env.user.id)]

    def _compute_ticket_count(self):
        for rec in self:
            ticket_count = self.env['sh.helpdesk.ticket'].sudo().search([])
            count = 0
            if ticket_count:
                for ticket in ticket_count:
                    if rec.email_subject and ticket.store_reference and ticket.store_reference in rec.email_subject:
                        if 'SO' in rec.email_subject and 'SO' in ticket.store_reference:
                            count+=1
            rec.ticket_count = count

    def action_view_tickets(self):
        self.ensure_one()
        email_subject = self.email_subject
        email_subject = email_subject.split(" ")
        length = len(email_subject)
        email_subject_str = email_subject[length - 1]
        subject = ''
        if 'SO' in email_subject_str:
            subject = email_subject_str
        tickets = []
        ticket_count = self.env['sh.helpdesk.ticket'].sudo().search([])
        if ticket_count:
            for ticket in ticket_count:
                if ticket.store_reference and ticket.store_reference in self.email_subject:
                    tickets.append(ticket.id)
        return{
            'name':'Helpdesk Ticket',
            'res_model':'sh.helpdesk.ticket',
            'type':'ir.actions.act_window',
            'view_mode':'kanban,tree,form',
            'domain':[('id','in',tickets)],
            'context':{
                'default_sh_user_ids':[(6,0,self.sh_user_ids.ids or [])],
                'default_email_subject':self.email_subject,
                'default_odoo_store_ticket':True,
                'default_store_reference':subject,
                'default_sh_odoo_end_ticket_id':self.id,
            },
            'target':'current',
        }

    @api.model
    def message_new(self, msg_dict, custom_values=None):
        defaults={}
        email_from = msg_dict.get('from') or ''
        email_from = email_escape_char(email_split(email_from)[0])
        if email_from == 'apps@odoo.com':
            defaults.update({
                'email_subject':  msg_dict.get('subject') or _("No Subject"),
                'description': msg_dict.get('body'),
                })
            return super(OdooEndTicket, self).message_new(msg_dict, custom_values=defaults)
        return True
    
    def sh_create_ticket(self):
        self.ensure_one()
        email_subject = self.email_subject
        email_subject = email_subject.split(" ")
        length = len(email_subject)
        email_subject_str = email_subject[length - 1]
        subject = ''
        if 'SO' in email_subject_str:
            subject = email_subject_str 
        return{
            'name':'Helpdesk Ticket',
            'res_model':'sh.helpdesk.ticket',
            'type':'ir.actions.act_window',
            'view_mode':'form',
            'context':{
                'default_sh_user_ids':[(6,0,self.sh_user_ids.ids or [])],
                'default_email_subject':self.email_subject,
                'default_odoo_store_ticket':True,
                'default_store_reference':subject,
                'default_sh_odoo_end_ticket_id':self.id,
            },
            'target':'current',
        }

class OdooEndMassUpdate(models.TransientModel):
    _name = 'sh.odoo.end.mass.update'
    _description = 'Mass Update'

    state = fields.Selection([('new','New'),('progress','In Progress'),('waiting','Waiting'),('done','Done'),('cancel','Cancelled')],string='Status')
    
    def update_record(self):
        self.ensure_one()
        if self.env.context.get('active_ids'):
            for ticket in self.env[self.env.context.get('active_model')].sudo().browse(self.env.context.get('active_ids')):
                ticket.state = self.state 


    