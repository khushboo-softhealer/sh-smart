# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models,_

class ShAllocationRejectReasonWizard(models.TransientModel):
    _name = "sh.allocation.reject.reason.wizard"
    _description = 'Employee Allocation Reject Reason'

    allocation_id = fields.Many2one('sh.employee.task.allocation', string="Allocation")
    sh_proposed_hours = fields.Float('Proposed Hours')
    sh_reject_reason = fields.Text('Reason to Reject')

    def action_reject_allocation(self):
        '''Move Employee Allocation to Rejected state with reason.'''
        # if self.
        self.bill_id.write({'state':'rejected'})
