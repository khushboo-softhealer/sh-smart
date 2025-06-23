from odoo import models, fields
from datetime import timedelta, datetime


class GlobalLeaveWizard(models.TransientModel):
    _name = 'sh.global.leave.wizard'
    _description = "Global Leave Wizard"

    calendar_ids = fields.Many2many('resource.calendar')
    name = fields.Char(string="Reason")
    date_from = fields.Date('Date From', default=fields.Date.today())
    date_to = fields.Date('Date To', default=fields.Date.today())

    def update_global_leave(self):
        listt = []
        sdate = self.date_from
        edate = self.date_to
        date_list = [sdate+timedelta(days=x)
                     for x in range((edate-sdate).days + 1)]
        for date in date_list:
            day_before = date - timedelta(days=1)
            sdatetime = datetime(date.year, day_before.month,
                                 day_before.day, 18, 30, 00)
            edatetime = datetime(date.year, date.month, date.day, 18, 29, 59)
            listt.append((0, 0, {
                'name': self.name,
                'date_from': sdatetime,
                'date_to': edatetime
            }))
        self.calendar_ids.write({
            'global_leave_ids': listt
        })
