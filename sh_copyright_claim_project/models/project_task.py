# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = "project.task"

    claim_ids = fields.One2many(comodel_name='sh.copyright.claim',
                                inverse_name='task_id',
                                string='Claim')
    claim = fields.Boolean(string=' Claim',
                           compute="_compute_claim",
                           default=False)

    @api.depends('company_id')
    def _compute_claim(self):
        for rec in self:
            if rec.project_id.id == rec.company_id.claim_project_id.id:
                rec.claim = True
            else:
                rec.claim = False

    def mass_print_project_claim(self):
        if self.env.user.has_group('sh_copyright_claim_project.group_project_user'):
            return {
                'name': 'Print Copyright Claim Reports',
                'res_model': 'sh.copyright.claim.wizard',
                'view_mode': 'form',
                'view_id': self.env.ref('sh_copyright_claim_project.sh_claim_wizard_view').id,
                'target': 'new',
                'type': 'ir.actions.act_window',
                'context': {'default_task_ids': [(6, 0, self.env.context.get('active_ids'))]}
            }
        else:
            raise ValidationError(
                'You are not Authorised to perform this action !')
