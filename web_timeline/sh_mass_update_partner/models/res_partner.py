# Part of Softhealer Technologies.
from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def action_mass_pricelist_update(self):
        return {
            'name':
            'Mass Update',
            'res_model':
            'sh.res.partner.mass.update.wizard',
            'view_mode':
            'form',
            'context': {
                'default_all_res_partner_ids':
                [(6, 0, self.env.context.get('active_ids'))]
            },
            'view_id':
            self.env.ref(
                'sh_mass_update_partner.sh_res_partner_update_wizard_form_view').
            id,
            'target':
            'new',
            'type':
            'ir.actions.act_window'
        }
