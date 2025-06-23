# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, _

from odoo.exceptions import ValidationError


class Slider(models.Model):
    _name = "sh.ecom.s.filter"
    _description = "Slider"

    name = fields.Char(string="Name", required=True, translate=True)

    filter_type = fields.Selection([
        ('domain', 'Domain'),
        ('manual', 'Manually')
    ], default="manual", string="Filter Type", required=True)

    tab_product_line = fields.One2many(
        comodel_name="sh.ecom.s.filter.tab.product.line", inverse_name="slider_id", string="Product Tabs")

    is_show_tab = fields.Boolean(string="Show Tabs?", default=True)
    is_show_slider = fields.Boolean(string="Show Slider?", default=False)

    # OWL OPTIONS
    items = fields.Integer(string='Items Per Slide', required=True, default=4)
    autoplay = fields.Boolean(string="Automatic Slide?", default=True)
    speed = fields.Integer(string="Slide Speed", default=300)
    loop = fields.Boolean(string="Loop Slide?", default=True)
    nav = fields.Boolean(string="Show Navigation Buttons?", default=True)


class SliderTabProductLine(models.Model):
    _name = "sh.ecom.s.filter.tab.product.line"
    _description = "Product Filter Tab"
    _order = "sequence, id"

    name = fields.Char(string="Tab Name", required=True, translate=True)
    product_tmpl_ids = fields.Many2many(
        comodel_name="product.template", string="Products")
    filter_id = fields.Many2one(
        comodel_name="ir.filters", string="Filter", domain='[("model_id","=","product.template" )]')
    slider_id = fields.Many2one('sh.ecom.s.filter', string='Slider Reference',
                                required=True, ondelete='cascade', index=True, copy=False)
    sequence = fields.Integer('Display order')
    limit = fields.Integer(string="Limit")
    
    categ_id = fields.Many2one(
        string='Category',
        comodel_name='product.public.category',
        ondelete='restrict',
    )
    

    @api.onchange('limit')
    def _onchange_limit(self):
        if self.limit and self.limit < 0:
            raise ValidationError(_('Limit must not be negative.'))
