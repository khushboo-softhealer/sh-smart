from odoo import fields, models

class TemplatesAllocationWizard(models.TransientModel):
    _name = 'sh.templates.allocation.wizard'
    _description = "Templates Allocation Wizard"

    template_ids = fields.Many2many('sh.template', string="Templates", required=True,)
    update_method = fields.Selection(
        [('add', 'Add'), ('replace', 'Replace')], default='add')
    user_ids = fields.Many2many('res.users')

    def action_templates_allocation_wizard(self):

        return{
            'name': 'Templates Allocation',
            'res_model': 'sh.templates.allocation.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('sh_user_group_allocation_hide_menu.sh_templates_allocation_wizard_view_form').id,
            'context': {'default_user_ids': [(6, 0, self.env.context.get('active_ids'))]},
            'target': 'new',
            'type': 'ir.actions.act_window'
        }

    def add_templates(self):
        if self.update_method == 'add':
            old_template_ids = self.user_ids.template_ids.ids
            print("\n\nBEFORE OLD IDS.........",old_template_ids)
            
            for template_id in self.template_ids.ids:
                if not template_id in old_template_ids:
                    old_template_ids.append(template_id)
            print("\n\nAFTER OLD IDS.........",old_template_ids)
            
            self.user_ids.write({
                'template_ids': [(6, 0, old_template_ids)]
            })

        if self.update_method == 'replace':
            self.user_ids.write({
                'template_ids': [(6, 0, self.template_ids.ids)]
            })
