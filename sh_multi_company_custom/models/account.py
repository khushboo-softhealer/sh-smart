# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    company_alert = fields.Boolean(
        string="",compute='_company_alert_onchange')

    @api.model
    def default_get(self, fields):
        res = super(AccountMove, self).default_get(fields)
        company_alert = False
        if self.env.company.name == 'Softhealer Technologies Private Limited':
            company_alert = True
        else:
            company_alert = False
        res.update({
            'company_alert': company_alert,
        })
        return res

    # @api.onchange('company_id')
    # @api.depends('company_id')
    def _company_alert_onchange(self):
        for rec in self:
            
            rec.company_alert = False
            if rec.company_id.name == 'Softhealer Technologies Private Limited':
                rec.company_alert = True
            else:
                rec.company_alert = False


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    task_id = fields.Many2one(
        'project.task', 'Task', index='btree_not_null',
        compute='_compute_task_id', store=True, readonly=False,
        domain="[('project_id.allow_timesheets', '=', True), ('project_id', '=?', project_id)]")
    