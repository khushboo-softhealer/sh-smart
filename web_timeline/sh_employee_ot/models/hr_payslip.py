# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def action_payslip_done(self):

        res = super(HrPayslip, self).action_payslip_done()

        employee_ot_ids = self.env['sh.employee.ot'].search([('sh_employee_id','=',self.employee_id.id),('sh_ot_date', '>=', self.date_from), ('sh_ot_date', '<=', self.date_to),('state','=','done')])
        if employee_ot_ids:
            employee_ot_ids.write({'state' : 'paid'})

        return res
    
    def action_payslip_cancel(self):
        res = super(HrPayslip, self).action_payslip_cancel()

        employee_ot_ids = self.env['sh.employee.ot'].search([('sh_employee_id','=',self.employee_id.id),('sh_ot_date', '>=', self.date_from), ('sh_ot_date', '<=', self.date_to),('state','=','paid')])
        if employee_ot_ids:
            employee_ot_ids.write({'state' : 'done'})

        return res
