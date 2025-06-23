# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError


class sh_signup_otp_verification_pending_email(models.Model):
    """ Model of blacklisted email addresses to stop signup by bot/api without OTP verification."""
    _name = 'sh.signup.otp.email'
    _description = 'signup otp verification email'
    _rec_name = 'email'
    _order = 'id desc'

    email = fields.Char(string='Email Address', required=True, index='trigram', help='This field is case insensitive.',
                        )
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('verified', 'Verified')
        ],
        string='Status',
        required=True,
        copy=False,
        default='draft',
    )