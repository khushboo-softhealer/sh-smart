# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models
from datetime import datetime
from math import ceil


class CopyrightProject(models.Model):
    _inherit = 'project.project'

    def generate_scale_wise_data(self, products, scale, task, user):
        products_size = products.filtered(
            lambda x: x.sh_scale_ids.name == scale.name)
        today_limit = len(products_size)/scale.days
        today_limit = ceil(today_limit)
        if today_limit >= 1:
            domain = [('sh_scale_ids.name', '=', scale.name), ('claim_created',
                                                               '=', False), ('copyright_claim_user', '=', user.id)]
            product_list = self.env['product.template'].search(
                domain, limit=today_limit)
            if product_list:
                find_product_list = product_list
            else:
                domain = [('sh_scale_ids.name', '=', scale.name),
                          ('copyright_claim_user', '=', user.id)]
                new_list = self.env['product.template'].search(domain)
                for rec in new_list:
                    rec.write({'claim_created': False})
                domain = [('sh_scale_ids.name', '=', scale.name), ('claim_created',
                                                                   '=', False), ('copyright_claim_user', '=', user.id)]
                product_list = self.env['product.template'].search(
                    domain, limit=today_limit)
                if product_list:
                    find_product_list = product_list
            for data in find_product_list:
                claim_vals = {
                    'task_id': task.id,
                    'product_id': data.id,
                }
                self.env['sh.copyright.claim'].create(claim_vals)
                data.write({'claim_created': True})

    # def prepare_claim_data(self, month_task, day_wise_task, claim_project):
    #     find_user_products = self.env['product.template'].search(
    #         [('copyright_claim_user', '!=', False)])
    #     all_users = find_user_products.mapped('copyright_claim_user')
    #     for user in all_users:
    #         user_task = day_wise_task + ' (' + user.name + ')'
    #         domain = [('project_id', '=', claim_project.id),
    #                   ('parent_id', '=', month_task.id), ('name', '=', user_task)]
    #         find_today_task = self.env['project.task'].search(domain)
    #         if find_today_task:
    #             daily_task = find_today_task
    #         else:
    #             create_today_task = self.env['project.task'].create(
    #                 {'name': user_task, 'project_id': claim_project.id, 'parent_id': month_task.id, 'user_id': user.id})
    #             daily_task = create_today_task
    #             products = self.env['product.template'].search(
    #                 [('copyright_claim_user', '=', user.id)])
    #             product_scale_wise = products.mapped('sh_scale_ids')
    #             for scale in product_scale_wise:
    #                 self.generate_scale_wise_data(
    #                     products, scale, daily_task, user)

    # def create_copyright_project_tasks(self):
    #     claim_project = self.env.user.company_id.claim_project_id
    #     claim_users = self.env.user.company_id.claim_users
    #     current_month = datetime.now().strftime('%B')
    #     current_day = datetime.now().strftime('%d')
    #     day_wise_task = current_day + ' ' + current_month
    #     domain = [('project_id', '=', claim_project.id),
    #               ('name', '=', current_month)]
    #     find_month_task = self.env['project.task'].search(domain)
    #     if find_month_task:
    #         month_task = find_month_task
    #     else:
    #         create_month_task = self.env['project.task'].create(
    #             {'name': current_month, 'project_id': claim_project.id, 'user_ids': [(6, 0, claim_users.ids)]})
    #         if create_month_task:
    #             month_task = create_month_task
    #     self.prepare_claim_data(month_task, day_wise_task, claim_project)
