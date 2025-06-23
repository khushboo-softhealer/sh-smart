from odoo import models, fields, api

class DefaultPayment(models.Model):
    _name = 'sh.default.payment'
    _description = "Default Payment"

    name = fields.Char("Name")
    total_amount = fields.Float("Total Amount")
    default_formate = fields.Text("Default Formate")