# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models
from odoo.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit = "hr.employee"

    def action_manager_mass_tag_update(self):
        if self.env.user.has_group('hr.group_hr_user'):
            return {'name': 'Mass Update',
                    'res_model': 'sh.employee.manager.update.mass.tag.wizard',
                    'view_mode': 'form',
                    'context': {'default_all_hr_employee_ids': [(6, 0, self.env.context.get('active_ids'))]},
                    'view_id': self.env.ref('sh_emp_mass_update.sh_employee_manager_update_mass_tag_wizard_form_view').id,
                    'target': 'new',
                    'type': 'ir.actions.act_window'}
        else:
            raise ValidationError("You are not authorized to perform this !")
