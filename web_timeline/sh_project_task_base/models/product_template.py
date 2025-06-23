# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, api
from odoo.exceptions import ValidationError

class product_template(models.Model):
    _inherit = 'product.template'

    @api.model
    def create_task(self):
        if not self.env.user.has_group('sh_project_task_base.group_create_task'):
            raise ValidationError(
                'You are not Authorised to perform this action !')

        for rec in self:

            version_attribute = self.env['product.attribute'].search([('name', 'ilike', 'Version')], limit=1)
            attribute_line_of_version=rec.attribute_line_ids.filtered(lambda x: x.attribute_id.id == version_attribute.id)

            listt=[]
            for version_attibute_value in attribute_line_of_version.value_ids:
                sh_version_value=self.env['sh.version'].search(
                    [('name', 'ilike', version_attibute_value.name)], limit=1)

                if sh_version_value:
                    listt.append(sh_version_value.id)
                else:
                    sh_version_value=self.env['sh.version'].create({
                        'name': version_attibute_value.name
                    })
                    listt.append(sh_version_value.id)
            
            responsible_ids_listt = []
            responsible_ids_listt.append(self.env.uid)
            if rec.resposible_user_id:
                responsible_ids_listt.append(rec.resposible_user_id.id)
            responsible_ids_listt.extend(rec.other_responsible_users.ids)

            if rec.sh_task_created==False:
                model_project_task=self.env['project.task'].sudo().create({
                    'name':rec.name,
                    'project_id': self.env.company.appstore_project_id.id,
                    'product_template_id' : rec.id,
                    'user_ids':[(6,0,responsible_ids_listt)],
                    'version_ids': [(6, 0, listt)],
                    'sh_technical_name':rec.sh_technical_name,
                    'depends': [(6, 0, rec.depends.ids)],
                    'license':rec.license.id,
                    'product_version':rec.product_version,
                    'supported_browsers':[(6, 0,rec.supported_browsers.ids)],
                    'released_date' : rec.released_date,
                    'last_updated_date' : rec.last_updated_date,
                    'live_demo' : rec.live_demo,
                    'user_guide' : rec.user_guide,
                    'sh_tag_ids' : [(6, 0,rec.tag_ids.ids)],
                    'sh_edition_ids':[(6, 0,rec.sh_edition_ids.ids)],
                    'sh_scale_ids' : rec.sh_scale_ids.id,
                    'banner':rec.banner,
                    'related_video':[(6,0,rec.related_video.ids)],
                    'sh_blog_post_ids':[(6,0,rec.sh_blog_post_ids.ids)],
                })

                rec.write({
                    'related_task': model_project_task.id,
                    'sh_task_created':True
                })
                if self.env.user.company_id.done_project_stage_id:
                    model_project_task.write({'stage_id':self.env.user.company_id.done_project_stage_id.id})

            if attribute_line_of_version:
                for version_attibute_value in attribute_line_of_version.value_ids:
                    variant = rec.product_variant_ids.filtered(lambda x:x.product_template_attribute_value_ids.name in [version_attibute_value.name])
                    sh_version_value=self.env['sh.version'].search(
                        [('name', 'ilike', version_attibute_value.name)], limit=1)

                    listt = []
                    if sh_version_value:
                        listt.append(sh_version_value.id)
                    else:
                        sh_version_value=self.env['sh.version'].create({
                            'name': version_attibute_value.name
                        })
                        listt.append(sh_version_value.id)
                    if variant and not variant.related_sub_task:
                    # if variant and variant.sh_sub_task_created == False:

                        responsible_ids_listt = []
                        responsible_ids_listt.append(self.env.uid)
                        if rec.resposible_user_id:
                            responsible_ids_listt.append(rec.resposible_user_id.id)
                        responsible_ids_listt.extend(variant.other_responsible_users.ids)

                        sub_task_id = self.env['project.task'].sudo().create({
                            'name': version_attibute_value.name+'/'+rec.name,
                            'project_id': self.env.company.appstore_project_id.id,
                            'display_project_id': self.env.company.appstore_project_id.id,
                            'parent_id': rec.related_task.id,
                            'user_ids':[(6,0,responsible_ids_listt)],
                            'version_ids': [(6, 0, listt)],
                            'sh_technical_name':variant.sh_technical_name,
                            'depends': [(6, 0, variant.depends.ids)],
                            'license':variant.license.id,
                            'product_version':variant.product_version,
                            'supported_browsers':[(6, 0,variant.supported_browsers.ids)],
                            'released_date' : variant.released_date,
                            'last_updated_date' : variant.last_updated_date,
                            'live_demo' : variant.live_demo,
                            'user_guide' : variant.user_guide,
                            'sh_tag_ids' : [(6, 0,variant.tag_ids.ids)],
                            'sh_edition_ids':[(6, 0,variant.sh_edition_ids.ids)],
                            'banner':variant.banner,
                            'related_video':[(6,0,variant.related_video.ids)],
                            'sh_blog_post_ids':[(6,0,variant.sh_blog_post_ids.ids)],
                        })

                        if variant.product_variant_change_log_id:
                            for log in variant.product_variant_change_log_id:
                                self.env['product.change.log'].sudo().create({
                                    'project_task_id': sub_task_id.id,
                                    'version':log.version,
                                    'date':log.date,
                                    'log_type':log.log_type,
                                    'details':log.details
                                    })

                        sub_task_id.write({ 'sh_product_id':variant.id })

                        if self.env.user.company_id.done_project_stage_id:
                            sub_task_id.write({'stage_id':self.env.user.company_id.done_project_stage_id.id})

                        if variant:
                            variant.sudo().write({'sh_sub_task_created':True,
                                'related_sub_task':sub_task_id.id})

