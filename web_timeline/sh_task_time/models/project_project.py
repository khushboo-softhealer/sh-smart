# Part of Softhealer Technologies.

from odoo import models,fields,api, _

class ProjectProject(models.Model):
    _inherit = ['project.project']

    is_temp_project = fields.Boolean("Temporary Project")

