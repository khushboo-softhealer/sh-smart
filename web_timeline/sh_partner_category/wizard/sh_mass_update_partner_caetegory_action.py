# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields


class MassActionPartnerCategory(models.TransientModel):
    _name = 'sh.partner.category.action.wizard'
    _description = "Wizard for Change Partner Category"

    sh_partner_category_id = fields.Many2one(
        'partner.category', string='Partner Category')
    sh_partners = fields.Many2many('res.partner')

    def update_partner_category(self):
        if self.sh_partners:
            dic = {}
            for partner in self.sh_partners:
                dic[partner.id] = partner.partner_category_id.name
            if len(self.sh_partners) > 1:
                if self.sh_partner_category_id.id:
                    self.env.cr.execute("""UPDATE RES_PARTNER SET partner_category_id ='%s' WHERE id IN %s""" % (
                        self.sh_partner_category_id.id, tuple(self.sh_partners.ids)))
                else:
                    for partner in self.sh_partners:
                        self.env.cr.execute(
                            """UPDATE RES_PARTNER SET partner_category_id =null WHERE id = %s""" % partner.id)
            else:
                if self.sh_partner_category_id.id:
                    self.env.cr.execute("""UPDATE RES_PARTNER SET partner_category_id ='%s' WHERE id = %s""" % (
                        self.sh_partner_category_id.id, self.sh_partners.id))
                else:
                    self.env.cr.execute(
                        """UPDATE RES_PARTNER SET partner_category_id =null WHERE id = %s""" % self.sh_partners.id)
        for partner in self.sh_partners:
            self.env['mail.message'].sudo().create({
                'subject': 'Partner Category Changed',
                'date': fields.Datetime.now(),
                'author_id': self.env.user.partner_id.id,
                'message_type': 'notification',
                'subtype_id': self.env.ref('mail.mt_note').id,
                'model': 'res.partner',
                'res_id': partner.id,
                'tracking_value_ids': [(0, 0, {
                    'field': self.sh_partner_category_id.id,
                    'field_desc': 'Partner Category',
                    'old_value_char': dic[partner.id],
                    'new_value_char': self.sh_partner_category_id.name,
                })]
            })
