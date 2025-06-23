# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class HrDepartureWizard(models.TransientModel):
    _inherit = 'hr.departure.wizard'

    sh_archive_user = fields.Boolean(string='Archive User ?',default=True)

    def action_register_departure(self):
        res =  super(HrDepartureWizard, self).action_register_departure()
        
        context = self.env.context.copy()

        employee_id =self.env['hr.employee'].browse(context['active_id'])

        if employee_id and employee_id.user_id and self.sh_archive_user:
            employee_id.user_id.active = False