# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class ManageAgenda(models.Model):
    _name = "sh.manage.agenda"
    _description = "Manage Agenda"

    name = fields.Char("Talking Point",required=True)
    sh_is_active = fields.Boolean("Active")
    sh_agenda_description = fields.Char("Agenda Description")


    def unlink(self):
        for record in self:
            agenda_line_ids = self.env['sh.talking.agenda.line'].search([('sh_agenda_id', '=' ,record.id)])
            if agenda_line_ids :
                agenda_line_ids.unlink()

        ret = super(ManageAgenda, self).unlink()
        return ret
