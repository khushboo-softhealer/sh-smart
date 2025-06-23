from odoo import api, models

class ir_ui_menu(models.Model):
    _inherit = "ir.ui.menu"

    @api.returns('self')
    def _filter_visible_menus(self):
        """ Filter `self` to only keep the menu items that should be visible in
            the menu hierarchy of the current user.
            Uses a cache for speeding up the computation.
        """
        self.env['ir.ui.menu'].sudo().clear_caches()

        res = super(ir_ui_menu, self)._filter_visible_menus()
        if res and self.env.user and self.env.user.sh_hm_hide_menu_ids:
            return res.filtered(lambda m: m.id not in self.env.user.sh_hm_hide_menu_ids.ids)
        return res
