# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields

class BlogPost(models.Model):
    _inherit = 'blog.post'
    
    sh_video = fields.Many2many('blog.post.video', 'rel_sh_video', string='video')
    blog_image = fields.Binary(string='Blog Image')  
    sh_product_template_ids = fields.Many2many('product.template', string=" Products")  
    buy_now = fields.Char('Buy Now')
    company_id = fields.Many2one('res.company', string='Company',
        default=lambda self: self.env.company)