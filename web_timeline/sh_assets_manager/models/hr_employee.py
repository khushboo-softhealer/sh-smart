# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields


class Employee(models.Model):
    _inherit = 'hr.employee'

    asset_ids = fields.One2many('sh.asset', 'employee_id', string='Assets ')
    assets_count = fields.Integer(string="Assets",
                                  compute='_compute_assets_count')
    requests_count = fields.Integer(string='Maintenance requests',
                                    compute='_compute_requests_count')

    def _compute_assets_count(self):
        if self:
            for rec in self:
                assets = self.env['sh.asset'].sudo().search([('employee_id',
                                                              '=', rec.id)])
                if assets:
                    rec.assets_count = len(assets.ids)
                else:
                    rec.assets_count = 0

    def action_view_assets(self):
        return {
            'name': 'Assets',
            'type': 'ir.actions.act_window',
            'res_model': 'sh.asset',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'domain': [('employee_id', '=', self.id)],
            'target': 'current',
        }

    def _compute_requests_count(self):
        if self:
            for rec in self:
                requests = self.env['asset.request'].sudo().search([
                    ('employee_id', '=', rec.id)
                ])
                if requests:
                    rec.requests_count = len(requests.ids)
                else:
                    rec.requests_count = 0

    def action_view_requests(self):
        return {
            'name': 'Maintenance Requests',
            'type': 'ir.actions.act_window',
            'res_model': 'asset.request',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'domain': [('employee_id', '=', self.id)],
            'target': 'current',
        }


class Employee(models.Model):
    _inherit = 'hr.employee.public'

    asset_ids = fields.One2many('sh.asset', 'employee_id', string='Assets ')
    assets_count = fields.Integer(string="Assets",
                                  compute='_compute_assets_count')
    requests_count = fields.Integer(string='Maintenance requests',
                                    compute='_compute_requests_count')
