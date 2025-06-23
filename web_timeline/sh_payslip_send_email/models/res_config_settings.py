# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    send_payslip = fields.Boolean("Send Payslip in Email ?", default=True)
    sh_send_mail_on = fields.Selection([('personal', 'Personal Email'), ('work', 'Work Email'), ('both', 'Both')],
                                       default='work', string="Send mail on")


class ResConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    send_payslip = fields.Boolean(
        "Send Payslip in Email ?", related='company_id.send_payslip', readonly=False)
    sh_send_mail_on = fields.Selection(string="Send mail on", related="company_id.sh_send_mail_on", readonly=False)
