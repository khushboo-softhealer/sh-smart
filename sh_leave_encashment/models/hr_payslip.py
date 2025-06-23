# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import _, api, fields, models

class HrPayslip(models.Model):
    
    _inherit = 'hr.payslip'
    _description = "HR Payslip"

    def action_payslip_done(self):
        res = super(HrPayslip, self).action_payslip_done()
        print(f"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\t--------------> 13 DONE FLOW",)
        leave_encasement = self.env['sh.leave.encasement'].sudo().search([('employee','=',self.employee_id.id),('current_contract_id','=',self.contract_id.id),('stage','=','unpaid')],limit=1)
        
        if leave_encasement:
            leave_encasement.sudo().write({'stage':'paid'})

        return res
        
    def action_payslip_cancel(self):
        res = super(HrPayslip, self).action_payslip_cancel()
        print(f"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\t--------------> 23 CANCEL FLOW",)
        if self.contract_id:

            leave_encasement = self.env['sh.leave.encasement'].sudo().search([('employee','=',self.employee_id.id),('current_contract_id','=',self.contract_id.id),('stage','=','paid')],limit=1)
            print(f"\n\n\n\t--------------> 15 leave_encasement",leave_encasement.employee)

            if leave_encasement:
                leave_encasement.sudo().write({'stage':'unpaid'})

        return res