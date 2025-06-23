# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields

class BlogPostVideo(models.Model):
    _name = 'blog.post.video'
    _description = "Blog Post Video"
    
    name = fields.Char('Name')
    link = fields.Char('Link')
    active = fields.Boolean('Active')
    company_id = fields.Many2one('res.company', string='Company',
        default=lambda self: self.env.company)