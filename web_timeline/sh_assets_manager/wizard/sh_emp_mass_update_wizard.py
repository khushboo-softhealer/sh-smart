# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models


class UpdateMassEmp(models.TransientModel):
    _name = "emp.mass.update.wizard"
    _description = "Mass Update Wizard"

    assets_ids = fields.Many2many("sh.asset", string="Assets")
    emp_id = fields.Many2one("hr.employee", string="Employees", required=True)

    def update_record(self):
        if self.emp_id:
            self.assets_ids.write({'employee_id': self.emp_id.id})