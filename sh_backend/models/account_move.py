# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields, api
from odoo.tools.translate import html_translate
from odoo.exceptions import ValidationError

class AccountMove(models.Model):
    _inherit = 'account.move'

    # def write(self, vals):
    #     print("=1111111111111111111111")
    #     for rec in self:
    #         print("==========vals",vals)
    #         if vals.get('payment_state') == 'paid':
    #             invoice = rec
    #             users = self.env['res.users'].search([])
    #             account_manager_listt = []

    #             for user in users:
    #                 if user.has_group('account.group_account_manager'):
    #                     account_manager_listt.append(user)
    #             print("\n\n==========account_manager_listt",account_manager_listt)
    #             base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
    #             self.env['user.push.notification'].push_notification(account_manager_listt,'New Payment Created for','Invoice Reference: '+rec.number,base_url+"/mail/view?model=account.move&res_id="+str(invoice.id),
    #                                                         'account.move',invoice.id,'sale')

    #     return super(AccountMove, self).write(vals)
