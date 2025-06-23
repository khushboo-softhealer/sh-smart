# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models, api
from odoo import Command

class UpdatemassTag(models.TransientModel):
    _name = "sh.project.stage.mass.update.wizard"
    _description = "Mass Update Wizard"

    project_project_ids = fields.Many2many("project.project")
    update_stage = fields.Many2many('project.task.type', string="Stages")
    update_stage_method = fields.Selection([
        ("add", "Add"),
        ("replace", "Replace"),
    ], string='Stage Update Method')

    responsible_user_update_method = fields.Selection([
        ("add", "Add"),
        ("replace", "Replace"),
        ("remove", "Remove"),
    ], string='Responsible User Update Method')
    responsible_user_ids = fields.Many2many('res.users', string="Responsible Users")
    
    sh_pricing_mode = fields.Selection([
        ('fp', 'FP - Fixed Price'),
        ('tm', 'T&M - Time and Material'),
    ], string="Pricing Model")
    
    sh_fp_based_on = fields.Selection([
        ('no_milestone', 'No Milestone - One shot'),
        ('milestone', 'Implementation Project'),
    ], string='FP Based On')
    
    sh_tm_based_on = fields.Selection([
            ('success_pack', 'Success Packs Based'),
            ('billable', 'Billable Hours Based'),
        ], string='T&M Based On',)
    
    odoo_version = fields.Many2one(comodel_name="sh.version", string="Version")
    sh_edition_id = fields.Many2one(comodel_name="sh.edition", string="Edition")
    date_start = fields.Date(string="Start Date")
    end_date = fields.Date(string="Expiration/End Date")
    project_type_selection = fields.Selection([("internal", "Internal"),("external", "External")],string="Project Type")
    
    def update_record(self):
        if self.update_stage_method:
            if self.update_stage_method == 'add':
                for i in self.update_stage:
                    self.project_project_ids.write({'sh_stage_ids': [(4, i.id)]})
            if self.update_stage_method == 'replace':
                self.project_project_ids.write(
                    {'sh_stage_ids': [(6, 0, self.update_stage.ids)]})
        
        if self.responsible_user_update_method:
            if self.responsible_user_update_method == 'add':
                for i in self.responsible_user_ids:
                    self.project_project_ids.write({'responsible_user_ids': [(4, i.id)]})
            if self.responsible_user_update_method == 'replace':
                self.project_project_ids.write(
                    {'responsible_user_ids': [(6, 0, self.responsible_user_ids.ids)]})
            if self.responsible_user_update_method == 'remove':
                self.project_project_ids.write({'responsible_user_ids': [Command.unlink(id) for id in self.responsible_user_ids.ids]})
        
        vals = {}
        if self.sh_pricing_mode:
            vals.update({'sh_pricing_mode': self.sh_pricing_mode})

        if self.sh_fp_based_on:
            vals.update({'sh_fp_based_on': self.sh_fp_based_on})
        
        if self.sh_tm_based_on:
            vals.update({'sh_tm_based_on': self.sh_tm_based_on})
        
        if self.odoo_version:
            vals.update({'odoo_version': self.odoo_version.id})
        
        if self.sh_edition_id:
            vals.update({'sh_edition_id': self.sh_edition_id.id})
        
        if self.date_start:
            vals.update({'date_start': self.date_start})
        
        if self.end_date:
            vals.update({'date': self.end_date})
        
        if self.project_type_selection:
            vals.update({'project_type_selection': self.project_type_selection})

        if vals:
            self.project_project_ids.write(vals)