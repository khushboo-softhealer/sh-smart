# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

import logging
from odoo import models,fields,api, tools
from odoo.tools import email_re

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    partner_website = fields.Char("Partner Website")
    sh_name_email_clean = fields.Boolean('Contact Name Cleaned?')
    sh_contact_type_changed = fields.Boolean('Contact Type Changed?')
    
    @api.model_create_multi
    def create(self, vals_list):
        res = super(ResPartner, self).create(vals_list)
        try:
            for vals in vals_list:
                if vals.get('email') and '@' in vals.get('email') and res.company_type == 'person':
                    partner_mail_value = email_re.findall(vals.get('email') or '')
                    if partner_mail_value:
                        new_mail = partner_mail_value[0]
                        partner_mail = new_mail.split('@')[1]
                        start_index =  new_mail.find("@") + 1
                        end_index = new_mail.rindex(".")
                        extracted_value = new_mail[start_index:end_index]
                        common_mail_domain_ids = self.env.company.sh_common_mail_domains_ids
                        common_mail_domain_names = common_mail_domain_ids.mapped('name')
                        res.partner_website = False
                        if partner_mail.lower() not in common_mail_domain_names:
                            res.partner_website = partner_mail.lower()
                            company_partner = self.env['res.partner'].sudo().search([('is_company','=',True),('partner_website','=',partner_mail.lower())], limit=1)
                            if company_partner:
                                    self.env.cr.execute("update res_partner set parent_id="+str(company_partner.sudo().id)+" where id="+str(res.id))
                                    self.env.cr.execute("update res_partner set type='delivery'"+" where id="+str(res.sudo().id))
                            else:
                                parent_id = self.env['res.partner'].sudo().create({
                                        'name':extracted_value,
                                        'is_company':True,
                                        'partner_website' : partner_mail.lower(),
                                    })
                                self.env.cr.execute("update res_partner set parent_id="+str(parent_id.sudo().id)+" where id="+str(res.sudo().id))
                                self.env.cr.execute("update res_partner set type='delivery'"+" where id="+str(res.sudo().id))
            return res
        except Exception as e:
            _logger.exception("partner company not created on ticket create: %s" % e)
             
            return res
        
    def write(self,vals):
        """This code write for when change Lead qualification page
        Updated_by(User) and updated_on(datetime) automatic added.
        """
        for rec in self:
            if vals.get('email') and '@' in vals.get('email') and rec.company_type == 'person':
                if not rec.parent_id:
                    partner_mail_value = email_re.findall(vals.get('email') or '')
                    if partner_mail_value:
                        new_mail = partner_mail_value[0]
                        partner_mail = new_mail.split('@')[1]
                        start_index =  new_mail.find("@") + 1
                        end_index = new_mail.rindex(".")
                        extracted_value = new_mail[start_index:end_index]
                        
                        common_mail_domain_ids = self.env.company.sh_common_mail_domains_ids
                        common_mail_domain_names = common_mail_domain_ids.mapped('name')
                        vals.update({
                            'partner_website':False
                        })
                        if partner_mail.lower() not in common_mail_domain_names:
                            rec.partner_website = partner_mail.lower()
                            
                            company_partner = self.env['res.partner'].sudo().search([('is_company','=',True),('partner_website','=',partner_mail.lower())], limit=1)
                            if company_partner:
                                    self.env.cr.execute("update res_partner set parent_id="+str(company_partner.sudo().id)+" where id="+str(rec.sudo().id))
                                    self.env.cr.execute("update res_partner set type='delivery'"+" where id="+str(rec.sudo().id))
                            else:
                                parent_id = self.env['res.partner'].sudo().create({
                                        'name':extracted_value,
                                        'is_company':True,
                                        'partner_website' : partner_mail.lower(),
                                    })
                                self.env.cr.execute("update res_partner set parent_id="+str(parent_id.sudo().id)+" where id="+str(rec.sudo().id))
                                self.env.cr.execute("update res_partner set type='delivery'"+" where id="+str(rec.sudo().id))
                # else:
                #     raise ValidationError("You can not change email")
                            
        return super(ResPartner, self).write(vals)
    
    def action_set_partner_email_domain(self):
        partner_active_ids = self.env['res.partner'].sudo().browse(self.env.context.get('active_ids'))
        for partner in partner_active_ids:
            if partner.email and '@' in partner.email:
                partner_mail_value = email_re.findall(partner.email or '')
                if partner_mail_value:
                    new_mail = partner_mail_value[0]
                    partner_mail = new_mail.split('@')[1]
                    start_index =  new_mail.find("@") + 1
                    end_index =  new_mail.rindex(".")
                    extracted_value = new_mail[start_index:end_index]
                    common_mail_domain_ids = self.env.company.sh_common_mail_domains_ids
                    common_mail_domain_names = common_mail_domain_ids.mapped('name')
                    partner.write({
                        'partner_website':False
                    })
                    if partner_mail.lower() not in common_mail_domain_names:
                        partner.write({
                            'partner_website':partner_mail.lower()
                        })
                
            
    def action_update_partner_parent(self):
        """ Mass action for update partner parent.
        """
        partner_active_ids = self.env['res.partner'].sudo().browse(self.env.context.get('active_ids'))
        
        
        for partner in partner_active_ids:
            if not partner.parent_id and not partner.is_company:
                if partner.email and '@' in partner.email:
                    partner_mail_value = email_re.findall(partner.email or '')
                    if partner_mail_value:
                        new_mail = partner_mail_value[0]
                        partner_mail = new_mail.split('@')[1]
                        start_index =  new_mail.find("@") + 1
                        end_index = new_mail.rindex(".")
                        extracted_value =new_mail[start_index:end_index]
                        common_mail_domain_ids = self.env.company.sh_common_mail_domains_ids
                        common_mail_domain_names = common_mail_domain_ids.mapped('name')
                        partner.write({
                            'partner_website':False,
                            'type':'delivery'
                        })
                        if partner_mail.lower() not in common_mail_domain_names:
                            partner.write({
                                'partner_website':partner_mail.lower(),
                                'type':'delivery'
                            })
                            
                            company_partner = self.env['res.partner'].search([('is_company','=',True),('partner_website','=',partner_mail.lower())] )
                            
                            if company_partner:
                                company_partner.write({
                                    'child_ids': [(4, partner.id)]
                                })
                            else:
                                self.env['res.partner'].create({
                                    'name':extracted_value,
                                    'child_ids':[(4,partner.id)],
                                    'is_company':True,
                                    'partner_website': partner_mail.lower(),                                    
                                })
            elif partner.parent_id and not partner.is_company:
                if partner.type == 'other':
                    partner.write({
                        'type':'delivery'
                    })


                
    def _compute_partner_ticket_count(self):
        for rec in self:
            rec.sh_partner_ticket_count = 0
            tickets = self.env['sh.helpdesk.ticket'].sudo().search(
                ['|','|',('partner_id', '=', rec.id),('partner_id','in',rec.child_ids.ids),('partner_id','in',rec.parent_id.child_ids.ids)])
            if tickets:
                rec.sh_partner_ticket_count = len(tickets.ids)

    def action_view_partner_ticket(self):
        self.ensure_one()
        tickets = self.env['sh.helpdesk.ticket'].sudo().search(
           ['|','|',('partner_id', '=', self.id),('partner_id','in',self.child_ids.ids),('partner_id','in',self.parent_id.child_ids.ids)])
        action = self.env.ref(
            "sh_helpdesk.helpdesk_ticket_action").read()[0]
        if len(tickets) > 1:
            action['domain'] = [('id', 'in', tickets.ids)]
        elif len(tickets) == 1:
            form_view = [
                (self.env.ref('sh_helpdesk.helpdesk_ticket_form_view').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + \
                    [(state, view)
                     for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = tickets.id
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
    
    

    def action_clear_partner_name(self):
        if self.env.context.get('active_ids'):
            partner_active_ids = self.env['res.partner'].sudo().browse(self.env.context.get('active_ids'))
            if partner_active_ids:
                for partner in partner_active_ids:
                    partner_name_split = tools.email_split_tuples(partner.name)
                    if partner_name_split:
                        for (partner_name, partner_email) in partner_name_split:
                            if '"' in partner_name:
                                new_name = partner_name.replace('"','')
                                partner.name = new_name
                            else:
                                partner.name = partner_name
                    else:
                        if '"' in partner.name:
                            partner.name = partner.name.replace('"','')
                    email_name_split = tools.email_split_tuples(partner.email)
                    if email_name_split:
                        for (name, email) in email_name_split:
                            partner.email = email
                    if partner.name == ' ' or not partner.name:
                        partner.name = partner.email

    @api.model
    def _run_clean_contact_name_email(self):
        partner_ids = self.env['res.partner'].sudo().search([('parent_id','!=',False),('is_company','=',False),('sh_name_email_clean','=',False)],limit=100)
        if partner_ids:
            for partner in partner_ids:
                partner_name_split = tools.email_split_tuples(partner.name)
                if partner_name_split:
                    for (partner_name, partner_email) in partner_name_split:
                        if '"' in partner_name:
                            new_name = partner_name.replace('"','')
                            partner.name = new_name
                        else:
                            partner.name = partner_name
                else:
                    if '"' in partner.name:
                        partner.name = partner.name.replace('"','')
                email_name_split = tools.email_split_tuples(partner.email)
                if email_name_split:
                    for (name, email) in email_name_split:
                        partner.email = email
                if partner.name == ' ' or not partner.name:
                    partner.name = partner.email
                partner.sh_name_email_clean = True

    @api.model
    def _run_update_contact_type_as_other(self):
        partner_ids = self.env['res.partner'].sudo().search([('parent_id','!=',False),('is_company','=',False),('sh_contact_type_changed','=',False),('type','in',['other'])],limit=100)
        if partner_ids:
            for partner in partner_ids:
                partner.type = 'delivery'
                partner.sh_contact_type_changed = True
