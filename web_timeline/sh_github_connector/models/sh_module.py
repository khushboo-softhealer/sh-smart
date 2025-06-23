# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models
from datetime import datetime

class ShModule(models.Model):
    _name = "sh.module"
    _description = "Module"
    _rec_name = "display_name"

    name = fields.Char("Technical Name")
    display_name = fields.Char("Name", compute='_compute_display_name')
    sh_branch_id = fields.Many2one("sh.repo.branch", string="Branch")
    repo_id = fields.Many2one(related='sh_branch_id.repo_id', string='Repo')
    sh_product_id = fields.Many2one("product.product", string="Product Ref")
    sh_version = fields.Char(related='sh_product_id.product_version', string='Version')
    sh_blog_post_id = fields.Many2one("blog.post", string="Blog Post Ref")
    sh_module_url = fields.Char("Module Url")
    sh_img_url = fields.Char('Image URLs')
    sh_media_list = fields.Char('Media List')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('error', 'Error'),
    ], string='State')
    message = fields.Char('Message')
    datetime = fields.Datetime('Datetime')
    sha = fields.Char('Sha')
    active = fields.Boolean('Active', default=True)

    def _compute_display_name(self):
        for module in self:
            module.display_name = module.name
            if module.sh_branch_id:
                module.display_name += f" v{module.sh_branch_id.name.replace('.0', '')}"

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

    # ====================================================
    #  Cron: Sync Module From Queue
    # ====================================================
    def _cron_sync_modules_from_queue(self):
        modules = self.env['sh.module'].sudo().search(
            [('state', '=', 'draft')], limit=1)
        if not modules:
            modules = self.env['sh.module'].sudo().search(
                [('state', '=', 'error')], limit=1)
            if not modules:
                return
        for module in modules:
            module.sync_module(pop_up=False, field_type='p_queue')

    # ====================================================
    #  Multi Action: Sync Module From Queue
    # ====================================================
    def sync_module_from_queue(self):
        modules = self.sudo().browse(self.env.context.get('active_ids'))
        success = failed = 0
        failed_list = []
        for module in modules:
            if module.sync_module(pop_up=False):
                success += 1
            else:
                failed += 1
                failed_list.append(module.name)
        message = ''
        if success:
            message += f'{success} module(s) are sync successfully.'
        if failed:
            message += f'\n{failed} module(s) are failed to sync:\n{failed_list}'
        return self.show_message(message)

    # ====================================================
    #  Method: Sync Module
    # ====================================================
    def sync_module(self, connector_obj=False, pop_up=True, field_type='product'):
        try:
            self.write({
                'state': 'error',
                'datetime': datetime.now(),
                'message': 'Initial Error State !'
            })
            if not connector_obj:
                connector_obj = self.env["sh.github.connector"].sudo().search(
                    [("state", "=", "success")], limit=1)
            if not connector_obj:
                self.message = 'Please generate access token first !'
                return False
            state, message = self.create_update_product(connector_obj)
            # state, message = self.update_product_categ(connector_obj)
            # connector_obj.create_log("sync", field_type, message, state)
            if state == "success":
                self.write({
                    'state': 'done',
                    'message': message
                })
            else:
                self.write({
                    'state': 'error',
                    'message': message
                })
                connector_obj.create_log("sync", field_type, message, state)
            if pop_up:
                return self.show_message(message)
            if state == "success":
                return 1
            return False
        except Exception as e:
            self.message = e
            connector_obj.create_log("sync", "product", e)
            return False

    def show_product(self):
        view = self.env.ref("product.product_normal_form_view")
        return {
            "name": "Product",
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "product.product",
            "views": [(view.id, "form")],
            "view_id": view.id,
            "context": {
                'create': False,
                'delete': False
            },
            "res_id": self.sh_product_id.id
        }
