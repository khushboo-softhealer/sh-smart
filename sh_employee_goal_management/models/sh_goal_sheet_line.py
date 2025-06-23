# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields, api
import json

class GoalSheetLine(models.Model):
    _name = 'sh.goal.sheet.line'
    _description = "List of all Goal Sheet Lines"

    name = fields.Char("Title")
    description = fields.Text("Description")
    employee_id = fields.Many2one("hr.employee", related="goal_id.employee_id",string="Employee",store=True)
    coach_id = fields.Many2one("hr.employee", related="goal_id.coach_id", string="Coach",store=True)
    manager_id = fields.Many2one("hr.employee", related="goal_id.manager_id", string="Manager",store=True)
    date_from = fields.Date("From Date", related="goal_id.date_from",store=True)
    date_to = fields.Date("To Date", related="goal_id.date_to",store=True)

    goal_id = fields.Many2one("sh.goal.sheet", string="Goal")
    employee_rating_id = fields.Many2one("sh.goal.marks",string="Employee Rating")
    employee_comment = fields.Text("Employee Justification")
    coach_rating_id = fields.Many2one("sh.goal.marks",string="Coach Rating")
    coach_comment = fields.Text("Coach Justification")
    need_rating = fields.Boolean("Need Rating")
    category_id = fields.Many2one('sh.goal.sheet.category', string="Category")
    display_type = fields.Selection(
        selection=[
            ('line_section', "Section"),
            ('line_note', "Note"),
        ],
        default=False)
    dynamic_domain = fields.Char(compute="_compute_dynamic_domain")
    is_required_for_emp = fields.Boolean("Is Required(Employee)",compute='_compute_is_desc_required')
    is_required_for_coach = fields.Boolean ("Is Required(coach)",compute='_compute_is_desc_required')
    stage = fields.Selection(related="goal_id.stage",store=True)
    
    @api.depends('coach_rating_id','employee_rating_id')
    def _compute_is_desc_required(self):
        for rec in self:
            rec.is_required_for_coach = False
            if rec.coach_rating_id.is_required_for_coach:
                rec.is_required_for_coach = True
            rec.is_required_for_emp = False
            if rec.employee_rating_id.is_required_for_emp:
                rec.is_required_for_emp = True


    def _compute_dynamic_domain(self):
        for rec in self:
            
            domain=[('id','in',rec.category_id.goal_marks_ids.ids)]
            rec.dynamic_domain = json.dumps(domain)