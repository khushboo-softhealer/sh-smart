# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models, _

class ShAddResponsibleUsers(models.TransientModel):
    _name = 'sh.responsible.users.wizard'
    _description = 'Add the responsible users'

    user_ids = fields.Many2many('res.users', string='Add Users')
    tmpl_ids = fields.Many2many('product.template', string='Templates')

    def btn_add_users(self):
        user_list = [(4, user.id) for user in self.user_ids]
        for tmpl in self.tmpl_ids:
            tmpl.write({
                'other_responsible_users': user_list
            })
