# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields


class ShGithubProduct(models.Model):
    _inherit = "product.product"

    sh_branch_id = fields.Many2one(
        "sh.repo.branch", string="Branch/Version ref")
    sh_seo_summary = fields.Char("SEO Summary")
    sh_seo_description = fields.Char("SEO Description")

    def show_message(self, message):
        # ========== Pop-Up Message ==========
        view = self.env.ref("sh_message.sh_message_wizard")
        context = dict(self._context or {})
        context["message"] = message
        return {
            "name": f"Sync Module",
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "sh.message.wizard",
            "views": [(view.id, "form")],
            "view_id": view.id,
            "target": "new",
            "context": context,
        }

    def mul_action_unlink_mul_blogs(self):
        message = ''
        archived = 0
        for product in self:
            blogs = self.env['blog.post'].sudo().search([
                ('sh_product_id', '=', product.id)
            ])
            blogs_count = len(blogs)
            if blogs_count > 1:
                for blog in blogs:
                    # Archive The Blogs
                    blog.sudo().write({'active': False})
                    product.sudo().write({
                        'sh_blog_post_id': False
                    })
                    # Unlink The Blog
                    # blog.sudo().unlink()
                archived += blogs_count
        if archived:
            message += f'{archived} Blogs Are Archived.'
        else:
            message += 'Not Found Multiple Blogs For The Selected Products.'
        return self.show_message(message)

    def mul_action_add_module_in_queue(self):
        message = ''
        module_in_queue = 0
        module_not_found = []
        for product in self:
            module = self.env['sh.module'].sudo().search([
                ('sh_product_id', '=', product.id)
            ], limit=1)
            if module:
                module.sudo().write({'state': 'draft'})
                module_in_queue += 1
            else:
                module_not_found.append(product.name)
        if module_in_queue:
            message += f'{module_in_queue} Modules Added In The Queue.'
        if module_not_found:
            message += f'\nModule Queue Not Found For The {len(module_not_found)} Products:\n{module_not_found}'
        return self.show_message(message)
