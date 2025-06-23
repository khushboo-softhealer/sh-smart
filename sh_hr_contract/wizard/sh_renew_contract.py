from odoo import models, fields, api, _
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta


class RenewContract(models.TransientModel):
    _name = 'sh.renew.contract'
    _description = "Renew Contract"

    employee_id = fields.Many2one("hr.employee",string="Employee")
    name = fields.Char("Contract Reference")
    date_start = fields.Date("Start Date")
    date_end = fields.Date("End Date")
    contract_type = fields.Selection([("month", "Month"), ("year", "Year")],
                                     default="month", string='Contract Type ', tracking=True)

    contract_period = fields.Integer(
        string="Period ", default=6, tracking=True)

    def _valid_field_parameter(self, field, name):
        # allow tracking on models inheriting from 'mail.thread'
        return name == 'tracking' or super()._valid_field_parameter(field, name)

    @api.model
    def default_get(self, fields):
        res = super(RenewContract, self).default_get(fields)
        if 'active_id' in self.env.context and 'active_model' in self.env.context:
            active_model = self.env.context.get("active_model")
            active_id = self.env.context.get("active_id")
            contract = self.env[active_model].browse(active_id)
            if contract:
                start_date = contract.date_end + timedelta(days=1)
                res.update({
                    'contract_type': contract.contract_type,
                    'contract_period': contract.contract_period,
                    'date_start':start_date,
                    'name':contract.employee_id.name + '\'s Contract from '+str(start_date),
                    'employee_id':contract.employee_id.id,
                })
        return res
    
    
    @api.onchange('contract_type', 'contract_period', 'date_start',)
    def _onchange_for_date_end(self):
        if self.date_start or self.contract_period:
            date = ' '
            if self.contract_type == 'month':
                date = self.date_start + \
                    relativedelta(months=self.contract_period, days=-1)
                self.date_end = date
            if self.contract_type == 'year':
                date = self.date_start + \
                    relativedelta(years=self.contract_period, days=-1)
                self.date_end = date

    def create_contract(self):
        if 'active_id' in self.env.context and 'active_model' in self.env.context:
            active_model = self.env.context.get("active_model")
            active_id = self.env.context.get("active_id")
            contract = self.env[active_model].browse(active_id)
            if contract:
                new_contract = contract.copy()
                new_contract.write({
                    'date_start':self.date_start,
                    'date_end':self.date_end,
                    'contract_type':self.contract_type,
                    'contract_period':self.contract_period,
                    'name':self.name,
                    'days_extend':0
                })
                return {
                    'name': 'Contract',
                    'type': 'ir.actions.act_window',
                    'res_model': 'hr.contract',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'target': 'current',
                    'res_id':new_contract.id
                }