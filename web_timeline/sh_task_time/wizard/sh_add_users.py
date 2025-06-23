# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from datetime import datetime
from odoo import models, fields

class AddUsersTask(models.TransientModel):
    _name = 'sh.add.users'
    _description = "Add Users To Current Task"

    sh_user_ids = fields.Many2many("res.users","mail_list_wizard_user_custom_ids",'res_user_id','res_add_user_id',domain=[('share', '=', False)])

    def sh_add_users(self):       
        parent_id = self.env.context.get("active_id")

        parent_model = self.env.context.get("active_model")
        parent_record = self.env[parent_model].browse(parent_id)
        for user in self.sh_user_ids:
            parent_record.sudo().write({
                'user_ids' : [(4,user.id)]
            })
            parent_record.project_id.sudo().write({
                'responsible_user_ids' : [(4,user.id)]
            })