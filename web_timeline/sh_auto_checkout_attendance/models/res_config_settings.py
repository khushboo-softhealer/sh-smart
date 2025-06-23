# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    auto_checkout = fields.Boolean("Enable Auto Checkout?", default=False)
    checkout_after = fields.Integer("Checkout After(minutes)")
    checkout_time = fields.Boolean(
        'Write Checkout datetime as same as Check in')

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        config_parameters = self.env["ir.config_parameter"].sudo()
        for record in self:
            config_parameters.set_param("sh_auto_checkout_attendance.auto_checkout",
                                        record.auto_checkout or False)
            config_parameters.set_param(
                "sh_auto_checkout_attendance.checkout_after", record.checkout_after)
            config_parameters.set_param(
                "sh_auto_checkout_attendance.checkout_time", record.checkout_time)
        return res

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        config_parameters = self.env["ir.config_parameter"].sudo()
        res.update(
            auto_checkout=config_parameters.get_param(
                "sh_auto_checkout_attendance.auto_checkout"),
            checkout_after=int(config_parameters.get_param(
                "sh_auto_checkout_attendance.checkout_after", default=0.0)),
            checkout_time=config_parameters.get_param(
                "sh_auto_checkout_attendance.checkout_time")
        )
        return res
