from odoo import models, fields, api
from odoo.tools.translate import html_translate
from odoo.exceptions import ValidationError

class AssignScaleWizard(models.TransientModel):
    _name='sh.assign.scale.wizard'
    _description="Assign Scale Wizard"

    scale_ids=fields.Many2one('sh.scale',string="Product Scale")
    product_ids = fields.Many2many('product.template',)

    def assign_mass_scale(self):
        self.product_ids.write({
            'sh_scale_ids':self.scale_ids.id
        })
