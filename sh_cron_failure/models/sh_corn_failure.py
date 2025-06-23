from odoo import _, api, fields, models
from datetime import datetime
class ShCronFailureLog(models.Model):
    _name = "sh.cron.failure"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Sh Cron Failure Show the record of failed cron"
    _order = 'id desc'

    name = fields.Char(string='Cron Name')
    time = fields.Datetime(string='Time',compute="_compute_time")
    
    failure_time = fields.Char(string='Time')
    failure_reason = fields.Text(string="Failure Reason")
    cron = fields.Many2one('ir.cron',String="Cron")

    @api.depends('failure_time')
    def _compute_time(self):
        for record in self:
            record.time = datetime.strptime(record.failure_time, '%d-%m-%Y %H:%M:%S')  # expects YYYY-MM-DD
 
