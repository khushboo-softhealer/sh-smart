# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields


class ShGithubBlogPost(models.Model):
    _inherit = 'blog.post'

    sh_product_id = fields.Many2one('product.product', string='Product Ref.')
    sh_is_from_gitub = fields.Boolean('Is From Github', compute='_compute_sh_is_from_gitub')
    sh_github_last_commit = fields.Char('Github Last Commit')

    def _compute_sh_is_from_gitub(self):
        for rec in self:
            rec.sh_is_from_gitub = False
            if rec.sh_product_id:
                if rec.sh_product_id.sh_branch_id:
                    rec.sh_is_from_gitub = True

    def _check_for_publication(self, vals):
        return False

    def write(self, vals):
        status = super(ShGithubBlogPost, self).write(vals)
        if vals.get('is_published'):
            for post in self:
                module_obj = self.env['sh.module'].sudo().search([
                    ('sh_blog_post_id', '=', post.id)
                ], limit=1)
                if module_obj:
                    module_obj._notify_partners()
        return status
