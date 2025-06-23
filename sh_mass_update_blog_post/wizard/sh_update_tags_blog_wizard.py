# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import models, fields


class UpdateBlogTag(models.TransientModel):
    _name = 'sh.update.tags.blog'
    _description = 'Update Tags'

    change_method = fields.Selection([('add', 'Add'), ('replace', 'Replace'), (
        'remove', 'Remove')], string="Change Method", default="add")
    tag_ids = fields.Many2many("blog.tag", string="Blog Tags")

    def update_blog_tag(self):
        blog_ids = self.env.context.get('default_blog_ids')
        if blog_ids and blog_ids[0] and blog_ids[0][2]:
            blogs = blog_ids[0][2]
            for blog in blogs:
                blog_obj = self.env['blog.post'].browse(blog)
                if self.change_method == 'add':
                    for tag in self.tag_ids:
                        blog_obj.write({'tag_ids': [(4, tag.id)]})
                elif self.change_method == 'replace':
                    blog_obj.write({'tag_ids': [(6, 0, self.tag_ids.ids)]})
                elif self.change_method == 'remove':
                    for tag in self.tag_ids:
                        blog_obj.write({'tag_ids': [(3, tag.id)]})
