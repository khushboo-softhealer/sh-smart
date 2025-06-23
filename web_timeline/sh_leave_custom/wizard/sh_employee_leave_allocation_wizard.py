# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models
from odoo.exceptions import UserError


class LeaveAllocationWizard(models.TransientModel):

    _name = "sh.employee.leave.allocation.wizard"
    _description = "Employee Leave Wizard"

    type = fields.Selection([('new', 'New Leave Allocation'), ('last',
                            'Merge With Last Contract')], string="Type", default='new')
    allocation_id = fields.Many2one(
        'hr.leave.allocation', string="Last Allocation")
    employee_id = fields.Many2one('hr.employee', string="Employee")
    contract_id = fields.Many2one('hr.contract', string="Contract")

    def create_leave_allocation(self, holiday_status_id, days):
        allocation_id = self.env['hr.leave.allocation'].create({
            'name' : self.employee_id.name + "'s " + str(days) + " leave" ,
            'holiday_status_id': holiday_status_id,
            'holiday_type': 'employee',
            'employee_id': self.employee_id.id,
            'date_end': self.contract_id.date_end,
            'date_start': self.contract_id.date_start,
            'number_of_days_display': days,
            'number_of_days': days,
            'employee_ids':[(6,0,[self.employee_id.id])]
        })
        return allocation_id

    def allocate_leave_wizard(self):
        if self.type == 'last' and not self.allocation_id:
            raise UserError(
                "Last Allocation not Found . Please select type New Leave Allocation !")
        if self.type == 'last' and self.allocation_id and self.employee_id:
            self.allocation_id.action_refuse()
            self.allocation_id.action_draft()
            if self.contract_id.contract_type == 'year':
                self.allocation_id.write({
                    'number_of_days': self.allocation_id.number_of_days + 14,
                    'date_end': self.contract_id.date_end,
                    'name' : self.employee_id.name + "'s " + str( self.allocation_id.number_of_days + 14) + " leave ",
                    'employee_ids':[(6,0,[self.employee_id.id])]
                })
                self.contract_id.write(
                    {'allocation_id': self.allocation_id.id})

            elif self.contract_id.contract_type == 'month' and self.contract_id.contract_period > 0:
                if self.contract_id.contract_period == 6:
                    self.allocation_id.write({
                        'number_of_days': self.allocation_id.number_of_days + 7,
                        'date_end': self.contract_id.date_end,
                         'name' : self.employee_id.name + "'s " + str( self.allocation_id.number_of_days + 7) + " leave ",
                        'employee_ids':[(6,0,[self.employee_id.id])]
                    })
                    self.contract_id.write(
                        {'allocation_id': self.allocation_id.id})

                elif self.contract_id.contract_period == 18:
                    self.allocation_id.write({
                        'number_of_days': self.allocation_id.number_of_days + 21,
                        'date_end': self.contract_id.date_end,
                         'name' : self.employee_id.name + "'s " + str( self.allocation_id.number_of_days + 21) + " leave ",
                    'employee_ids':[(6,0,[self.employee_id.id])]
                    })
                    self.contract_id.write(
                        {'allocation_id': self.allocation_id.id})

                elif self.contract_id.contract_period == 3:
                    self.allocation_id.write({
                        'number_of_days': self.allocation_id.number_of_days + 3.5,
                        'date_end': self.contract_id.date_end,
                         'name' : self.employee_id.name + "'s " + str( self.allocation_id.number_of_days + 3.5) + " leave ",
                    'employee_ids':[(6,0,[self.employee_id.id])]
                    })
                    self.contract_id.write(
                        {'allocation_id': self.allocation_id.id})

        elif self.type == 'new' and self.employee_id and self.contract_id:
            paid_leave_type = self.env['hr.leave.type'].sudo().search(
                [('unpaid', '=', False)], limit=1)
            if paid_leave_type:
                if self.contract_id.contract_type == 'year':
                    allocation_id = self.create_leave_allocation(
                        paid_leave_type.id, 14.0)
                    self.contract_id.write({'allocation_id': allocation_id.id})

                elif self.contract_id.contract_type == 'month' and self.contract_id.contract_period > 0:
                    if self.contract_id.contract_period == 6:
                        allocation_id = self.create_leave_allocation(
                            paid_leave_type.id, 7.0)
                        self.contract_id.write(
                            {'allocation_id': allocation_id.id})

                    elif self.contract_id.contract_period == 18:
                        allocation_id = self.create_leave_allocation(
                            paid_leave_type.id, 21.0)
                        self.contract_id.write(
                            {'allocation_id': allocation_id.id})

                    elif self.contract_id.contract_period == 3:
                        allocation_id = self.create_leave_allocation(
                            paid_leave_type.id, 3.5)
                        self.contract_id.write(
                            {'allocation_id': allocation_id.id})

                    else:
                        raise UserError(
                            "Contract Type and Period is not Valid !")
                else:
                    raise UserError("Contract Type and Period is not Valid !")
