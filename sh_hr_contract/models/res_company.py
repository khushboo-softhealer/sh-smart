# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields
from odoo.tools.translate import html_translate


class ResCompany(models.Model):
    _inherit = 'res.company'

    annexure_b_notes = fields.Html('Annexure - B ',
                                   translate=html_translate,
                                   sanitize=False, prefetch=True)
