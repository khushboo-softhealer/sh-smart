# Part of Softhealer Technologies.
from odoo import fields, models


class UpdatemassPricelist(models.TransientModel):
    _name = "sh.res.partner.mass.update.wizard"
    _description = "Mass Update Wizard"

    all_res_partner_ids = fields.Many2many('res.partner')
    update_pricelist_id = fields.Many2one(
        'product.pricelist', string='Pricelist')
    update_pricelist_bool = fields.Boolean(string="Update Pricelist")

    def update_record(self):
        if self.update_pricelist_bool == True:
            self.all_res_partner_ids.write(
                {'property_product_pricelist': self.update_pricelist_id.id})
