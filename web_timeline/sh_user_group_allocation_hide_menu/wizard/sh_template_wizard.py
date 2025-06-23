from odoo import api,  fields, models


class TemplateWizard(models.TransientModel):
    _name = 'sh.template.wizard'
    _description = "Template Wizard"

    name = fields.Char(string="Name", required=True)
    group_ids = fields.Many2many('res.groups')
    menu_ids = fields.Many2many('ir.ui.menu')

    @api.model
    def default_get(self, fields):

        rec = super(TemplateWizard, self).default_get(fields)

        active_id = self._context.get('active_id')
        active_model = self._context.get('active_model')
        res_users = self.env[active_model].browse(active_id)

        if res_users.groups_id.ids:
            rec['group_ids'] = res_users.groups_id.ids
        if res_users.sh_hm_hide_menu_ids.ids:
            rec['menu_ids'] = res_users.sh_hm_hide_menu_ids.ids

        return rec

    def create_template(self):

        self.env['sh.template'].create({
            'name': self.name,
            'group_ids': self.group_ids.ids,
            'menu_ids': self.menu_ids.ids,

        })
