# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models
import base64

class ShImageSlider(models.Model):
    _name = 'sh.image.slider'
    _description = "Sh Image Slider Snippet"

    name = fields.Char(string="Title", required=True)
    sub_title = fields.Char(string="Sub Title")
    # img = fields.Many2many('ir.attachment', string="Slider Images",) #for have multiple images in one field 
    # image_thumb_id = fields.Many2many('ir.attachment', string="Thumbnail Image", relation="sh_img_slider___ir_attachment",column1="image_id",column2="ir_attachment")
    website_published = fields.Boolean(string="Published")  # For website visibility

    images = fields.One2many('sh.image.slider.data','sh_image_slider_id',string="Slider Images")
    img = fields.Image(string="Thumbnail Image")
    sequence = fields.Integer(string='Sequence', default=10)

class ShImageSlider(models.Model):
    _name = 'sh.image.slider.data'
    _inherit = ['image.mixin']
    _description = "Sh Image Slider Data"
    _order = 'id'

    name = fields.Char("Name", required=True)
    # slider_image = fields.Image()
    sh_image_slider_id = fields.Many2one('sh.image.slider', "Sh Image Slider Id", index=True, ondelete='cascade')
