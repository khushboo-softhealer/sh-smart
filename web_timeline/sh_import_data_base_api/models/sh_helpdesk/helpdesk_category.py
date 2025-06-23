# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class HelpdeskCategory(models.Model):
    _inherit = 'sh.helpdesk.category'

    remote_sh_helpdesk_category_id = fields.Char("Remote Helpdesk Category ID",copy=False)
    
class HelpdeskSubcategory(models.Model):
    _inherit ='helpdesk.subcategory'
    
    remote_helpdesk_subcategory_id = fields.Char("Remote Helpdesk SubCategory ID",copy=False)