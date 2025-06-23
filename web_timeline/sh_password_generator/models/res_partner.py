# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    password_o2m = fields.One2many('password.generator','partner_id',string='Password ')

    def action_password(self):
        if self:
            list=[]
            for res in self.env['password.generator'].search([('partner_id','=',self.id)]):
                list.append(res.id)
            return{
                'type': 'ir.actions.act_window',
                'name':'Password Generator',
                'res_model': 'password.generator',
                'view_mode': 'tree,form',
                'domain':[('id', 'in',list)],
                'target': 'current',
            }
