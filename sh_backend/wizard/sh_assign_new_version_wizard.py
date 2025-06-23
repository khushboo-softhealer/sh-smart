# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields

class NewVersion(models.TransientModel):
    _name = 'sh.assign.new.version.wizard'
    _description = 'Mass Assign Wizard'

    version_ids  = fields.Many2many('sh.version', string="Versions", required=True,)
    product_ids = fields.Many2many('product.template')

    def assign_new_versions(self):
        message = ''
        already_has_task = 0
        parent_task_not_found_list = []
        created_task_list = []
        for version in self.version_ids:
            var_message = self.product_ids.add_variants(version)
            if var_message:
                message += var_message
            for tmpl in self.product_ids:
                # domain = [('product_tmpl_id', '=', tmpl.id)]
                # all_variant = self.env['product.product'].search(domain,limit=2,order = "id desc")
                # for variant in all_variant:
                #     if version.name != variant.name:
                #         product = variant

                for variant in tmpl.product_variant_ids:
                    # for rec in variant.attribute_value_ids:
                    for rec in variant.product_template_attribute_value_ids:
                        if version.name != rec.name:
                            continue
                        # product = variant
                        # vva= {
                        #     'sh_technical_name' : product.sh_technical_name if product.sh_technical_name else '',
                        #     'banner' : product.banner,
                        #     'sh_edition_ids' :[(6,0,product.sh_edition_ids.ids)] if product.sh_edition_ids else False,
                        #     'depends' :[(6,0,product.depends.ids)]  if product.depends else False,
                        #     'required_apps' : [(6,0,product.required_apps.ids)] if product.required_apps else False,
                        #     'license' : product.license.id if product.license else False,
                        #     'product_version' : product.product_version if product.product_version else False,
                        #     'supported_browsers' : product.supported_browsers if product.supported_browsers else False,
                        #     'released_date' : product.released_date if product.released_date else False,
                        #     'last_updated_date' : product.last_updated_date if product.last_updated_date else False,
                        #     'live_demo' : product.live_demo if product.live_demo else False,
                        #     'user_guide' : product.user_guide if product.user_guide else False,
                        #     'related_video' : [(6,0,product.related_video.ids)] if product.related_video else False,
                        #     'sh_blog_post_ids' : [(6,0,product.sh_blog_post_ids.ids)] if product.sh_blog_post_ids else False,
                        #     'tag_ids' : [(6,0,product.tag_ids.ids)] if product.tag_ids else False,
                        #     'qty_show' : product.qty_show if product.qty_show else False,
                        #     'resposible_user_id' : product.resposible_user_id.id if product.resposible_user_id else False,
                        #     'sh_scale_ids' : product.sh_scale_ids.id if product.sh_scale_ids else False,
                        # }
                        # tmpl.sudo().write(vva)
                        # domain = [('name', '=', product.name)]
                        # If product has related task
                        find_parent = tmpl.related_task
                        if not find_parent:
                            # If product tmpl linked any of the task
                            find_parent = self.env['project.task'].search([
                                ('product_template_id', '=', tmpl.id),
                                ('parent_id', 'in', (False, None, ''))
                            ],limit=1)
                            if not find_parent:
                                # If product tmpl name matched any of the task
                                find_parent = self.env['project.task'].search([
                                    ('name', '=', tmpl.name),
                                    ('parent_id', 'in', (False, None, ''))
                                ], limit=1)
                                if not find_parent:
                                    parent_task_not_found_list.append(tmpl.sh_technical_name or tmpl.name)
                                    continue
                                if find_parent.product_template_id:
                                    if find_parent.product_template_id.id != tmpl.id:
                                        message += f'{find_parent.name} parent task find using name but it linked with the different tmpl !\n'
                                        continue
                                else:
                                    # Linked the tmpl with task
                                    find_parent.sudo().write({
                                        'product_template_id': tmpl.id
                                    })
                            # Link the task with tmpl
                            if find_parent:
                                tmpl.sudo().write({
                                    'related_task': find_parent.id
                                })
                        if version.id in find_parent.version_ids.ids:
                            already_has_task += 1
                            if find_parent.child_ids:
                                for child_task in find_parent.child_ids:
                                    if child_task.version_ids and len(child_task.version_ids) == 1:
                                        if version.id == child_task.version_ids[0].id:
                                            if child_task.project_id.id == self.env.company.appstore_project_id.id:
                                                child_task.sudo().write({
                                                    'project_id': self.env.company.appstore_project_id.id,
                                                    'version_ids': [(6, 0, [version.id])]
                                                })
                            # message += f'\nTemplate: {tmpl.name}:\nTask already exist !\n'
                            continue
                        find_child_task = False
                        for child_task in find_parent.child_ids:
                            if child_task.version_ids:
                                if version.id in child_task.version_ids.ids:
                                    find_child_task = True
                                    break
                        if find_child_task:
                            continue
                        # sh_version_value=self.env['sh.version'].search([('name', 'ilike', rec.name)], limit=1)
                        sh_version_value=version
                        listt = []
                        if sh_version_value:
                            listt.append(sh_version_value.id)
                        # if find_parent:
                        find_parent.sudo().write({'version_ids': [(4, sh_version_value.id)]})
                        task_vals = {
                            'name': rec.name+'/'+tmpl.name,
                            'project_id': self.env.company.appstore_project_id.id,
                            'parent_id': find_parent.id,
                            'user_ids':[(4, tmpl.resposible_user_id.id)],
                            'version_ids': [(6, 0, listt)],
                            'sh_technical_name': tmpl.sh_technical_name,
                            'depends': [(6, 0, tmpl.depends.ids)],
                            'license':tmpl.license.id,
                            'product_version':tmpl.product_version,
                            'supported_browsers':[(6, 0,tmpl.supported_browsers.ids)],
                            'released_date' : tmpl.released_date,
                            'last_updated_date' : tmpl.last_updated_date,
                            'live_demo' : tmpl.live_demo,
                            'user_guide' : tmpl.user_guide,
                            'sh_tag_ids' : [(6, 0,tmpl.tag_ids.ids)],
                            'sh_edition_ids':[(6, 0,tmpl.sh_edition_ids.ids)],
                            'banner':tmpl.banner,
                            'related_video':[(6,0,tmpl.related_video.ids)],
                            'sh_blog_post_ids':[(6,0,tmpl.sh_blog_post_ids.ids)],
                            'sh_product_id': variant.id
                        }
                        sub_task_id = self.env['project.task'].sudo().create(task_vals)
                        variant.sudo().write({'sh_sub_task_created':True,
                            'related_sub_task':sub_task_id.id})
                        created_task_list.append(tmpl.sh_technical_name)
        if already_has_task:
            message += f'\nAlready has task: {already_has_task}\n'
        if created_task_list:
            # message += f'\nTask created for {len(created_task_list)} templates:\n{created_task_list}\n'
            message += f'\nTask created for {len(created_task_list)} templates.\n'
        if parent_task_not_found_list:
            message += f'\nFaild to find parent task for {len(parent_task_not_found_list)} templates:\n{parent_task_not_found_list}\n'

        view = self.env.ref('sh_message.sh_message_wizard')
        context = dict(self._context or {})
        context['message'] = message
        return {
            'name': 'Add Version & Task',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sh.message.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': context
        }
