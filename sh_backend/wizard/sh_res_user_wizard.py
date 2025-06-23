# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields, api, _
from odoo.tools.translate import html_translate
from odoo.exceptions import ValidationError


class ResUser(models.TransientModel):
    _name = "sh.res.user.wizard"
    _description = 'User Wizard'

    user_id = fields.Many2one('res.users', string="User", )
    product_ids = fields.Many2many('product.template',)
    update_other_respnosible_users = fields.Boolean(string = "Update other reposnible user ?")
    update_method_user = fields.Selection([
        ("add", "Add"),
        ("replace", "Replace"),
    ],default="add")
    other_responsible_users = fields.Many2many('res.users',string = "Other Responsible Users")

    def assign_user(self):
        self.product_ids.write({'resposible_user_id': self.user_id.id})
        if self.update_other_respnosible_users:
            if self.update_method_user == 'add':
                for user in self.other_responsible_users:
                    self.product_ids.write({
                        'other_responsible_users' : [(4,user.id)]
                    })
            
            else:
                for user in self.other_responsible_users:
                    self.product_ids.write({
                        'other_responsible_users' : [(6,0,self.other_responsible_users.ids)]
                    })
