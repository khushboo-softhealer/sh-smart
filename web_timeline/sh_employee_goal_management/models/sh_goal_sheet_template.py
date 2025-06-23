# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields
import calendar
from datetime import datetime,timedelta


class EmployeeSheetTemplate(models.Model):
    _name = 'sh.goal.sheet.template'
    _description = "List of all Templates"

    name = fields.Char(string="Template Name")
    category_ids = fields.Many2many(
        "sh.goal.sheet.category", string="Category")
    active = fields.Boolean('Active', default=True)
    employee_ids = fields.Many2many("hr.employee", string="Employees")

    def action_generate_goal_sheet(self):
        return {
            'name': 'Generate Goal Sheet',
            'res_model': 'sh.generate.goal.sheet.wizard',
            'view_mode': 'form',
            'view_id':
            self.env.ref(
                'sh_employee_goal_management.sh_generate_goal_sheet_wizard_Form'
            ).id,
            'target': 'new',
            'type': 'ir.actions.act_window'
        }

    def create_monthly_goal_template(self):
        # Check any pending goal sheet to submit
        todayDate = datetime.today().date()
        draft_sheets = self.env['sh.goal.sheet'].sudo().search([('stage','=','draft')])
        for draft_sheet in draft_sheets:
            if draft_sheet.coach_deadline:
                if draft_sheet.coach_deadline <= todayDate and not draft_sheet.sudo().submitted_by_coach:
                    draft_sheet.sudo().write({'auto_submitted_coach': True})
                    draft_sheet.action_submit_coach()
            if draft_sheet.employee_deadline:
                if draft_sheet.employee_deadline <= todayDate and not draft_sheet.sudo().submitted_by_employee:
                    draft_sheet.sudo().write({'auto_submitted_employee': True})
                    draft_sheet.action_submit_employee()

        if self.env.company.sh_goal_sheet_template_ids:

            for sh_goal_sheet_template_id in self.env.company.sh_goal_sheet_template_ids:
                sh_goal_sheet_template_id.sudo().generate_goals()



    def generate_goals(self):
        todayDate = datetime.today().date()
       
        first_date = todayDate.replace(day=1,month=todayDate.month-1)
        current_month_first_day = todayDate.replace(month=todayDate.month,day=1)

        last_date = current_month_first_day- timedelta(1)

        
       
        coach_deadline = todayDate + timedelta(days=self.env.company.coach_deadline)
        employee_deadline = todayDate + timedelta(days=self.env.company.employee_deadline)

        for employee in self.employee_ids:
            domain = [("employee_id", '=', employee.id), ('date_from',
                                                          '=', first_date), ('date_to', '=', last_date)]
            already_sheet = self.env['sh.goal.sheet'].search(domain)
            if not already_sheet:
                # check if last month goal sheet exist
                last_month_first_date = first_date.replace(month=first_date.month-1)

                last_month_last_date = first_date - timedelta(1)
                last_month_domain = [("employee_id", '=', employee.id), ('date_from',
                                                          '=', last_month_first_date), ('date_to', '=', last_month_last_date)]
                last_month_sheet = self.env['sh.goal.sheet'].search(last_month_domain)
                if last_month_sheet:
                    current_month_sheet = last_month_sheet.sudo().copy()
                    current_month_sheet.sudo().write({
                        'date_from' : first_date,
                        'date_to' : last_date,
                        'coach_deadline': coach_deadline,
                        'employee_deadline': employee_deadline,
                        'total_month':1,
                        'submitted_by_employee':False,
                        'submitted_by_coach':False,
                        'creation_type':'system',
                    })

                    # Update Category & related kpi in new generated goal sheet
                   
                    #Check if category removed 
                    if current_month_sheet.detail_ids.filtered(lambda x:x.category_id.id not in self.category_ids.ids):
                        removed_lines = current_month_sheet.detail_ids.filtered(lambda x:x.category_id.id not in self.category_ids.ids)
                        removed_lines.unlink()
                         
                    # find missing category
                   
                    for each_category in self.category_ids:  
                        if not current_month_sheet.detail_ids.filtered(lambda x:x.category_id.id == each_category.id):
                            missing_category = each_category
                            if missing_category:
                                line_list = []
                                section_vals = {
                                    'display_type': 'line_section',
                                    'name': missing_category.name,
                                     'category_id': missing_category.id,
                                }
                                line_list.append((0, 0, section_vals))
                                
                                for categ_line in missing_category.category_line_ids:
                                    line_vals = {
                                        'name': categ_line.name,
                                        'need_rating': categ_line.need_rating,
                                        'description': categ_line.description,
                                        'category_id': missing_category.id,
                                    }
                                    line_list.append((0, 0, line_vals))
                                if line_list:
                                    current_month_sheet.write({'detail_ids':line_list})
                                


                else:
                    difference = last_date - first_date
                    goal_vals = {
                        'employee_id': employee.id,
                        'coach_id': employee.coach_id.id,
                        'manager_id' : employee.coach_id.coach_id.id,
                        'date_from': first_date,
                        'date_to': last_date,
                        'total_month':1,
                        'coach_deadline': coach_deadline,
                        'employee_deadline': employee_deadline,
                        'creation_type':'system',
                    }
                    if difference.days <= 31:
                        goal_vals['total_month'] = 1
                    elif difference.days > 31 and difference.days < 185:
                        goal_vals['total_month'] = 6
                    line_list = []
                    # summary_list = []
                    for record in self.category_ids:
                        section_vals = {
                            'display_type': 'line_section',
                            'name': record.name,
                            'category_id': record.id,
                        }
                        line_list.append((0, 0, section_vals))
                        # summary_vals = {
                        #     'category_id': record.id
                        # }
                        # summary_list.append((0, 0, summary_vals))
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
