# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.


from odoo import models, fields , api , _

class Saleordertemplate(models.Model):
    _inherit = 'sale.order.template'

    project_manager = fields.Many2one("res.users",string="Project Manager",default=lambda self:self.env.user, required=True,domain=[('share', '=', False)])


    responsible_user_id = fields.Many2one("res.users", string="Technical Head",domain=[('share', '=', False)])

    sh_project_stage_tmpl_id = fields.Many2one(
        'sh.project.project.stage.template',
        string='Project Stage Template',required=True)

    sh_pricing_mode = fields.Selection([
        ('fp', 'FP - Fixed Price'),
        ('tm', 'T&M - Time and Material'),
    ], string="Pricing Model", required=True)

    sh_fp_based_on = fields.Selection([
        ('no_milestone', 'No Milestone - One shot'),
        ('milestone', 'Milestone Based'),
    ], string='FP Based On', required=True)

    sh_tm_based_on = fields.Selection([
        ('success_pack', 'Success Packs Based'),
        ('billable', 'Billable Hours Based'),
    ], string='T&M Based On',
        help='Success Packs Based (Renewable required based on usage) - SO\nBillable Hours Based (Monthly billable invoice created) - MANUALLY'
    )
    sh_total_work_duration = fields.Integer('Total Work Duration (Days)', required=True)

    @api.onchange('sh_project_stage_tmpl_id')
    def onchange_project_stage_template(self):
        self.ensure_one()
        if self.sh_project_stage_tmpl_id:
            if self.sh_project_stage_tmpl_id.sh_pricing_mode:
                self.sh_pricing_mode=self.sh_project_stage_tmpl_id.sh_pricing_mode
            if self.sh_project_stage_tmpl_id.sh_fp_based_on:
                self.sh_fp_based_on=self.sh_project_stage_tmpl_id.sh_fp_based_on
        