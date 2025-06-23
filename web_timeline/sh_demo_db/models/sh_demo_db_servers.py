# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, _


class sh_demo_db_servers(models.Model):
    _name = 'sh.servers'
    _rec_name = 'sh_server_url'
    _description = "Servers"

    sh_server_url = fields.Char(string="Server Url", required=True)
    sh_master_password = fields.Char(
        string="Server Master Password", required=True)
    sh_user_login = fields.Char(
        string="Support User Login", required=True)
    sh_user_password = fields.Char(
        string="Support User Password", required=True)
    sh_version_id = fields.Many2one('sh.version',string='Version',required=True)
    sh_edition_id = fields.Many2one('sh.edition',string='Edition',required=True)
    sh_demo_template_db_password = fields.Char('Demo Template admin password')
    
