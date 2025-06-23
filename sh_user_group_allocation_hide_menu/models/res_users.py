from odoo import  fields, models

class ResUsers(models.Model):
    _inherit = 'res.users'

    sh_hm_hide_menu_ids = fields.Many2many(
        comodel_name="ir.ui.menu",
        relation="rel_sh_hm_hide_menu_ir_ui_menu",
        string="Hide Menu"
    )
    template_ids = fields.Many2many(
        'sh.template', string="Templates", inverse="inverse_template")

    def inverse_template(self):

        user_groups = self.mapped('groups_id')

        if self.template_ids:
            for user_group in user_groups:
                self.write({'groups_id': [(3, user_group.id)]})

            template_groups = self.template_ids.mapped('group_ids')

            for template_group in template_groups:

                self.write({
                    'groups_id': [(4, template_group.id)]
                })

            for menu in self.sh_hm_hide_menu_ids.ids:
                self.write({
                    'sh_hm_hide_menu_ids': [(3, menu)]
                })

            menus = self.template_ids.mapped('menu_ids')
            for menu in menus:
                self.write({
                    'sh_hm_hide_menu_ids': [(4, menu.id)],
                })
