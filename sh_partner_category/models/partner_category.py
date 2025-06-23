# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import _, models, fields
from odoo.exceptions import UserError


class PartnerCategory(models.Model):
    _name = 'partner.category'
    _description = "Partner Category"
    
    name = fields.Char(string="Partner Category",
                       required=True)
    sequence = fields.Integer(string="Sequence")
    from_invoice_amount=fields.Float('From Invoice Amount')
    to_invoice_amount=fields.Float('to Invoice Amount')