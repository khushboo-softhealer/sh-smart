from odoo import models, fields, api
from odoo.tools.translate import html_translate
from odoo.exceptions import ValidationError


class AssignEditionWizard(models.TransientModel):
    _name='sh.assign.edition.wizard'
    _description="Assign Edition Wizard"

    edition_ids=fields.Many2many('sh.edition',string="Edition",)
    product_ids = fields.Many2many('product.template',)

    def assign_mass_edition(self):
        self.product_ids.write({
            'sh_edition_ids': [(6, 0, self.edition_ids.ids)],
            'sh_edition_ids_duplicate': [(6, 0, self.edition_ids.ids)]
        })
