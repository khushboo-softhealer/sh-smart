# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

from odoo.addons.auth_signup.models.res_partner import SignupError, now



class ResUsers(models.Model):
    _inherit = 'res.users'

    # @api.model_create_multi
    # def create(self, vals_list):
    #     # overridden to automatically invite user to sign up
    #     users = super(ResUsers, self).create(vals_list)
    #     if not self.env.context.get('no_reset_password'):
    #         users_with_email = users.filtered('email')
    #         if users_with_email:
    #             try:
    #                 users_with_email.with_context(create_user=True).action_reset_password()
    #             except MailDeliveryException:
    #                 users_with_email.partner_id.with_context(create_user=True).signup_cancel()
    #     return users

    # @api.returns('self', lambda value: value.id)
    # def copy(self, default=None):
    #     self.ensure_one()
    #     sup = super(ResUsers, self)
    #     if not default or not default.get('email'):
    #         # avoid sending email to the user we are duplicating
    #         sup = super(ResUsers, self.with_context(no_reset_password=True))
    #     return sup.copy(default=default)
    

    # @api.returns('self', lambda value: value.id)
    # def copy(self, default=None):
    #     user = super(ResUsers, self).copy(default)
    #     # reward_lines = order.order_line.filtered('is_reward_line')
    #     # if reward_lines:
    #     #     reward_lines.unlink()

    #     # SOFTHEALER CUSTOM CODE TO STORE PENDING VERIFICATION EMAILS IN MODE MODEL
    #     # TO PREVENT IT TO SIGNUP THROUGH API/BOT
    #     sh_signup_otp_email = self.env['sh.signup.otp.email'].sudo().search([
    #         ('email','=', user.login),
    #         ('state','=','verified')

    #     ])
    #     if not sh_signup_otp_email:
    #         raise ValueError(_('Signup: Please verify your email with the OTP.'))


    #     # SOFTHEALER CUSTOM CODE TO STORE PENDING VERIFICATION EMAILS IN MODE MODEL

    #     return user
    

    @api.model
    def _signup_create_user(self, values):
        # SOFTHEALER CUSTOM CODE TO STORE PENDING VERIFICATION EMAILS IN MODE MODEL
        # TO PREVENT IT TO SIGNUP THROUGH API/BOT
        sh_signup_otp_email = self.env['sh.signup.otp.email'].sudo().search([
            ('email','=', values.get('login',False) ),
            ('state','=','verified')

        ])
        if not sh_signup_otp_email:
            raise SignupError(_('Signup: Please verify your email with the OTP.'))

        # SOFTHEALER CUSTOM CODE TO STORE PENDING VERIFICATION EMAILS IN MODE MODEL
        new_user = super(ResUsers, self)._signup_create_user(values)
        return new_user
        
        