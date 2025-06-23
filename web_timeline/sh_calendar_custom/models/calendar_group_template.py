from odoo import models,fields,api,_

class CalendarGroupTemplate(models.Model):
    _name = 'sh.calendar.group.template'

    name = fields.Char(string = "Name",required = True)
    partner_ids = fields.Many2many('res.partner',string = "Attendees",domain = [('user_ids','!=',False)])