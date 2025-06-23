import string
from odoo import models,fields,api,_
from odoo.exceptions import UserError

class ResCompany(models.Model):
    _inherit = 'res.company'

    invoice_product_id = fields.Many2one('product.product',string = "Invoice Product")

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    invoice_product_id = fields.Many2one('product.product',string = "Invoice Product",
    related='company_id.invoice_product_id',readonly = False)