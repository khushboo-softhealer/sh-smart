# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import http, _
from odoo.http import request
from odoo.osv import expression

from odoo.addons.hr_timesheet.controllers.portal import TimesheetCustomerPortal


class SHTimesheetCustomerPortal(TimesheetCustomerPortal):

    @http.route(['/my/timesheets', '/my/timesheets/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_timesheets(self, page=1, sortby=None, filterby=None, search=None, search_in='all', groupby='none', **kw):
        if request.env.user.sh_display_timesheet:
            return super().portal_my_timesheets(page, sortby, filterby, search, search_in, groupby, **kw)
        else:
            return request.not_found()
    
    def _task_get_searchbar_sortings(self, milestones_allowed):
        values = super()._task_get_searchbar_sortings(milestones_allowed)
        keys_to_remove = ['progress']
        for key in keys_to_remove:
            values.pop(key, None)
        return values
