# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from datetime import datetime, timedelta
import xmlrpc.client
import json
from odoo.http import request
from odoo import models, fields, api
import random
import time
import requests
import logging
_logger = logging.getLogger(__name__)


class DemoDbLog(models.Model):
    _name = 'sh.demo.db.log'
    _rec_name = 'sh_database_name'
    _description = " Demo DB Log"

    sh_database_name = fields.Char(string='Database Name')
    sh_username = fields.Char(string='Username')
    sh_password = fields.Char(string='Password')
    sh_url = fields.Char(string='Demo Server', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    db_create_date = fields.Datetime(string='Create Date')
    log_message = fields.Char('Log Message')
    ticket_id = fields.Many2one('sh.helpdesk.ticket', string='Demo DB Ticket')
    sh_db_ids = fields.Many2many('product.template', string="Modules")
    create_date = fields.Datetime(string='Create Date')

    def action_drop_db(self):
        get_url_split = list(self.sh_url.split("/"))
        get_url = 'http://' + get_url_split[2]
        url_for_drop_db = get_url + '/web/database/drop'
        data = {'master_pwd': self.sh_server_id.sh_master_password,
                'name': self.sh_database_name}
        result = requests.post(url=url_for_drop_db, data=data)


class HelpdeskTicket(models.Model):
    _inherit = 'sh.helpdesk.ticket'

    sh_demo_password = fields.Char('Password')
    sh_demo_db_create_date = fields.Datetime(
        'Demo DB Create Date', readonly=True)
    sh_demo_db_expired_date = fields.Datetime('Demo DB Expired Date')
    sh_demo_db_url = fields.Char('Demo Db Url')
    sh_demo_db_name = fields.Char('Demo db')
    sh_db_log_ids = fields.One2many(
        'sh.demo.db.log', 'ticket_id', string='Demo DB Log')
    sh_demo_content = fields.Html('Demo Email Content')
    sh_demo_ticket = fields.Boolean('Demo Ticket ?')
    sh_drop_db = fields.Boolean('Drop Demo DB')

    def sh_password_generate(self):
        lower_alphabet = "abcdefghijklmnopqrstuvwxyz"
        upper_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        digit = "1234567890"
        symbol = r"!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
        password = ""
        random.seed()
        COMBINED_LIST = lower_alphabet + upper_alphabet + digit + symbol
        for i in range(0, 9):
            next_index = random.randrange(len(COMBINED_LIST))
            password = password + COMBINED_LIST[next_index]
        return password

    @api.model_create_multi
    def create(self, vals_list):
        res = super(HelpdeskTicket, self).create(vals_list)
        for vals in vals_list:
            company_id = self.env.user.company_id
            if company_id:
                if company_id.new_stage_id:
                    if company_id.sh_demo_type_id.id == vals.get('ticket_type'):
                        res.stage_id = company_id.sh_demo_stage_id.id or self.env.ref(
                            'sh_demo_db.demo_request').id
                        if company_id.sh_demo_db_user_ids:
                            for user in company_id.sh_demo_db_user_ids:
                                res.sh_user_ids = [(4, user.id)]
                        res.sh_demo_ticket = True
                    else:
                        res.stage_id = company_id.new_stage_id.id
        return res

    def write(self, vals):
        # if vals.get('stage_id') and self.env.user.company_id.sh_demo_stage_id.id == vals.get('stage_id'):
        #     if self.env.user.company_id.sh_demo_db_user_ids:
                
        #         for user in self.env.user.company_id.sh_demo_db_user_ids:
        #             vals.update({
        #                 'sh_user_ids': [(4, user.id)]
        #             })
        if self.env.user.company_id.sh_demo_type_id.id == vals.get('ticket_type'):
            vals.update({
                'stage_id': self.env.user.company_id.sh_demo_stage_id.id or self.env.ref('sh_demo_db.demo_request').id,
                'sh_demo_ticket': True
            })
        return super(HelpdeskTicket, self).write(vals)

    def action_approve(self):
        if self.ticket_type.id == self.env.user.company_id.sh_demo_type_id.id and self.stage_id and self.stage_id.id == self.env.user.company_id.sh_demo_stage_id.id:
            if self.sh_version_id and self.sh_edition_id:
                demo_server_id = self.env['sh.servers'].sudo().search(
                    [('sh_version_id', '=', self.sh_version_id.id), ('sh_edition_id', '=', self.sh_edition_id.id)], limit=1)

                if demo_server_id:
                    demo_db_name = 'demo'
                    new_db_name = str(int(time.time()))
                    if self.sh_version_id.name == 'Odoo 15' and self.sh_edition_id.name == 'Community':
                        demo_db_name = demo_db_name + '_' + 'v15'+'_'+'com'
                    elif self.sh_version_id.name == 'Odoo 15' and self.sh_edition_id.name == 'Enterprise':
                        demo_db_name = demo_db_name + '_' + 'v15'+'_'+'ent'
                    if self.sh_version_id.name == 'Odoo 14' and self.sh_edition_id.name == 'Community':
                        demo_db_name = demo_db_name + '_' + 'v14'+'_'+'com'
                    elif self.sh_version_id.name == 'Odoo 14' and self.sh_edition_id.name == 'Enterprise':
                        demo_db_name = demo_db_name + '_' + 'v14'+'_'+'ent'
                    if self.sh_version_id.name == 'Odoo 13' and self.sh_edition_id.name == 'Community':
                        demo_db_name = demo_db_name + '_' + 'v13'+'_'+'com'
                    elif self.sh_version_id.name == 'Odoo 13' and self.sh_edition_id.name == 'Enterprise':
                        demo_db_name = demo_db_name + '_' + 'v13'+'_'+'ent'
                    if self.sh_version_id.name == 'Odoo 12' and self.sh_edition_id.name == 'Community':
                        demo_db_name = demo_db_name + '_' + 'v12'+'_'+'com'
                    elif self.sh_version_id.name == 'Odoo 12' and self.sh_edition_id.name == 'Enterprise':
                        demo_db_name = demo_db_name + '_' + 'v12'+'_'+'ent'
                    if self.sh_version_id.name == 'Odoo 16' and self.sh_edition_id.name == 'Community':
                        demo_db_name = demo_db_name + '_' + 'v16'+'_'+'com'
                    elif self.sh_version_id.name == 'Odoo 16' and self.sh_edition_id.name == 'Enterprise':
                        demo_db_name = demo_db_name + '_' + 'v16'+'_'+'ent'
                    if self.sh_version_id.name == 'Odoo 17' and self.sh_edition_id.name == 'Community':
                        demo_db_name = demo_db_name + '_' + 'v17'+'_'+'com'
                    elif self.sh_version_id.name == 'Odoo 17' and self.sh_edition_id.name == 'Enterprise':
                        demo_db_name = demo_db_name + '_' + 'v17'+'_'+'ent'
                    if self.sh_version_id.name == 'Odoo 18' and self.sh_edition_id.name == 'Community':
                        demo_db_name = demo_db_name + '_' + 'v18'+'_'+'com'
                    elif self.sh_version_id.name == 'Odoo 18' and self.sh_edition_id.name == 'Enterprise':
                        demo_db_name = demo_db_name + '_' + 'v18'+'_'+'ent'
                    if self.product_ids:
                        if self.product_ids[0].sh_demo_db_template_name:
                            demo_db_name = self.product_ids[0].sh_demo_db_template_name
                        url_for_duplicate_db = demo_server_id.sh_server_url + '/web/database/duplicate'
                        data = {'master_pwd': demo_server_id.sh_master_password,
                                'name': demo_db_name, 'new_name': new_db_name}

                        try:
                            result = requests.post(
                                url=url_for_duplicate_db, data=data)
                            if result.status_code == 200:
                                self.sh_demo_db_create_date = fields.Datetime.now()
                                self.sh_demo_db_expired_date = self.sh_demo_db_create_date + + \
                                    timedelta(
                                        hours=self.env.user.company_id.sh_expired_demo_db)
                                self.sh_demo_db_url = demo_server_id.sh_server_url + '?db='+new_db_name
                                self.sh_demo_db_name = new_db_name
                                url = demo_server_id.sh_server_url
                                db = new_db_name
                                username = demo_server_id.sh_user_login
                                password = demo_server_id.sh_user_password
                                common = xmlrpc.client.ServerProxy(
                                    '{}/xmlrpc/2/common'.format(url))
                                uid = common.authenticate(
                                    db, username, password, {})
                                models = xmlrpc.client.ServerProxy(
                                    '{}/xmlrpc/2/object'.format(url))
                                for product in self.product_ids:
                                    update_module_id = models.execute_kw(
                                        db, uid, password, 'base.module.update', 'create', [{}])
                                    u_module_id = models.execute_kw(
                                        db, uid, password, 'base.module.update', 'update_module', [[update_module_id]])
                                    search_module_id = models.execute_kw(db, uid, password, 'ir.module.module', 'search', [
                                                                         [['name', '=', product.sh_technical_name], ['state', '=', 'uninstalled']]], {'limit': 1})
                                    if len(search_module_id) > 0:
                                        module_id = models.execute_kw(
                                            db, uid, password, 'ir.module.module', 'button_immediate_install', [[search_module_id[0]]])
                                
                                # template_id = self.env.ref('sh_demo_db.sh_demo_db_template')
                                # if template_id:
                                #     template_id.sudo().send_mail(self.id, force_send=True)
                                if self.partner_id:
                                    search_user_id = models.execute_kw(db, uid, password, 'res.users', 'search', [
                                                                       [['id', '=', 2]]], {'limit': 1})
                                    if len(search_user_id) > 0:
                                        self.sh_demo_password = self.sh_password_generate()
                                        new_user_id = models.execute_kw(
                                            db, uid, password, 'res.users', 'copy', [[search_user_id[0]]])
                                        group_id = models.execute_kw(db, uid, password, 'res.groups', 'search', [
                                                                     [['name', '=', 'Super Admin']]], {'limit': 1})
                                        if isinstance(new_user_id, list):
                                            new_user_id = new_user_id[0]
                                        if group_id:
                                            group_id = models.execute_kw(db, uid, password, 'res.groups', 'write', [
                                                                         [group_id[0]], {'users': [(3, new_user_id)]}])
                                        if self.partner_id.email and self.sh_demo_password:
                                            user_id = models.execute_kw(db, uid, password, 'res.users', 'write', [[new_user_id], {
                                                                        'name': self.partner_id.name, 'login': self.partner_id.email, 'password': self.sh_demo_password}])
                                            partner_search_id = models.execute_kw(db, uid, password, 'res.users', 'search_read', [[['id', '=', new_user_id]]], {'fields': ['partner_id'], 'limit': 1})
                                            partner_id = models.execute_kw(db, uid, password, 'res.partner', 'write', [[partner_search_id[0].get('partner_id')[0]], {
                                                                        'email': self.partner_id.email}])
                                        elif not self.partner_id.email and self.sh_demo_password:
                                            user_id = models.execute_kw(db, uid, password, 'res.users', 'write', [[new_user_id], {
                                                                        'name': self.partner_id.name, 'login': self.partner_id.name, 'password': self.sh_demo_password}])
                                db_content = '<p>'
                                if self.partner_id.name:
                                    db_content += 'Dear '+'<strong>'+self.partner_id.name+'</strong>'+'<br/><br/>'
                                db_content += '<strong>Here is your demo database login details</strong>'+'<br/><br/>'
                                db_content += '<strong>URL : </strong>'+self.sh_demo_db_url+'<br/><br/>'
                                if self.partner_id.email:
                                    db_content += '<strong>Username/Email : </strong>' + \
                                        self.partner_id.email+'<br/><br/>'
                                if self.sh_demo_password:
                                    db_content += '<strong>Password : </strong>'+self.sh_demo_password+'<br/><br/>'
                                db_content += "</p>"
                                if db_content:
                                    self.sh_demo_content = db_content
                                db_vals = {
                                    'db_create_date': self.sh_demo_db_create_date,
                                    'sh_database_name': self.sh_demo_db_name,
                                    'sh_password': self.sh_demo_password,
                                    'sh_url': demo_server_id.sh_server_url,
                                    'partner_id': self.partner_id.id,
                                    'log_message': 'Created Successfully.',
                                    'ticket_id': self.id,
                                }
                                if self.partner_id.email:
                                    db_vals.update({
                                        'sh_username': self.partner_id.email
                                    })
                                else:
                                    db_vals.update({
                                        'sh_username': self.partner_id.name
                                    })
                                self.env['sh.demo.db.log'].sudo().create(
                                    db_vals)
                        except Exception as e:
                            self.env['sh.demo.db.log'].sudo().create({
                                'db_create_date': self.sh_demo_db_create_date,
                                'sh_url': demo_server_id.sh_server_url,
                                'partner_id': self.partner_id.id,
                                'log_message': str(e),
                                'ticket_id': self.id,
                                'sh_database_name':new_db_name,
                                'sh_password': self.sh_demo_password,
                            })
                            _logger.error("%s", e)
        return super(HelpdeskTicket, self).action_approve()

    @api.model
    def _run_drop_demo_db(self):
        demo_limit = 10
        default_company = self.env['res.company'].sudo().search([('id','=',1)])
        if default_company and default_company.sh_demo_limit > 0:
            demo_limit = default_company.sh_demo_limit
        tikcet_ids = self.env['sh.helpdesk.ticket'].sudo().search(
            [('sh_drop_db','=',False),('sh_demo_ticket', '=', True), ('sh_demo_db_expired_date', '<', fields.Datetime.now())],limit=demo_limit)
        url_for_drop_db = ''
        if tikcet_ids:
            for ticket in tikcet_ids:
                if ticket.sh_version_id and ticket.sh_edition_id:
                    demo_server_id = self.env['sh.servers'].sudo().search(
                        [('sh_version_id', '=', ticket.sh_version_id.id), ('sh_edition_id', '=', ticket.sh_edition_id.id)], limit=1)
                    if demo_server_id and ticket.sh_demo_db_name:
                        try:                            
                            list_db_url = demo_server_id.sh_server_url+'/web/database/list'
                            r = requests.post(list_db_url, json={})
                            if r.status_code == 200:
                                json_data_result = r.json().get('result')
                                if ticket.sh_demo_db_name in json_data_result:
                                    url_for_drop_db = demo_server_id.sh_server_url + '/web/database/drop'
                                    data = {
                                        'master_pwd': demo_server_id.sh_master_password, 'name': ticket.sh_demo_db_name}
                                    result = requests.post(url=url_for_drop_db, data=data)
                                    if result.status_code == 200:
                                        db_vals = {
                                            'db_create_date': fields.Datetime.now(),
                                            'sh_database_name': ticket.sh_demo_db_name,
                                            'sh_url': demo_server_id.sh_server_url,
                                            'log_message': 'Droped Successfully.',
                                            'ticket_id': ticket.id,
                                        }
                                        self.env['sh.demo.db.log'].sudo().create(
                                            db_vals)
                                        ticket.sudo().write({
                                            'sh_drop_db':True
                                        })
                                else:
                                    ticket.sudo().write({
                                        'sh_drop_db':True
                                    })
                        except Exception as e:
                            db_vals = {
                                    'db_create_date': fields.Datetime.now(),
                                    'sh_database_name': ticket.sh_demo_db_name,
                                    'sh_url': demo_server_id.sh_server_url,
                                    'log_message': str(e),
                                    'ticket_id': ticket.id,
                                }
                            self.env['sh.demo.db.log'].sudo().create(db_vals)
                            activity_type = self.env['mail.activity.type'].search(
                                    [('name', '=', 'Exception')], limit=1)
                            self.env['mail.activity'].create({
                                'activity_type_id': activity_type.id,
                                'res_id': ticket.id,
                                'res_model_id': self.env['ir.model']._get('sh.helpdesk.ticket').id,
                                'user_id': default_company.sh_db_drop_activity_assign_id.id if default_company.sh_db_drop_activity_assign_id else self.env.user.id,
                                'date_deadline': fields.date.today(),
                                'summary': str(ticket.name) + ' Demo DB Delete Operation Failed',
                                'note': str(e)
                            })
                            _logger.error("%s", e)


    def action_delete_demo_database(self):
        default_company = self.env['res.company'].sudo().search([('id','=',1)])
        for rec in self:
            if not rec.sh_drop_db and rec.sh_demo_ticket and rec.sh_demo_db_expired_date < fields.Datetime.now() and rec.sh_version_id and rec.sh_edition_id:
                demo_server_id = self.env['sh.servers'].sudo().search(
                    [('sh_version_id', '=', rec.sh_version_id.id), ('sh_edition_id', '=', rec.sh_edition_id.id)], limit=1)
                if demo_server_id and rec.sh_demo_db_name:
                    try:                            
                        list_db_url = demo_server_id.sh_server_url+'/web/database/list'
                        r = requests.post(list_db_url, json={})
                        if r.status_code == 200:
                            json_data_result = r.json().get('result')
                            if rec.sh_demo_db_name in json_data_result:
                                url_for_drop_db = demo_server_id.sh_server_url + '/web/database/drop'
                                data = {
                                    'master_pwd': demo_server_id.sh_master_password, 'name': rec.sh_demo_db_name}
                                result = requests.post(url=url_for_drop_db, data=data)
                                if result.status_code == 200:
                                    db_vals = {
                                        'db_create_date': fields.Datetime.now(),
                                        'sh_database_name': rec.sh_demo_db_name,
                                        'sh_url': demo_server_id.sh_server_url,
                                        'log_message': 'Droped Successfully.',
                                        'ticket_id': rec.id,
                                    }
                                    self.env['sh.demo.db.log'].sudo().create(
                                        db_vals)
                                    rec.sudo().write({
                                        'sh_drop_db':True
                                    })
                            else:
                                rec.sudo().write({
                                    'sh_drop_db':True
                                })
                    except Exception as e:
                        db_vals = {
                                'db_create_date': fields.Datetime.now(),
                                'sh_database_name': rec.sh_demo_db_name,
                                'sh_url': demo_server_id.sh_server_url,
                                'log_message': str(e),
                                'ticket_id': rec.id,
                            }
                        self.env['sh.demo.db.log'].sudo().create(db_vals)
                        activity_type = self.env['mail.activity.type'].search(
                                [('name', '=', 'Exception')], limit=1)
                        self.env['mail.activity'].create({
                            'activity_type_id': activity_type.id,
                            'res_id': rec.id,
                            'res_model_id': self.env['ir.model']._get('sh.helpdesk.ticket').id,
                            'user_id': default_company.sh_db_drop_activity_assign_id.id if default_company.sh_db_drop_activity_assign_id else self.env.user.id,
                            'date_deadline': fields.date.today(),
                            'summary': str(rec.name) + ' Demo DB Delete Operation Failed',
                            'note': str(e)
                        })
                        _logger.error("%s", e)

