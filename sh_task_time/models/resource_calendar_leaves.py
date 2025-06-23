# Part of Softhealer Technologies.

from odoo import models, fields

class ResourceCalendarLeave(models.Model):
    _inherit = 'resource.calendar.leaves'

    is_saturday_leave = fields.Boolean("Saturday Leave")
