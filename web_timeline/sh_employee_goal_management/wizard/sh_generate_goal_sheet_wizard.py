# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields, api
# import datetime
from datetime import datetime,timedelta


class GenerateGoalSheet(models.TransientModel):
    _name = 'sh.generate.goal.sheet.wizard'
    _description = "Wizard To create Goal Sheet"

    date_from = fields.Date("From Date")
    date_to = fields.Date("From to")
    employee_ids = fields.Many2many("hr.employee", string="Employees")
    want_to_duplicate = fields.Boolean("Want to Duplicate ?",default=False)

    @api.model
    def default_get(self, default_fields):
        rec = super(GenerateGoalSheet, self).default_get(default_fields)
        if self.env.context and 'active_id' in self.env.context:
            res = self.env['sh.goal.sheet.template'].sudo().browse(
                self.env.context.get('active_id'))
            if res:
                rec['employee_ids'] = [(6, 0, res.employee_ids.ids)]
        return rec

    def generate_goals(self):
        active_template = self.env['sh.goal.sheet.template'].browse(
            self.env.context.get('active_id'))
        if active_template:
            date_1 = datetime.now().date()
            coach_deadline = date_1 + timedelta(days=self.env.company.coach_deadline)
            employee_deadline = date_1 + timedelta(days=self.env.company.employee_deadline)
            for employee in self.employee_ids:
                domain = [("employee_id", '=', employee.id), ('date_from',
                                                              '=', self.date_from), ('date_to', '=', self.date_to)]
                already_sheet = self.env['sh.goal.sheet'].search(domain)
                if not already_sheet:

                    # check if last month goal sheet exis
                    
                    last_month_domain = [("employee_id", '=', employee.id), ('creation_type','=','manually')]
                    last_month_sheet = self.env['sh.goal.sheet'].search(last_month_domain,order="id desc",limit=1)
                    
                    if last_month_sheet and self.want_to_duplicate:
                        current_month_sheet = last_month_sheet.sudo().copy()
                        current_month_sheet.sudo().write({
                            'date_from' : self.date_from,
                            'date_to' : self.date_to,
                            'coach_deadline': coach_deadline,
                            'employee_deadline': employee_deadline,
                            'submitted_by_employee':False,
                            'submitted_by_coach':False,
                            'creation_type':'manually',
                        })

                    else:
                        difference = self.date_to - self.date_from

                        goal_vals = {
                            'employee_id': employee.id,
                            'coach_id': employee.coach_id.id,
                            'manager_id' : employee.coach_id.coach_id.id,
                            'date_from': self.date_from,
                            'date_to': self.date_to,
                            'coach_deadline': coach_deadline,
                            'employee_deadline': employee_deadline,
                            'creation_type':'manually'
                        }
                        if difference.days <= 31:
                            goal_vals['total_month'] = 1
                        elif difference.days > 31 and difference.days < 185:
                            goal_vals['total_month'] = 6
                        line_list = []
                        for record in active_template.category_ids:
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
                        self.env['sh.goal.sheet'].create(goal_vals)
