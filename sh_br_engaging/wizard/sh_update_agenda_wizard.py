# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import _, api, fields, models

class UpdateAgenda(models.TransientModel):
    _name = "sh.update.agenda.wizard"
    _description = "Model for Update Agenda List in Talking Points"

    name = fields.Char("Talking Point",required=True)
    sh_talking_point_id=fields.Many2one('sh.talking.points','Talking Point Id')

    def update_agenda_record(self):
        if self.sh_talking_point_id:
            new_agenda=self.env['sh.manage.agenda'].create({
                'name': self.name
            })
            if new_agenda:
                line_vals={
                    'sh_agenda_id':new_agenda.id,
                    'sh_talking_point_id':self.sh_talking_point_id.id,
                }
                self.env['sh.talking.agenda.line'].create(line_vals)

        return {'type': 'ir.actions.client', 'tag': 'soft_reload'}