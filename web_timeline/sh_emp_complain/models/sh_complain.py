# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import api, fields, models

# Sh complain object


class ShComplain(models.Model):
    _name = 'sh.complain'
    _description = 'Complain'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Complain Sequence', readonly=True,
                       required=True, copy=False, default='New')
    subject = fields.Char(string="Subject")
    complain_category = fields.Many2one(
        'sh.complain.categories', string="Complain Category")
    create_date = fields.Date(required=True, default=lambda self: self._context.get(
        'Created On', fields.Date.context_today(self)))
    created_by = fields.Many2one(
        'res.users', default=lambda self: self.env.uid, string="Created By")
    resp_persons = fields.Many2many(
        'res.users', string="Responsible Persons", compute="_compute_responsible_per", store=True, domain=[('share', '=', False)])
    has_effect_on = fields.Many2many('sh.effect.model', string="Has Effect On")
    description = fields.Html('Description')
    state = fields.Selection([
        ('new', 'New'),
        ('waiting', 'Waiting For Approval'),
        ('resolve', 'Resolved'),
        ('refused', 'Refused'),
        ('closed', 'Closed')], string='State', readonly=True, index=True, copy=False, default='new',)
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.company)
    is_resolve = fields.Boolean(compute="_compute_resolve_buttont_check")
    resolved_by = fields.Many2one('res.users', string="Responsible Person ")
    refused_by = fields.Many2one('res.users', string="Responsible Person")
    refused_comment = fields.Text(string="Refused Comment")
    resolved_comment = fields.Text(string="Resolved Comment")
    rating = fields.Selection([
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ], string="Rating")
    is_editable = fields.Boolean(compute="_compute_is_editable") 
    is_category_editable = fields.Boolean(compute='_compute_is_category_editable')
    
    @api.depends('resp_persons')
    def _compute_is_editable(self):
        for rec in self:
            if rec.resp_persons and self.env.user.id in rec.resp_persons.ids:

                rec.is_editable = True
            else:   
                rec.is_editable = False
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sh.complain') or 'New'
                result = super(ShComplain, self).create(vals_list)
        return result

    @api.depends('complain_category')
    def _compute_responsible_per(self):
        for rec in self:
            rec.resp_persons = False
            if rec.complain_category:
                rec.resp_persons = [
                    (6, 0, rec.complain_category.responsible_persons.ids)]

    @api.depends('created_by')
    def _compute_resolve_buttont_check(self):
        self.is_resolve = False
        if self.created_by.id == self.env.user.id:
            self.is_resolve = True

    # complain form button actions
    def new_complain_button(self):
        self.write({'state': 'waiting'})
        template = self.env.ref(
            'sh_emp_complain.send_new_complain_notification_responsible_user')

        partner_to = ''
        total_receipients = len(self.resp_persons)
        count = 1
        if self.resp_persons:
            for resp in self.resp_persons:
                partner_to += str(resp.partner_id.id)
                if count < total_receipients:
                    partner_to += ','
                count += 1

        # template.partner_to = partner_to
        # template.send_mail(self.id, force_send=True,
        #                    email_layout_xmlid='mail.mail_notification_light')

        listt = []
        for user in self.resp_persons:
            listt.append(user)
        
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        self.env['user.push.notification'].push_notification(listt,'New Complain Created :','Complain ref %s'% (self.subject),base_url+"/mail/view?model=sh.complain&res_id="+str(self.id),'sh.complain', self.id,'hr')

    def resolve_button(self):
        self.write({'state': 'resolve'})
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        self.env['user.push.notification'].push_notification([self.created_by],'Your complain is resolved :','Complain ref %s'% (self.subject),base_url+"/mail/view?model=sh.complain&res_id="+str(self.id),'sh.complain', self.id,'hr')
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sh.complain.resolve.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {'current_id': self.id}
        }

    def refuse_button(self):
        self.write({'state': 'refused'})
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        self.env['user.push.notification'].push_notification([self.created_by],'Your complain is refused :','Complain ref %s'% (self.subject),base_url+"/mail/view?model=sh.complain&res_id="+str(self.id),'sh.complain', self.id,'hr')
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sh.complain.refuse.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {'current_id': self.id}
        }

    def close_button(self):
        self.write({'state': 'closed'})
        return {}

    def reset_to_draft_button(self):
        self.write({'state': 'new',
                    'refused_comment': '',
                    'refused_by': False,
                    'resolved_comment': '',
                    'resolved_by': False,
                    'rating': '0',
                    })
        return {}

    @api.depends('state','resp_persons')
    def _compute_is_category_editable(self):
        for rec in self:
            rec.is_category_editable = (
                rec.state not in ['resolve', 'closed'] and
                rec.env.user.id in rec.resp_persons.ids
            )

            if rec.state == 'new':
                rec.is_category_editable = True
