# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class EstimationTempalte(models.Model):
    _name = "sh.estimation.template"
    _description = "Estimation Template"

    name = fields.Char(string="Name", copy=False)
    estimation_template_line = fields.One2many('sh.estimation.template.line', 'estimation_template_id', string='Estimation Template Lines')


class EstimationLabel(models.Model):
    _name = "sh.estimation.label"
    _description = "Estimation Label"

    name = fields.Char("Label")

class EstimationTempalteLine(models.Model):
    _name = "sh.estimation.template.line"
    _description = "Estimation Template Line"

    name = fields.Char(string="Name")
    department_id = fields.Many2one('hr.department', 'Department')
    estimated_hours = fields.Float(string="Estimated Hours")
    accountable_user_ids = fields.Many2many('res.users', string="Accountable(s)",  domain="[('share', '=', False)]")
    responsible_user_ids = fields.Many2many('res.users','responsible_users', string="Responsible(s)",  domain="[('share', '=', False)]")
    other_details = fields.Text(string="Other Details")
    estimation_template_id = fields.Many2one('sh.estimation.template', string='Estimation Template')
    label_id = fields.Many2one("sh.estimation.label",string="Label")
    

class SaleLineEstimationTempalteLine(models.Model):
    _name = "sh.sale.line.estimation.template.line"
    _description = "Sale Order Line Estimation Template Line"

    name = fields.Char(string="Name")
    department_id = fields.Many2one('hr.department', 'Department')
    estimated_hours = fields.Float(string="Estimated Hours")
    accountable_user_ids = fields.Many2many('res.users', string="Accountable(s)")
    responsible_user_ids = fields.Many2many('res.users','sale_responsible_users', string="Responsible(s)")
    other_details = fields.Text(string="Other Details")
    estimation_template_id=fields.Many2one('sh.estimation.template', string='Estimation Template')
    sale_order_line_id=fields.Many2one('sale.order.line','Sale Order Line Id')
    project_id = fields.Many2one("project.project",'Project Id')
    label = fields.Char(string="Label")
    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    label_id = fields.Many2one("sh.estimation.label",string="Label")
    actual_from_date = fields.Date(string='Actual From Date')
    actual_to_date = fields.Date(string='Actual To Date')