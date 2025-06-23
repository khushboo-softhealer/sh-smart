# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo.exceptions import ValidationError
from odoo import models, _


class ShHrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def sh_confirm_multiple_payslips(self):
        for payslip in self:
            if payslip.state == 'draft':
                get_groups = self.env['res.groups'].search([])
                for i in get_groups:
                    if i.category_id.name == 'Payroll' and i.name == 'Manager':
                        ids_list = i.users.ids
                        payslip.action_payslip_done()
                if self.env.user.id not in ids_list:
                    raise ValidationError(
                        _("You are not Authorized to Perform this !"))

            else:
                raise ValidationError(
                    _("Please Select Draft Stage Payslips !"))
