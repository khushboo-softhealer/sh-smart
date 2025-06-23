from odoo import models, fields, api

class responseWizard(models.TransientModel):
    _name = 'sh.response.wizard'

    response_message = fields.Text(readonly=True)
    