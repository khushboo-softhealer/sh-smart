# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, _


class ProjectMgmtPartner(models.Model):
    _inherit = 'res.partner'

    sh_project_mgmt_customer_type = fields.Selection([
        ('b2b', 'B2B (Business-to-Business)'),
        ('b2c', 'B2C (Business-to-Consumer)'),
        ('unknown', 'Unknown'),
    ], string='Customer Type', default='unknown')

    sh_project_count = fields.Integer('Project Count', compute='_compute_sh_project_count')

    def _compute_sh_project_count(self):
        for partner in self:
            partner.sh_project_count = self.env['project.project'].search_count([
                ('partner_id', '=', partner.id)
            ])

    def show_customer_projects(self):
        self.ensure_one()
        return_view = {
            'name': _('Project'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'project.project',
            'target': 'current',
            'domain': [('partner_id' ,'=', self.id)],
            'context': {
                'create': False,
                'delete': False
            }
        }
        if self.sh_project_count == 1:
            view = self.env.ref('project.edit_project')
            return_view['view_id'] = view.id
            return_view['view_mode'] = 'form'
            project_id = self.env['project.project'].search([
                ('partner_id', '=', self.id)
            ])
            return_view['res_id'] = project_id.id
            return_view['views'] = [(view.id, 'form')]
        return return_view
