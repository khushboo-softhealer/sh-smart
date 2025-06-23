# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields, api
import datetime
from datetime import datetime


class AssetsManitenanceRequests(models.Model):
    _inherit = ['mail.thread',
                'mail.activity.mixin']
    _name = 'asset.request'
    _description = 'Maintenance Request'
    _rec_name = 'employee_id'

    asset_ids = fields.Many2many(
        'sh.asset', string='Assets', tracking=True)
    asset_type_id = fields.Many2one('sh.asset.type',string="Asset Type",tracking=True)
    technician_id = fields.Many2one(
        'res.users', string='Technician', tracking=True)
    problem = fields.Text(string='Probelm', required=True,
                          tracking=True)
    employee_id = fields.Many2one(
        'hr.employee', string='Employee', tracking=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible Person', tracking=True)
    partner_id = fields.Many2one(
        'res.partner', string='Vendor', tracking=True)
    create_date = fields.Datetime(readonly=True, tracking=True)
    update_date = fields.Datetime(readonly=True, tracking=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("under_process", "UnderProcess"),
            ("solved", "Solved"),
            ("scrap", "Scraped"),
            ("cancel", "Cancel"),
        ],
        default="new",
        tracking=True,
    )
    priority = fields.Selection(
        [
            ("high", "High"),
            ("medium", "Medium"),
            ("low", "Low"),
        ],
        default="high",
        tracking=True,
    )

    request_type = fields.Selection([('device', 'Allocated Device'), ('other', 'General Device'),('new','New Device'),('software','Software Issue')], string='Request Type',tracking=True)

    def scrap(self):
        self.state = "scrap"
        self.asset_ids.state = "scrap"

    def repair(self):
        self.state = "under_process"
        self.asset_ids.state = "repairing"

    def repairing_done(self):
        self.state = "solved"
        self.asset_ids.state = "running"

    def cancel_request(self):
        self.state = "cancel"
        self.asset_ids.state = "running"

    @api.model_create_multi
    def create(self, vals_list):
        record = super(AssetsManitenanceRequests, self).create(vals_list)
        record.create_date = datetime.today()
        return record

    def write(self, vals):
        vals.update({'update_date': datetime.today()})
        res = super(AssetsManitenanceRequests, self).write(vals)
        if self.state == "cancel":
            self.asset_ids.state = "running"
        return res
