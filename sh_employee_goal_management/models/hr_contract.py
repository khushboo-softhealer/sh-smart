# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields, api, _
from datetime import datetime,timedelta
from odoo.exceptions import UserError

class Contract(models.Model):
    _inherit = 'hr.contract'

    goal_sheet_id = fields.Many2one('sh.goal.sheet',string="Goal Sheet",copy=False)


    def action_view_goal_sheet(self):
        if self.goal_sheet_id:
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                "res_model": "sh.goal.sheet",
                'target': 'self',
                'res_id': self.goal_sheet_id.id
            }

class GenerateGoalSheetContract(models.TransientModel):
    _name = 'sh.generate.goal.sheet.wizard.contract'
    _description = "Wizard To create Goal Sheet from Contract"

    date_from = fields.Date("From Date",required=True)
    date_to = fields.Date("From to",required=True)
    employee_id = fields.Many2one("hr.employee", string="Employee",required=True)
    contract_id = fields.Many2one("hr.contract",string="Contract")

    @api.model
    def default_get(self, fields):
        res = super(GenerateGoalSheetContract, self).default_get(fields)
        hr_contract_id = self.env.context.get('active_id')
        hr_contract = self.env['hr.contract'].browse(hr_contract_id)
        if hr_contract:
            res.update({'date_from': hr_contract.date_start ,'date_to':hr_contract.date_end,
                        'employee_id':hr_contract.employee_id.id,
                        'contract_id':hr_contract.id})
        return res
    
    def generate_goals(self):
        if self.date_from and self.date_to and self.employee_id and self.contract_id:

            todayDate = datetime.today().date()
            coach_deadline = todayDate + timedelta(days=self.env.company.coach_deadline)
            employee_deadline = todayDate + timedelta(days=self.env.company.employee_deadline)

            # hr_contract_id = self.env.context.get('active_id')
            # hr_contract = self.env['hr.contract'].browse(hr_contract_id)
            hr_contract = self.contract_id
            
            employee = self.employee_id
            goal_vals = {
                'employee_id': employee.id,
                'coach_id': employee.coach_id.id,
                'manager_id' : employee.coach_id.coach_id.id,
                'date_from': self.date_from,
                'date_to': self.date_to,
                'total_month':6,
                'coach_deadline': coach_deadline,
                'employee_deadline': employee_deadline,
                'creation_type':'manually',
                'contract_id':hr_contract.id,

            }
            
            line_list = []

            goal_sheet_template = self.env['sh.goal.sheet.template'].search([('employee_ids','in',[employee.id])],limit=1)
            if not goal_sheet_template:
                raise UserError("Goal sheet template not found for this employee !")
            
            if goal_sheet_template:
                
                for record in goal_sheet_template.category_ids:
                    section_vals = {
                        'display_type': 'line_section',
                        'name': record.name,
                        'category_id': record.id,
                    }
                    line_list.append((0, 0, section_vals))
                
                    for categ_line in record.category_line_ids:
                        line_vals = {
                            'name': categ_line.name,
                            'need_rating': categ_line.need_rating,
                            'description': categ_line.description,
                            'category_id': record.id,
                        }
                        line_list.append((0, 0, line_vals))
                if line_list:
                    goal_vals['detail_ids'] = line_list
            
                goal_sheet_id = self.env['sh.goal.sheet'].create(goal_vals)
                hr_contract.sudo().write({'goal_sheet_id':goal_sheet_id.id})

