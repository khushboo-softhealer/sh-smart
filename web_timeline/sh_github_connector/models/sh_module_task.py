# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models
from datetime import datetime


class ShModuleIndex(models.Model):
    _inherit = "sh.module"

    # ------------------------------------------
    #  Create Activity If Not Link Task
    # ------------------------------------------

    def _check_for_activity(self, connector_obj, product):
        if not product.related_sub_task:
            connector_obj._generate_activity('product.product', product, 'Github Connector: Failed to find appstore task using tech name and version !')
        if not product.product_tmpl_id.related_task:
            connector_obj._generate_activity('product.template', product.product_tmpl_id, 'Github Connector: Failed to find appstore task using tech name and version !')

    # ------------------------------------------
    #  Link Product <-> Task
    # ------------------------------------------

    def _link_product_task(self, connector_obj, product, link_tmpl_task=False):
        ''' Linked the newly created product and template with the task '''
        if not connector_obj.appstore_project_id:
            return
        tasks = self.env['project.task'].sudo().search([
            ('project_id', '=', connector_obj.appstore_project_id.id),
            ('sh_technical_name', '=', product.sh_technical_name)
        ])
        if not tasks:
            # Create an activity
            self._check_for_activity(connector_obj, product)
            return
        version = self.sh_branch_id.name.split('.')[0]
        if len(tasks) == 1:
            if not tasks.version_ids:
                self._check_for_activity(connector_obj, product)
                return
            if len(tasks.version_ids) > 1:
                # parent task
                if link_tmpl_task:
                    product.product_tmpl_id.sudo().write({
                        'related_task': tasks.id
                    })
                    tasks.sudo().write({
                        'product_template_id': product.product_tmpl_id.id
                    })
                    link_tmpl_task = False
            else:
                # child task
                if version in tasks.version_ids[0].name:
                    product.sudo().write({
                        'related_sub_task': tasks.id
                    })
                    tasks.sudo().write({
                        'sh_product_id': product.id
                    })
        else:
            is_task_linked = False
            for task in tasks:
                if is_task_linked and not link_tmpl_task:
                    break
                if not task.version_ids:
                    continue
                if len(task.version_ids) > 1:
                    # parent task
                    if not link_tmpl_task:
                        continue
                    product.product_tmpl_id.sudo().write({
                        'related_task': task.id
                    })
                    task.sudo().write({
                        'product_template_id': product.product_tmpl_id.id
                    })
                    link_tmpl_task = False
                else:
                    # child task
                    if version in task.version_ids[0].name:
                        product.sudo().write({
                            'related_sub_task': task.id
                        })
                        task.sudo().write({
                            'sh_product_id': product.id
                        })
                        is_task_linked = True
        self._check_for_activity(connector_obj, product)

    # ====================================================
    #  Create Parent Task
    # ====================================================

    def create_parent_task(self, version_name, connector_obj):
        find_version = self.env["sh.version"].sudo().search(
            [("name", "=", version_name)], limit=1)
        # ======== Create Parent Task ========
        parent_task = self.env["project.task"].sudo().create({
            "name": self.sh_product_id.name,
            "product_template_id": self.sh_product_id.product_tmpl_id.id,
            "project_id": connector_obj.appstore_project_id.id,
            "user_ids": [(4, self.sh_product_id.git_repo.responsible_user.id)],
            'sh_technical_name': self.sh_product_id.sh_technical_name,
        })
        # ======= Task Version Ids =======
        if not find_version:
            find_version = self.env["sh.version"].sudo().create(
                {"name": version_name})
        parent_task.sudo().write({"version_ids": [(4, find_version.id)]})
        return parent_task

    # ====================================================
    #  Create/Update Task
    # ====================================================
    def process_module_task(self, connector_obj):
        task_obj = self.env["project.task"]
        version = self.sh_branch_id.name.split(".")[0]
        vals = {"user_ids": [
            (4, self.sh_product_id.git_repo.responsible_user.id)]}
        find_parent_task = self.sh_product_id.product_tmpl_id.related_task or False
        if not find_parent_task:
            find_parent_tasks = task_obj.sudo().search([
                ('sh_technical_name', '=', self.sh_product_id.sh_technical_name),
                ('parent_id', 'in', (False, None)),
            ])
            if find_parent_tasks:
                if len(find_parent_tasks) > 1:
                    for parent_task in find_parent_tasks:
                        if parent_task.product_template_id.id == self.sh_product_id.product_tmpl_id.id:
                            find_parent_task = parent_task
                            break
                        elif parent_task.project_id.id == connector_obj.preappstore_project_id.id:
                            find_parent_task = parent_task
                            break
                else:
                    find_parent_task = find_parent_tasks

        version_name = f"Odoo {version}"
        find_version = self.env["sh.version"].sudo().search(
            [("name", "=", version_name)], limit=1)
        if find_parent_task:
            # ======= Cheange Project Of Task =======
            if find_parent_task.project_id.id == connector_obj.preappstore_project_id.id:
                find_parent_task.sudo().write(
                    {"project_id": connector_obj.appstore_project_id.id})
            elif not find_parent_task.project_id == connector_obj.appstore_project_id:
                # create parent project
                find_parent_task = self.create_parent_task(
                    version_name, connector_obj)
            # ======= Task Version Ids =======
            if not find_version:
                find_version = self.env["sh.version"].sudo().create(
                    {"name": version_name})
                find_parent_task.sudo().write(
                    {"version_ids": [(4, find_version.id)]})
            elif find_parent_task.version_ids:
                if find_version.id not in find_parent_task.version_ids.ids:
                    find_parent_task.sudo().write(
                        {"version_ids": [(4, find_version.id)]})
            else:
                find_parent_task.sudo().write(
                    {"version_ids": [(4, find_version.id)]})
        else:
            # ======== Create Parent Task ========
            find_parent_task = self.create_parent_task(
                version_name, connector_obj)

        # ======================== Child Task Process ========================
        vals["project_id"] = find_parent_task.project_id.id
        vals["display_project_id"] = find_parent_task.project_id.id
        # ======== Create/Update Task ========
        find_task = self.sh_product_id.related_sub_task or False
        if not find_task:
            find_child_tasks = task_obj.sudo().search([
                ("parent_id", "=", find_parent_task.id)
            ])
            if find_child_tasks:
                # if len(find_child_tasks) > 1:
                for task in find_child_tasks:
                    if task.sh_product_id:
                        if task.sh_product_id.id == self.sh_product_id.id:
                            find_task = task
                            break
                    elif len(task.version_ids.ids) == 1:
                        if task.version_ids[0].id == find_version.id:
                            find_task = task
                            break
                # else:
                #     find_task = find_child_tasks
        if find_task:
            find_task.sudo().write(vals)
        else:
            # if not find_task => Create Child Task:
            vals.update({
                'name': f"{self.sh_product_id.name} v{version}",
                'sh_product_id': self.sh_product_id.id,
                'sh_technical_name': self.sh_product_id.sh_technical_name,
                'product_template_id': self.sh_product_id.product_tmpl_id.id,
            })
            if find_version:
                vals['version_ids'] = [(4, find_version.id)]
            find_task = task_obj.sudo().create(vals)
            find_parent_task.sudo().write({"child_ids": [(4, find_task.id)]})
        # ======== Link Product To Task ========
        self.sh_product_id.product_tmpl_id.sudo().write(
            {"related_task": find_parent_task.id})
        self.sh_product_id.sudo().write({"related_sub_task": find_task.id})
