# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import http, _
from odoo.http import request
from odoo.osv import expression
from odoo import _lt
from odoo.osv.expression import OR

from odoo.addons.project.controllers.portal import ProjectCustomerPortal


class SHTaskCustomerPortal(ProjectCustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'project_count' in counters:
            values['project_count'] = request.env['project.project'].search_count([]) \
                if request.env['project.project'].check_access_rights('read', raise_exception=False) else 0
        if 'task_count' in counters:
            if request.env.user.sh_display_task_menu:
                values['task_count'] = request.env['project.task'].search_count([('project_id', '!=', False)]) \
                    if request.env['project.task'].check_access_rights('read', raise_exception=False) else 0
            else:
                values['task_count'] = 0
        return values

    @http.route(['/my/tasks', '/my/tasks/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_tasks(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, search=None, search_in='content', groupby=None, **kw):
        if request.env.user.sh_display_task_menu:
            return super().portal_my_tasks(page, date_begin, date_end, sortby, filterby, search,search_in,groupby, **kw)
        else:
            return request.not_found()

    def _task_get_searchbar_groupby(self, milestones_allowed):
        values = super()._task_get_searchbar_groupby(milestones_allowed)
        keys_to_remove = ['milestone', 'sale_line', 'sale_order','customer']
        for key in keys_to_remove:
            values.pop(key, None)
        return dict(sorted(values.items(), key=lambda item: item[1]["order"]))

    def _task_get_groupby_mapping(self):
        groupby_mapping = super()._task_get_groupby_mapping()
        keys_to_remove = ['customer', 'milestone', 'sale_order','sale_line']
        for key in keys_to_remove:
            groupby_mapping.pop(key, None)
        return groupby_mapping

    def _task_get_searchbar_inputs(self, milestones_allowed):
        values = super()._task_get_searchbar_inputs(milestones_allowed)
        keys_to_remove = ['all','ref','project','milestone', 'sale_order', 'invoice','message','users']
        for key in keys_to_remove:
            values.pop(key, None)
        return dict(sorted(values.items(), key=lambda item: item[1]["order"]))

    def _task_get_searchbar_sortings(self, milestones_allowed):
        values = super()._task_get_searchbar_sortings(milestones_allowed)
        keys_to_remove = ['update', 'date_deadline', 'milestone']
        for key in keys_to_remove:
            values.pop(key, None)
        return values