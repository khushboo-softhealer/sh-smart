# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class ShMapCateg(models.Model):
    _name = "sh.map.categ"
    _description = "Map Categ"
    _rec_name = 'categ_id'

    categ_id = fields.Many2one('product.public.category', string='Category')
    categ_like = fields.Char('Category Like')
