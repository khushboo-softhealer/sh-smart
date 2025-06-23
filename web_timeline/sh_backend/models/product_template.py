# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models, api
from odoo.tools.translate import html_translate
from odoo.exceptions import ValidationError
from datetime import timedelta, datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

class product_template(models.Model):
    _inherit = 'product.template'

    # resposible_user_id=fields.Many2one('res.users',string="Assign To")
    # other_responsible_users = fields.Many2many('res.users',string = "Other Responsible Users")
    # sh_task_created = fields.Boolean(string="Task created", copy=False)
    # related_task=fields.Many2one('project.task',string="Relatd Task",copy=False)
    # copyright_claim_user = fields.Many2one('res.users',"Copyright Claim User")
    # individual_modules = fields.Many2many('product.template','template_individual_all_in_one_rel','individual_id','all_in_one_id',string = "Individual Modules")

    # ========= added =====================

    # def get_product_image_ids(self):
    #     return {
    #         "type": "ir.actions.act_window",
    #         "name": "Images",
    #         "view_mode": "kanban,tree,form",
    #         "res_model": "product.image",
    #         "domain": [("product_tmpl_id", "=", self.id)],
    #     }

    @api.model
    def add_variants(self,sh_version):
        if not sh_version:
            return '\nPlease provide the versions !\n'
        # if self.env.user.has_group('sh_backend.group_variant_creation'):
        message = ''
        version_added_count = 0
        already_has = 0
        for tmpl in self:
            try:
                version_attribute = self.env['product.attribute'].search(
                    [('name', 'ilike', 'Version')], limit=1)

                if not version_attribute:
                    version_attribute = self.env['product.attribute'].create({
                        'name': 'Version'
                    })

                related_line = tmpl.attribute_line_ids.filtered(lambda x: x.attribute_id.id == version_attribute.id)
                # if not tmpl.attribute_line_ids.filtered(lambda x: x.attribute_id.id == version_attribute.id):
                if not related_line:
                    # if sh_version:
                    # attribute list value list
                    version_value_list = []
                    version_name_list = []
                    for version in sh_version:
                        version_name_list.append(version.name)
                        attr_value = self.env['product.attribute.value'].search(
                            [('name', 'ilike', version.name)], limit=1)
                        if attr_value:
                            version_value_list.append(attr_value.id)
                        else:
                            version_attr_value = self.env['product.attribute.value'].create({
                                'name': version.name,
                                'attribute_id': version_attribute.id
                            })
                            version_value_list.append(version_attr_value.id)

                    if version_attribute:
                        dictt = []
                        attributs = {
                            'attribute_id': version_attribute.id,
                            'value_ids': [(6, 0, version_value_list)]
                        }
                        dictt.append((0, 0, attributs))
                        tmpl.update({
                            'attribute_line_ids': dictt
                        })
                        version_added_count += 1
                else:
                    # if sh_version:
                    # attribute list value list
                    # version_value_list = []
                    for version in sh_version:
                        attr_value = self.env['product.attribute.value'].search(
                            [('name', 'ilike', version.name)], limit=1)
                        if not attr_value:
                            attr_value = self.env['product.attribute.value'].create({
                                'name': version.name,
                                'attribute_id': version_attribute.id
                            })
                        if attr_value.id not in tmpl.attribute_line_ids.mapped('value_ids').ids:
                            if related_line:
                                related_line.write(
                                    {'value_ids': [(4, attr_value.id)]})
                                version_added_count += 1
                        else:
                            already_has += 1
            except Exception as e:
                message += f'Error for {tmpl.sh_technical_name}: {e}\n'
        # else:
        #     raise ValidationError('You are not Authorised to perform this action !' )
        version_name = ' '
        if len(sh_version) == 1:
            version_name = f' {sh_version.name} '
        if version_added_count:
            message += f'Version{version_name}added in the {version_added_count} templates.\n'
        if already_has:
            message += f'Version{version_name}already contains in the {already_has} templates.\n'
        return message

    # @api.multi
    @api.model
    def update_responsible_user(self):

        if self.env.user.has_group('sh_backend.group_update_res_user'):
           return {
               'name': 'Responsible User',
               'res_model': 'sh.res.user.wizard',
               'view_mode': 'form',
               'view_id': self.env.ref('sh_backend.res_user_wizard_form').id,
               'target': 'new',
               'type': 'ir.actions.act_window',
               'context': {'default_product_ids': [(6, 0, self.env.context.get('active_ids'))]}
           }
        else:
            raise ValidationError('You are not Authorised to perform this action !')

    # @api.multi
    @api.model
    def update_technical_name(self):
        for rec in self:
            if len(rec.product_variant_ids) > 0:
                rec.write({
                            'sh_technical_name': rec.product_variant_ids[0].sh_technical_name,
                        })

    # @api.multi
    @api.model
    def assign_mass_edition(self):
        if self.env.user.has_group('sh_backend.group_assign_edition'):
            return {
                'name': 'Assign Editions',
                'res_model': 'sh.assign.edition.wizard',
                'view_mode': 'form',
                'view_id': self.env.ref('sh_backend.mass_assign_edition_wizard_form').id,
                'target': 'new',
                'type': 'ir.actions.act_window',
                'context': {'default_product_ids': [(6, 0, self.env.context.get('active_ids'))]}
            }
        else:
            raise ValidationError('You are not Authorised to perform this action !')

    # @api.multi
    @api.model
    def assign_mass_scale(self):
        if self.env.user.has_group('sh_backend.group_assign_scale'):
            return {
                'name':'Assign Product Scale',
                'res_model':'sh.assign.scale.wizard',
                'view_mode':'form',
                'view_id': self.env.ref('sh_backend.mass_assign_scale_wizard_form').id,
                'target':'new',
                'type':'ir.actions.act_window',
                'context':{'default_product_ids':[(6,0,self.env.context.get('active_ids'))]}
            }
        else:
            raise ValidationError('You are not Authorised to perform this action !')

    # @api.multi
    @api.model
    def mass_update_category(self):
        if self.env.user.has_group('sh_product_base.group_product_tags_manager'):
            return {
                'name':'Mass Update Product Category',
                'res_model':'sh.update.category.wizard',
                'view_mode':'form',
                'view_id': self.env.ref('sh_backend.mass_update_product_category_form').id,
                'target':'new',
                'type':'ir.actions.act_window',
                'context':{'default_product_ids':[(6,0,self.env.context.get('active_ids'))]}
            }
        else:
            raise ValidationError('You are not Authorised to perform this action !')

    # @api.multi
    @api.model
    def mass_update_ecommerce_category(self):
        if self.env.user.has_group('sh_product_base.group_product_tags_manager'):
            return {
                'name':'Mass Update Product Ecommerce Category',
                'res_model':'sh.update.ecommerce.category.wizard',
                'view_mode':'form',
                'view_id': self.env.ref('sh_backend.mass_update_product_ecommerce_category_form').id,
                'target':'new',
                'type':'ir.actions.act_window',
                'context':{'default_product_ids':[(6,0,self.env.context.get('active_ids'))]}
            }
        else:
            raise ValidationError('You are not Authorised to perform this action !')

    # @api.multi
    @api.model
    def mass_update_product_type(self):
        if self.env.user.has_group('sh_product_base.group_product_tags_manager'):
            return {
                'name':'Mass Update Product Type',
                'res_model':'sh.update.product.type.wizard',
                'view_mode':'form',
                'view_id': self.env.ref('sh_backend.mass_update_product_type_form').id,
                'target':'new',
                'type':'ir.actions.act_window',
                'context':{'default_product_ids':[(6,0,self.env.context.get('active_ids'))]}
            }
        else:
            raise ValidationError('You are not Authorised to perform this action !')


##################################################################################

    #=============== added
    # not_unique_product = fields.Boolean("Not Unique")
    # git_repo = fields.Many2one('sh.git.repo',string="Git Repo", track_visibility='onchange')

    # scheduler for Update Module
    @api.model
    def notify_module_update(self):
        products = self.env["product.template"].search([])

        for product in products:
            if product.module_last_updated_date and product.sh_scale_ids and product.related_task :

                update_date = datetime.strptime(str(product.module_last_updated_date), DEFAULT_SERVER_DATE_FORMAT).date(
                            ) + timedelta(days=product.sh_scale_ids.days)
                if update_date <= datetime.now().date():
                    if product.related_task.stage_id == product.company_id.done_project_stage_id and product.related_task.stage_id != product.company_id.to_be_project_stage_id :
                        product.related_task.write({'stage_id':product.company_id.to_be_project_stage_id.id})

    # @api.multi
    @api.model
    def add_new_version(self):
        return {
                'name':'Add New Versions',
                'res_model':'sh.assign.new.version.wizard',
                'view_mode':'form',
                'view_id': self.env.ref('sh_backend.sh_assign_new_version_wizard_form').id,
                'target':'new',
                'type':'ir.actions.act_window',
                'context':{'default_product_ids':[(6,0,self.env.context.get('active_ids'))]}
            }

    # @api.multi
    @api.model
    def update_responsible_user_in_task(self):
        active_product_ids = self.env['product.template'].browse(self.env.context.get('active_ids'))
        for data in active_product_ids:
            if data.related_task:
                task = data.related_task
                task.write({"user_ids":(4,data.resposible_user_id.id)})
                for sub_task in task.child_ids:
                    sub_task.write({"user_ids":(4,data.resposible_user_id.id)})

    # def write(self,vals):
        # res = super(product_template, self).write(vals)
        # for rec in self:
        #     if 'resposible_user_id' in vals:
        #         new_id = vals['resposible_user_id']
        #         if rec.related_task:
        #             rec.related_task.sudo().user_ids = [(4,self.env.uid)]
        #         if rec.related_task.sudo().child_ids:
        #             for task in rec.related_task.sudo().child_ids:
        #                 task.sudo().user_ids = [(4,self.env.uid)]

        #     if 'other_responsible_users' in vals:
        #         responsible_ids = vals['other_responsible_users'][0]
        #         for resposible in responsible_ids:
        #             if rec.related_task:
        #                 rec.related_task.sudo().user_ids = [(4,resposible)]
        #             if rec.related_task.sudo().child_ids:
        #                 for task in rec.related_task.sudo().child_ids:
        #                     task.sudo().user_ids = [(4,resposible)]
        # return res

    @api.model
    def update_git_repo_product(self):
        return {
                'name':'Update Git Repo',
                'res_model':'sh.update.git.repo.wizard',
                'view_mode':'form',
                'view_id': self.env.ref('sh_backend.sh_update_git_repo_wizard_form').id,
                'target':'new',
                'type':'ir.actions.act_window',
                'context':{'default_product_ids':[(6,0,self.env.context.get('active_ids'))]}
            }


    sh_has_current_version = fields.Boolean('Has Current Version')
    sh_has_current_version_compute = fields.Boolean('Has Current Version Compute', compute='_compute_sh_has_current_version_compute')

    @api.depends('attribute_line_ids')
    def _compute_sh_has_current_version_compute(self):
        for tmpl in self:
            tmpl.sh_has_current_version_compute = False
            if not tmpl.attribute_line_ids:
                continue
            for line in tmpl.attribute_line_ids:
                if not line.attribute_id.name == 'Version':
                    continue
                for version in line.value_ids:
                    if version.name == 'Odoo 17':
                        tmpl.write({
                            'sh_has_current_version': True
                        })
                        tmpl.sh_has_current_version_compute = True
                        break
