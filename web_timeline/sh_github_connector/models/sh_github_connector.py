# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models, _
import requests
from odoo.exceptions import UserError
from datetime import datetime


class ShGithubConnector(models.Model):
    _name = "sh.github.connector"
    _inherit = ["mail.thread","mail.activity.mixin"]
    _description = "Github Connector"

    # ====================================================
    #  Fields
    # ====================================================

    name = fields.Char('Name', tracking=True)
    user_name = fields.Char('Github User Name', tracking=True)
    access_token = fields.Char('Access Token', tracking=True)
    client_id = fields.Char('Client Id', tracking=True)
    client_secret = fields.Char('Client Secret', tracking=True)
    redirect_uri = fields.Char('Redirect Uri', tracking=True)
    token_type = fields.Char('Token Type', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('success', 'Success'),
        ('error', 'Failed')
    ], string='Status', default='draft', tracking=True)
    log_line = fields.One2many(
        'sh.connector.log', 'connector_obj_id', string='Log Line')
    active = fields.Boolean('Active', default='True', tracking=True)
    # ======== Configurations ========
    blog_blog_id = fields.Many2one('blog.blog', string='Blog Category', tracking=True)
    product_attribute_id = fields.Many2one(
        'product.attribute', string='Attribute', tracking=True)
    # product_attribute_value_ids = fields.Many2many(
    #     'product.attribute.value', string='Values(Versions)')
    # product_latest_version_id = fields.Many2one(
    #     'product.attribute.value', string='Latest Version')
    # Default Move From Project
    preappstore_project_id = fields.Many2one(
        'project.project', string='Preappstore Project', tracking=True)
    appstore_project_id = fields.Many2one(
        'project.project', string='Appstore Project', tracking=True)
    categ_id = fields.Many2one('product.category', string='Product Category', tracking=True)
    # activity_user_id = fields.Many2one(
    #     'res.users', string='Activity Assign To ')
    activity_user_ids = fields.Many2many(
        'res.users', string='Activity Assign To', help='''
    # Used when
        1) New Product is created
        2) Check Blog For Multi Language
        3) Failed to find appstore task using tech name and version
''', tracking=True)
    website_id = fields.Many2one('website', string='Website', tracking=True)
    ignore_dir = fields.Char('Ignore Directories', tracking=True)
    # notify_version_id = fields.Many2one(
    #     'product.attribute.value', string='Notify partners when the version is released')

    # ====================================================
    #  Authorise Credentials
    # ====================================================

    def authorise_creds(self):
        try:
            if self.client_id and self.client_secret and self.user_name:
                api_endpoint = f'https://github.com/login/oauth/authorize?client_id={self.client_id}&redirect_uri={self.redirect_uri}&state={int(self.id)}&login={self.user_name}&scope=repo'
                return {
                    'type': 'ir.actions.act_url',
                    'target': '_blank',
                    'url': api_endpoint
                }
            raise UserError(
                _("Please Re-Check Credentials and User Name and Try again!"))
        except Exception as e:
            raise UserError(_(e))

    # ====================================================
    #  Generate Access Token
    # ====================================================

    def generate_access_token(self, code=False):
        '''The code is valid for 10 Minutes.'''
        if not code:
            raise UserError(_("Failed To Generate Code"))
        # ====================================================
        #  If Get Code To Generate Access Token
        # ====================================================
        headers = {'Accept': 'application/json'}
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": self.redirect_uri,
        }
        token_endpoint = "https://github.com/login/oauth/access_token"
        response = requests.post(
            url=token_endpoint, headers=headers, params=params)
        if response.status_code == 200:
            json_data = response.json()
            self.access_token = json_data.get('access_token')
            self.token_type = json_data.get('token_type')
            self.create_log(
                'auth', 'auth', 'Token Generated Successfully.', 'success')
            self.state = 'success'
        else:
            self.create_log('auth', 'auth', 'Failed to Generate Token!')
            self.state = 'error'

    # ====================================================
    #  Create Log Method
    # ====================================================

    def create_log(self, operation='sync', field_type='-', message='Something Went Wrong!', state='error'):
        '''Create Log'''
        self.env['sh.connector.log'].sudo().create({
            'operation': operation,
            'field_type': field_type,
            'message': message,
            'state': state,
            'datetime': datetime.now(),
            'connector_obj_id': self.id
        })

    # ====================================================
    #  Get Req. Method
    # ====================================================

    def get_req(self, url, media_type='.raw'):
        '''Make a get request and return the response.
        Defuault Media Type = .raw'''
        # 'accept': 'application/vnd.github.html',
        # 'accept': 'application/vnd.github.raw',
        response = requests.get(url, headers={
            'Authorization': f'Bearer {self.access_token}',
            'accept': f'application/vnd.github{media_type}',
        })
        if response.status_code != 200:
            response_text = response.text
            if "Bad credentials" in response_text:
                self.state = "error"
                self.create_log('auth', 'auth', f'Please authorize with github to proceed, Response text: {response_text} !')
        return response

    # ====================================================
    #  Sync Repo(s)
    # ====================================================

    def sync_repo(self, repo):
        message = ''
        for branch_obj in repo.branch_line:
            branch_message = branch_obj.sync_branch(pop_up=False)
            if branch_message:
                message += f'\nFor Branch: \'{branch_obj.name}\':\n{branch_message}'
            repo.last_sync_date = datetime.now()
        return message

    # ------------------------------------------
    #  Create Activity
    # ------------------------------------------

    def _generate_activity(self, model, res_id, note):
        if not self.activity_user_ids:
            return
        res_model_id = self.env['ir.model'].sudo().search([
            ('model', '=', model)
        ], limit=1)
        for user in self.activity_user_ids:
            activity = self.env['mail.activity'].sudo().search([
                ('user_id', '=', user.id),
                ('res_model', '=', model),
                ('res_id', '=', res_id.id),
                ('note', '=', note),
                ('res_model_id', '=', res_model_id.id),
            ], limit=1)
            if not activity:
                activity = self.env['mail.activity'].sudo().create({
                    'res_model_id': res_model_id.id,
                    'user_id': user.id,
                    'res_model': model,
                    'res_id': res_id.id,
                    'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                    'note': note,
                    'date_deadline': datetime.now(),
                })

