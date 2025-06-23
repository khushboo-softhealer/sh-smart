# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields, api


class AssetsRequest(models.TransientModel):
    _name = 'assets.request.wizard'
    _description = 'Assets Request Wizard'

    asset_ids = fields.Many2many('sh.asset',
                                 string='Equipments')
    employee_id = fields.Many2one('hr.employee',
                                  string='Employee',
                                  readonly=True)
    problem = fields.Text(string='Problem', required=True)

    maintenance = fields.Selection([('device', 'Allocated Device'), ('other', 'General Device'),('new','New Device'),('software','Software Issue')], string='Maintenance type', default='device')
    new_asset_id = fields.Many2one('sh.asset.type',string='Category') 
    priority = fields.Selection(
        [
            ("high", "High"),
            ("medium", "Medium"),
            ("low", "Low"),
        ],
        default="high",
        tracking=True,
    )
    general_asset_ids = fields.Many2many(
        'sh.asset','sh_general_asset_ids', string='General Assets', tracking=True)

    def _valid_field_parameter(self, field, name):
        # allow tracking on models inheriting from 'mail.thread'
        return name == 'tracking' or super()._valid_field_parameter(field, name)
    @api.model
    def default_get(self, fields):
        res = super(AssetsRequest, self).default_get(fields)
        employee_id = self.env['hr.employee'].sudo().search(
            [('user_id', '=', self.env.user.id)], limit=1)
        if employee_id:
            res.update({
                'employee_id': employee_id.id,
            })
        return res

    def action_submit(self):
        # assets = False
        if self.maintenance == 'device' or self.maintenance == 'other':
            request_id = self.env['asset.request'].sudo().create({
                'employee_id': self.employee_id.id,
                'problem': self.problem,
                'asset_ids': [(6, 0, self.asset_ids.ids if self.maintenance=='device' else self.general_asset_ids.ids)],
                'request_type' : self.maintenance,
                'user_id': self.env.user.company_id.user_id.id,
                'priority': self.priority})
        else :
            request_id = self.env['asset.request'].sudo().create({
                'employee_id': self.employee_id.id,
                'problem': self.problem,
                'asset_type_id': (self.new_asset_id.id if self.maintenance=='new' else False),
                'request_type' : self.maintenance,
                'user_id': self.env.user.company_id.user_id.id,
                'priority': self.priority})
        #     assets = self.asset_ids.ids
        # elif self.maintenance == 'other':
        #     assets = self.general_asset_ids.ids
        # elif self.maintenance == 'new':
        #     assets
        listt = []
        employees = self.env['hr.employee'].search([])
        user_list = [employee.user_id for employee in employees if employee.user_id]

        for users in user_list:
            if users.has_group('sh_assets_manager.asset_management_group'):
                listt.append(users)

        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        self.env['user.push.notification'].push_notification(listt,'New Asset Request Created ','Request ref %s'% (self.problem),base_url+"/mail/view?model=asset.request&res_id="+str(request_id.id),'asset.request', request_id.id,'hr')
