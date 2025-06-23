# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import models


class BlogPost(models.Model):
    _inherit = 'blog.post'

    def action_update_tags_wizard(self):
        return{
            'name': 'Update Tags',
            'res_model': 'sh.update.tags.blog',
            'view_mode': 'form',
            'view_id': self.env.ref('sh_mass_update_blog_post.action_mass_update_blog_tags_form').id,
            'context': {'default_blog_ids': [(6, 0, self.env.context.get('active_ids'))]},
            'target': 'new',
            'type': 'ir.actions.act_window'
        }
