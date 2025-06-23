from odoo import api, exceptions, fields, models, _

class GroupsAllocationWizard(models.TransientModel):
    _name = 'sh.groups.allocation.wizard'

    group_ids = fields.Many2many('res.groups',string="Groups",required=True,)
    update_method = fields.Selection([('add','Add'),('replace','Replace')],default='add')
    user_ids = fields.Many2many('res.users')

    def action_groups_allocation_wizard(self):

        return{
            'name': 'Groups Allocation',
            'res_model': 'sh.groups.allocation.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('sh_user_group_allocation_hide_menu.sh_groups_allocation_wizard_view_form').id,
            'context':{'default_user_ids':[(6,0,self.env.context.get('active_ids'))]},
            'target': 'new',
            'type': 'ir.actions.act_window'
        }
    
    def add_groups(self):
        if self.update_method == 'add':
            for group_id in self.group_ids:
                self.user_ids.write({
                'groups_id' : [(4,group_id.id)]
            })
        
        if self.update_method == 'replace':
            self.user_ids.write({
                'groups_id' : [(6,0,self.group_ids.ids)]
            })