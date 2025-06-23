# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class OdooEndTicket(models.Model):
    _inherit = 'sh.odoo.end.ticket'

    remote_sh_odoo_end_ticket_id = fields.Char("Remote Odoo End Ticket ID",copy=False)


