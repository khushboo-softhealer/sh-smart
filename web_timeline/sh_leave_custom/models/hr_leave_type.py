# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import api, fields, models
from odoo.addons.resource.models.resource import Intervals
from collections import defaultdict
import datetime
from datetime import time, timedelta
from odoo.tools.translate import _
from odoo.tools.float_utils import float_round

class LeaveType(models.AbstractModel):
    _inherit = "hr.leave.type"

    allocation_type = fields.Selection([
        ('fixed', 'Fixed by HR'),
        ('fixed_allocation', 'Fixed by HR + allocation request'),
        ('no', 'No allocation')],
        default='fixed', string='Mode',
        help='\tFixed by HR: allocated by HR and cannot be bypassed; users can request leaves;'
             '\tFixed by HR + allocation request: allocated by HR and users can request leaves and allocations;'
             '\tNo allocation: no allocation by default, users can freely request leaves;')


    def _get_employees_days_per_allocation(self, employee_ids, date=None):
        if not date:
            date = fields.Date.to_date(self.env.context.get('default_date_from')) or fields.Date.context_today(self)

        leaves_domain = [
            ('employee_id', 'in', employee_ids),
            ('state', 'in', ['confirm', 'validate1', 'validate']),
            ('holiday_status_id', 'in', self.ids)
        ]
        if self.env.context.get("ignore_future"):
            leaves_domain.append(('date_from', '<=', date))
        leaves = self.env['hr.leave'].search(leaves_domain)

        allocations = self.env['hr.leave.allocation'].with_context(active_test=False).search([
            ('employee_id', 'in', employee_ids),
            ('state', 'in', ['validate']),
            ('holiday_status_id', 'in', self.ids),
        ])

        # The allocation_employees dictionary groups the allocations based on the employee and the holiday type
        # The structure is the following:
        # - KEYS:
        # allocation_employees
        #   |--employee_id
        #      |--holiday_status_id
        # - VALUES:
        # Intervals with the start and end date of each allocation and associated allocations within this interval
        allocation_employees = defaultdict(lambda: defaultdict(list))

        ### Creation of the allocation intervals ###
        for holiday_status_id in allocations.holiday_status_id:
            for employee_id in employee_ids:
                allocation_intervals = Intervals([(
                    fields.datetime.combine(allocation.date_from, time.min),
                    fields.datetime.combine(allocation.date_to or datetime.date.max, time.max),
                    allocation)
                    for allocation in allocations.filtered(lambda allocation: allocation.employee_id.id == employee_id and allocation.holiday_status_id == holiday_status_id)])
                allocation_employees[employee_id][holiday_status_id] = allocation_intervals

        # The leave_employees dictionary groups the leavess based on the employee and the holiday type
        # The structure is the following:
        # - KEYS:
        # leave_employees
        #   |--employee_id
        #      |--holiday_status_id
        # - VALUES:
        # Intervals with the start and end date of each leave and associated leave within this interval
        leaves_employees = defaultdict(lambda: defaultdict(list))
        leave_intervals = []

        ### Creation of the leave intervals ###
        if leaves:
            for holiday_status_id in leaves.holiday_status_id:
                for employee_id in employee_ids:
                    leave_intervals = Intervals([(
                        fields.datetime.combine(leave.date_from, time.min),
                        fields.datetime.combine(leave.date_to, time.max),
                        leave)
                        for leave in leaves.filtered(lambda leave: leave.employee_id.id == employee_id and leave.holiday_status_id == holiday_status_id)])
                    leaves_employees[employee_id][holiday_status_id] = leave_intervals
        # allocation_days_consumed is a dictionary to map the number of days/hours of leaves taken per allocation
        # The structure is the following:
        # - KEYS:
        # allocation_days_consumed
        #  |--employee_id
        #      |--holiday_status_id
        #          |--allocation
        #              |--virtual_leaves_taken
        #              |--leaves_taken
        #              |--virtual_remaining_leaves
        #              |--remaining_leaves
        #              |--max_leaves
        #              |--closest_allocation_to_expire
        # - VALUES:
        # Integer representing the number of (virtual) remaining leaves, (virtual) leaves taken or max leaves for each allocation.
        # The unit is in hour or days depending on the leave type request unit
        allocations_days_consumed = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0))))

        company_domain = [('company_id', 'in', list(set(self.env.company.ids + self.env.context.get('allowed_company_ids', []))))]

        ### Existing leaves assigned to allocations ###
        if leaves_employees:
            for employee_id, leaves_interval_by_status in leaves_employees.items():
                for holiday_status_id in leaves_interval_by_status:
                    days_consumed = allocations_days_consumed[employee_id][holiday_status_id]
                    if allocation_employees[employee_id][holiday_status_id]:
                        allocations = allocation_employees[employee_id][holiday_status_id] & leaves_interval_by_status[holiday_status_id]
                        available_allocations = self.env['hr.leave.allocation']
                        for allocation_interval in allocations._items:
                            available_allocations |= allocation_interval[2]
                        # Consume the allocations that are close to expiration first
                        sorted_available_allocations = available_allocations.filtered('date_to').sorted(key='date_to')
                        sorted_available_allocations += available_allocations.filtered(lambda allocation: not allocation.date_to)
                        leave_intervals = leaves_interval_by_status[holiday_status_id]._items
                        sorted_allocations_with_remaining_leaves = self.env['hr.leave.allocation']
                        for leave_interval in leave_intervals:
                            leaves = leave_interval[2]
                            for leave in leaves:
                                if leave.leave_type_request_unit in ['day', 'half_day']:
                                    leave_duration = leave.number_of_days
                                #     leave_unit = 'days'
                                else:
                                    # leave_duration = leave.number_of_hours_display
                                    leave_unit = 'hours'
                                leave_duration = leave.number_of_days
                                if holiday_status_id.requires_allocation != 'no':
                                    for available_allocation in sorted_available_allocations:
                                        if (available_allocation.date_to and available_allocation.date_to < leave.date_from.date()) \
                                            or (available_allocation.date_from > leave.date_to.date()):
                                            continue
                                        virtual_remaining_leaves = (available_allocation.number_of_days) - allocations_days_consumed[employee_id][holiday_status_id][available_allocation]['virtual_leaves_taken']
                                        max_leaves = min(virtual_remaining_leaves, leave_duration)
                                        days_consumed[available_allocation]['virtual_leaves_taken'] += max_leaves
                                        if leave.state == 'validate':
                                            days_consumed[available_allocation]['leaves_taken'] += max_leaves
                                        leave_duration -= max_leaves
                                        # Check valid allocations with still availabe leaves on it
                                        if days_consumed[available_allocation]['virtual_remaining_leaves'] > 0 and available_allocation.date_to and available_allocation.date_to > date:
                                            sorted_allocations_with_remaining_leaves |= available_allocation
                                    if leave_duration > 0:
                                        # There are not enough allocation for the number of leaves
                                        days_consumed[False]['virtual_remaining_leaves'] -= leave_duration
                                else:
                                    days_consumed[False]['virtual_leaves_taken'] += leave_duration
                                    if leave.state == 'validate':
                                        days_consumed[False]['leaves_taken'] += leave_duration
                        # no need to sort the allocations again
                        allocations_days_consumed[employee_id][holiday_status_id][False]['closest_allocation_to_expire'] = sorted_allocations_with_remaining_leaves[0] if sorted_allocations_with_remaining_leaves else False

        # Future available leaves
        future_allocations_date_from = fields.datetime.combine(date, time.min)
        future_allocations_date_to = fields.datetime.combine(date, time.max) + timedelta(days=5*365)
        for employee_id, allocation_intervals_by_status in allocation_employees.items():
            employee = self.env['hr.employee'].browse(employee_id)
            for holiday_status_id, intervals in allocation_intervals_by_status.items():
                if not intervals:
                    continue
                future_allocation_intervals = intervals & Intervals([(
                    future_allocations_date_from,
                    future_allocations_date_to,
                    self.env['hr.leave'])])
                search_date = date
                closest_allocations = self.env['hr.leave.allocation']
                for interval in intervals._items:
                    closest_allocations |= interval[2]
                allocations_with_remaining_leaves = self.env['hr.leave.allocation']
                for interval_from, interval_to, interval_allocations in future_allocation_intervals._items:
                    if interval_from.date() > search_date:
                        continue
                    interval_allocations = interval_allocations.filtered('active')
                    if not interval_allocations:
                        continue
                    # If no end date to the allocation, consider the number of days remaining as infinite
                    employee_quantity_available = (
                        employee._get_work_days_data_batch(interval_from, interval_to, compute_leaves=False, domain=company_domain)[employee_id]
                        if interval_to != future_allocations_date_to
                        else {'days': float('inf'), 'hours': float('inf')}
                    )
                    for allocation in interval_allocations:
                        if allocation.date_from > search_date:
                            continue
                        days_consumed = allocations_days_consumed[employee_id][holiday_status_id][allocation]
                        if allocation.type_request_unit in ['day', 'half_day']:
                            quantity_available = employee_quantity_available['days']
                            # remaining_days_allocation = (allocation.number_of_days - days_consumed['virtual_leaves_taken'])
                        else:
                            quantity_available = employee_quantity_available['hours']
                            # remaining_days_allocation = (allocation.number_of_hours_display - days_consumed['virtual_leaves_taken'])
                        remaining_days_allocation = (allocation.number_of_days - days_consumed['virtual_leaves_taken'])
                        if quantity_available <= remaining_days_allocation:
                            search_date = interval_to.date() + timedelta(days=1)
                        days_consumed['virtual_remaining_leaves'] += min(quantity_available, remaining_days_allocation)
                        days_consumed['max_leaves'] = allocation.number_of_days
                        days_consumed['remaining_leaves'] = days_consumed['max_leaves'] - days_consumed['leaves_taken']
                        if remaining_days_allocation >= quantity_available:
                            break
                        # Check valid allocations with still availabe leaves on it
                        if days_consumed['virtual_remaining_leaves'] > 0 and allocation.date_to and allocation.date_to > date:
                            allocations_with_remaining_leaves |= allocation
                allocations_sorted = sorted(allocations_with_remaining_leaves, key=lambda a: a.date_to)
                allocations_days_consumed[employee_id][holiday_status_id][False]['closest_allocation_to_expire'] = allocations_sorted[0] if allocations_sorted else False
        return allocations_days_consumed


    def name_get(self):
        if not self.requested_name_get():
            # leave counts is based on employee_id, would be inaccurate if not based on correct employee
            return super(LeaveType, self).name_get()
        res = []
        for record in self:
            name = record.name
            if record.requires_allocation == "yes" and not self._context.get('from_manager_leave_form'):
                name = "%(name)s (%(count)s)" % {
                    'name': name,
                    'count': _('%g remaining out of %g') % (
                        float_round(record.virtual_remaining_leaves, precision_digits=2) or 0.0,
                        float_round(record.max_leaves, precision_digits=2) or 0.0,
                    ) + (_(' days'))
                }
            res.append((record.id, name))
        return res


    def get_days(self, employee_id):
        # need to use `dict` constructor to create a dict per id
        result = dict((id, dict(max_leaves=0, leaves_taken=0,
                      remaining_leaves=0, virtual_remaining_leaves=0)) for id in self.ids)

        current_contract_id = self.env['hr.contract'].search(
            [('employee_id', '=', employee_id), ('state', 'in', ('open', 'pending')),
             ('date_start', '<=', fields.Date.today()),
             ('date_end', '>=', fields.Date.today())],
            limit=1)
        if current_contract_id and current_contract_id.allocation_id:

            requests = self.env['hr.leave'].search([
                ('employee_id', '=', employee_id),
                ('state', 'in', ['confirm', 'validate1', 'validate']),
                ('request_date_from', '>=',
                 current_contract_id.allocation_id.date_start),
                ('request_date_to', '<=',
                 current_contract_id.allocation_id.date_end),
                ('holiday_status_id', 'in', self.ids)
            ])
            allocations = current_contract_id.allocation_id
            if requests:
                for request in requests:
                    if request.holiday_status_id.id in result:
                        status_dict = result[request.holiday_status_id.id]
                        status_dict['virtual_remaining_leaves'] -= (
                            request.number_of_hours_display
                            if request.leave_type_request_unit == 'hour' else
                            request.number_of_days)
                        if request.state == 'validate':
                            status_dict['leaves_taken'] += (
                                request.number_of_hours_display
                                if request.leave_type_request_unit == 'hour' else
                                request.number_of_days)
                            status_dict['remaining_leaves'] -= (
                                request.number_of_hours_display
                                if request.leave_type_request_unit == 'hour' else
                                request.number_of_days)

            if allocations:
                for allocation in allocations.sudo():
                    if allocation.holiday_status_id.id in result:
                        status_dict = result[allocation.holiday_status_id.id]
                        if allocation.state == 'validate':
                            # note: add only validated allocation even for the virtual
                            # count; otherwise pending then refused allocation allow
                            # the employee to create more leaves than possible
                            status_dict['virtual_remaining_leaves'] += (
                                allocation.number_of_hours_display
                                if allocation.type_request_unit == 'hour' else
                                allocation.number_of_days)
                            status_dict['max_leaves'] += (
                                allocation.number_of_hours_display
                                if allocation.type_request_unit == 'hour' else
                                allocation.number_of_days)
                            status_dict['remaining_leaves'] += (
                                allocation.number_of_hours_display
                                if allocation.type_request_unit == 'hour' else
                                allocation.number_of_days)
        return result
