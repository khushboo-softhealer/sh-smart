# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.


from odoo import models, fields

class RepliedStatus(models.Model):
    _name = 'sh.replied.status'
    _description = 'Replied Status'
    _order = "sequence, name, id"

    name = fields.Char('Name',required=True)
    sh_customer_replied = fields.Boolean('Customer Replid')
    sh_staff_replied = fields.Boolean('Staff Replid')
    sh_running = fields.Boolean('Running')
    sh_closed = fields.Boolean('Closed')
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    company_id = fields.Many2one('res.company', string='Company',
        default=lambda self: self.env.company)