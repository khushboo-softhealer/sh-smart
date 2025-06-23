# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, http, _
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.tools import date_utils, groupby as groupbyelem
from odoo.osv.expression import AND
from dateutil.relativedelta import relativedelta
from operator import itemgetter
from collections import OrderedDict
import json
import base64
import werkzeug


class PortalHelpdesk(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)

        ticket_domain = []
        if request.env.user.sh_portal_user_access and request.env.user.sh_portal_user_access == 'user':
            ticket_domain.append(('|'))
            ticket_domain.append(('|'))
            ticket_domain.append(('user_id', '=', request.env.user.id))
            ticket_domain.append(('sh_user_ids', 'in', [request.env.user.id]))
            ticket_domain.append(
                ('partner_id', '=', request.env.user.partner_id.id))
        elif request.env.user.sh_portal_user_access and request.env.user.sh_portal_user_access == 'leader':
            ticket_domain.append(('|'))
            ticket_domain.append(('|'))
            ticket_domain.append(('|'))
            ticket_domain.append(('sh_user_ids', 'in', [request.env.user.id]))
            ticket_domain.append(('user_id', '=', request.env.user.id))
            ticket_domain.append(
                ('partner_id', '=', request.env.user.partner_id.id))
            ticket_domain.append(('team_head', '=', request.env.user.id))
        elif request.env.user.sh_portal_user_access and request.env.user.sh_portal_user_access == 'manager':
            ticket_domain.append(('|'))
            ticket_domain.append(('|'))
            ticket_domain.append(('|'))
            ticket_domain.append(('|'))
            ticket_domain.append(('|'))
            ticket_domain.append(('|'))
            ticket_domain.append(('user_id', '=', request.env.user.id))
            ticket_domain.append(('user_id', '=', False))
            ticket_domain.append(('sh_user_ids', 'in', [request.env.user.id]))
            ticket_domain.append(('sh_user_ids', '=', False))
            ticket_domain.append(
                ('partner_id', '=', request.env.user.partner_id.id))
            ticket_domain.append(('team_head', '=', request.env.user.id))
            ticket_domain.append(('team_head', '=', False))
        else:
            ticket_domain.append(('|'))
            ticket_domain.append(('|'))
            ticket_domain.append(('sh_user_ids', 'in', [request.env.user.id]))
            ticket_domain.append(('user_id', '=', request.env.user.id))
            ticket_domain.append(
                ('partner_id', '=', request.env.user.partner_id.id))
        
        
        # --------------------------------------------------------------------------------------------------
        # IF INTERNAL USER LOG-IN THAN ONLY TICKET ONLY ACCESSIBLE WHICH IS ACCESSIBLE IN BACKEND
        # --------------------------------------------------------------------------------------------------
        if request.env.user.has_group('sh_helpdesk.helpdesk_group_user'):
            ticket_domain = request.env['ir.rule']._compute_domain('sh.helpdesk.ticket')
        # --------------------------------------------------------------------------------------------------
        # IF INTERNAL USER LOG-IN THAN ONLY TICKET ONLY ACCESSIBLE WHICH IS ACCESSIBLE IN BACKEND
        # --------------------------------------------------------------------------------------------------
        ticket_count = 0
        if request.env.user._is_admin():
            ticket_domain = [] 
        if request.env.user.has_group('base.group_portal'):
            ticket_count = request.env['sh.helpdesk.ticket'].sudo().search_count(ticket_domain)
        
        # if ticket_count == 0:
        #     ticket_count = '0'

        values['ticket_count'] = ticket_count
        return values

    def _prepare_portal_layout_values(self):
        values = super(PortalHelpdesk, self)._prepare_portal_layout_values()
        ticket_domain = []
        if request.env.user.sh_portal_user_access and request.env.user.sh_portal_user_access == 'user':
            ticket_domain.append(('|'))
            ticket_domain.append(('|'))
            ticket_domain.append(('user_id', '=', request.env.user.id))
            ticket_domain.append(('sh_user_ids', 'in', [request.env.user.id]))
            ticket_domain.append(
                ('partner_id', '=', request.env.user.partner_id.id))
        elif request.env.user.sh_portal_user_access and request.env.user.sh_portal_user_access == 'leader':
            ticket_domain.append(('|'))
            ticket_domain.append(('|'))
            ticket_domain.append(('|'))
            ticket_domain.append(('user_id', '=', request.env.user.id))
            ticket_domain.append(('sh_user_ids', 'in', [request.env.user.id]))
            ticket_domain.append(
                ('partner_id', '=', request.env.user.partner_id.id))
            ticket_domain.append(('team_head', '=', request.env.user.id))
        elif request.env.user.sh_portal_user_access and request.env.user.sh_portal_user_access == 'manager':
            ticket_domain.append(('|'))
            ticket_domain.append(('|'))
            ticket_domain.append(('|'))
            ticket_domain.append(('|'))
            ticket_domain.append(('|'))
            ticket_domain.append(('|'))
            ticket_domain.append(('user_id', '=', request.env.user.id))
            ticket_domain.append(('user_id', '=', False))
            ticket_domain.append(('sh_user_ids', 'in', [request.env.user.id]))
            ticket_domain.append(('sh_user_ids', '=', False))
            ticket_domain.append(
                ('partner_id', '=', request.env.user.partner_id.id))
            ticket_domain.append(('team_head', '=', request.env.user.id))
            ticket_domain.append(('team_head', '=', False))
        else:
            ticket_domain.append(('|'))
            ticket_domain.append(('user_id', '=', request.env.user.id))
            ticket_domain.append(
                ('partner_id', '=', request.env.user.partner_id.id))

        # --------------------------------------------------------------------------------------------------
        # IF INTERNAL USER LOG-IN THAN ONLY TICKET ONLY ACCESSIBLE WHICH IS ACCESSIBLE IN BACKEND
        # --------------------------------------------------------------------------------------------------
        if request.env.user.has_group('sh_helpdesk.helpdesk_group_user'):
            ticket_domain = request.env['ir.rule']._compute_domain('sh.helpdesk.ticket')
        # --------------------------------------------------------------------------------------------------
        # IF INTERNAL USER LOG-IN THAN ONLY TICKET ONLY ACCESSIBLE WHICH IS ACCESSIBLE IN BACKEND
        # --------------------------------------------------------------------------------------------------
        ticket_count = 0
        if request.env.user._is_admin():
            ticket_domain = [] 

        if request.env.user.has_group('base.group_portal'):
            ticket_count = request.env['sh.helpdesk.ticket'].sudo().search_count(ticket_domain)

        values['ticket_count'] = ticket_count
        return values

    def _ticket_get_page_view_values(self, ticket, access_token, **kwargs):
        values = {
            'page_name': 'ticket',
            'ticket': ticket,
        }
        return self._get_page_view_values(ticket, access_token, values, 'my_tickets_history', False, **kwargs)

    @http.route(['/my/sh_tickets', '/my/sh_tickets/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_tickets(self, page=1, sortby=None, filterby=None, search=None, search_in='all', groupby='create_by', **kw):
        values = self._prepare_portal_layout_values()
        HelpdeskTicket = request.env['sh.helpdesk.ticket'].sudo()

        searchbar_sortings = {
            'create_date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
        }
        searchbar_inputs = {
            'all': {'input': 'all', 'label': _('Search in All')},
        }

        searchbar_groupby = {
            'create_by': {'input': 'create_by', 'label': _('Created By')},
            'ticket_type': {'input': 'ticket_type', 'label': _('Ticket Type')},
            'status': {'input': 'status', 'label': _('Status')},
            'customer': {'input': 'customer', 'label': _('Customer')},
            'category': {'input': 'category', 'label': _('Category')},
            'subcategory': {'input': 'subcategory', 'label': _('Sub Category')},
            'subject': {'input': 'subject', 'label': _('Subject')},
            'priority': {'input': 'priority', 'label': _('Priority')},
            'state': {'input': 'state', 'label': _('Reply Status')},
        }

        today = fields.Date.today()
        quarter_start, quarter_end = date_utils.get_quarter(today)
        last_week = today + relativedelta(weeks=-1)
        last_month = today + relativedelta(months=-1)
        last_year = today + relativedelta(years=-1)

        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
            'today': {'label': _('Today'), 'domain': [("create_date", "=", today)]},
            'week': {'label': _('This week'), 'domain': [('create_date', '>=', date_utils.start_of(today, "week")), ('create_date', '<=', date_utils.end_of(today, 'week'))]},
            'month': {'label': _('This month'), 'domain': [('create_date', '>=', date_utils.start_of(today, 'month')), ('create_date', '<=', date_utils.end_of(today, 'month'))]},
            'year': {'label': _('This year'), 'domain': [('create_date', '>=', date_utils.start_of(today, 'year')), ('create_date', '<=', date_utils.end_of(today, 'year'))]},
            'quarter': {'label': _('This Quarter'), 'domain': [('create_date', '>=', quarter_start), ('create_date', '<=', quarter_end)]},
            'last_week': {'label': _('Last week'), 'domain': [('create_date', '>=', date_utils.start_of(last_week, "week")), ('create_date', '<=', date_utils.end_of(last_week, 'week'))]},
            'last_month': {'label': _('Last month'), 'domain': [('create_date', '>=', date_utils.start_of(last_month, 'month')), ('create_date', '<=', date_utils.end_of(last_month, 'month'))]},
            'last_year': {'label': _('Last year'), 'domain': [('create_date', '>=', date_utils.start_of(last_year, 'year')), ('create_date', '<=', date_utils.end_of(last_year, 'year'))]},
        }
        # default sort by value
        if not sortby:
            sortby = 'create_date'
        order = searchbar_sortings[sortby]['order']
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain = AND([searchbar_filters[filterby]['domain']])

        if search and search_in:
            domain = AND([domain, [('name', 'ilike', search)]])
        ticket_domain = []
        if request.env.user.sh_portal_user_access and request.env.user.sh_portal_user_access == 'user':
            ticket_domain.append(('|'))
            ticket_domain.append(('|'))
            ticket_domain.append(('user_id', '=', request.env.user.id))
            ticket_domain.append(('sh_user_ids', 'in', [request.env.user.id]))
            ticket_domain.append(
                ('partner_id', '=', request.env.user.partner_id.id))
        elif request.env.user.sh_portal_user_access and request.env.user.sh_portal_user_access == 'leader':
            ticket_domain.append(('|'))
            ticket_domain.append(('|'))
            ticket_domain.append(('|'))
            ticket_domain.append(('user_id', '=', request.env.user.id))
            ticket_domain.append(('sh_user_ids', 'in', [request.env.user.id]))
            ticket_domain.append(
                ('partner_id', '=', request.env.user.partner_id.id))
            ticket_domain.append(('team_head', '=', request.env.user.id))
        elif request.env.user.sh_portal_user_access and request.env.user.sh_portal_user_access == 'manager':
            ticket_domain.append(('|'))
            ticket_domain.append(('|'))
            ticket_domain.append(('|'))
            ticket_domain.append(('|'))
            ticket_domain.append(('|'))
            ticket_domain.append(('|'))
            ticket_domain.append(('user_id', '=', request.env.user.id))
            ticket_domain.append(('user_id', '=', False))
            ticket_domain.append(('sh_user_ids', 'in', [request.env.user.id]))
            ticket_domain.append(('sh_user_ids', '=', False))
            ticket_domain.append(
                ('partner_id', '=', request.env.user.partner_id.id))
            ticket_domain.append(('team_head', '=', request.env.user.id))
            ticket_domain.append(('team_head', '=', False))
        else:
            ticket_domain.append(('|'))
            ticket_domain.append(('|'))
            ticket_domain.append(('user_id', '=', request.env.user.id))
            ticket_domain.append(('sh_user_ids', 'in', [request.env.user.id]))
            ticket_domain.append(
                ('partner_id', '=', request.env.user.partner_id.id))
        domain = AND([domain, ticket_domain])

        # --------------------------------------------------------------------------------------------------
        # IF INTERNAL USER LOG-IN THAN ONLY TICKET ONLY ACCESSIBLE WHICH IS ACCESSIBLE IN BACKEND
        # --------------------------------------------------------------------------------------------------
        if request.env.user.has_group('sh_helpdesk.helpdesk_group_user'):
            domain = request.env['ir.rule']._compute_domain('sh.helpdesk.ticket')
        # --------------------------------------------------------------------------------------------------
        # IF INTERNAL USER LOG-IN THAN ONLY TICKET ONLY ACCESSIBLE WHICH IS ACCESSIBLE IN BACKEND
        # --------------------------------------------------------------------------------------------------

        if request.env.user._is_admin():
            domain = [] 

        # count for pager
        ticket_count = HelpdeskTicket.sudo().search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/sh_tickets",
            url_args={'sortby': sortby, 'search_in': search_in,
                      'search': search, 'filterby': filterby},
            total=16,
            page=page,
            step=self._items_per_page
        )
        if groupby == 'create_by':
            order = "create_uid, %s" % order
        elif groupby == 'ticket_type':
            order = "ticket_type, %s" % order
        elif groupby == 'status':
            order = "stage_id, %s" % order
        elif groupby == 'customer':
            order = "partner_id, %s" % order
        elif groupby == 'category':
            order = "category_id, %s" % order
        elif groupby == 'subcategory':
            order = "sub_category_id, %s" % order
        elif groupby == 'subject':
            order = "subject_id, %s" % order
        elif groupby == 'priority':
            order = "priority, %s" % order
        elif groupby == 'state':
            order = 'state,%s' % order
        tickets = HelpdeskTicket.search(
            domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_tickets_history'] = tickets.ids[:100]
        if groupby == 'create_by':
            grouped_tickets = [HelpdeskTicket.concat(
                *g) for k, g in groupbyelem(tickets, itemgetter('create_uid'))]
        elif groupby == 'ticket_type':
            grouped_tickets = [HelpdeskTicket.concat(
                *g) for k, g in groupbyelem(tickets, itemgetter('ticket_type'))]
        elif groupby == 'status':
            grouped_tickets = [HelpdeskTicket.concat(
                *g) for k, g in groupbyelem(tickets, itemgetter('stage_id'))]
        elif groupby == 'customer':
            grouped_tickets = [HelpdeskTicket.concat(
                *g) for k, g in groupbyelem(tickets, itemgetter('partner_id'))]
        elif groupby == 'category':
            grouped_tickets = [HelpdeskTicket.concat(
                *g) for k, g in groupbyelem(tickets, itemgetter('category_id'))]
        elif groupby == 'subcategory':
            grouped_tickets = [HelpdeskTicket.concat(
                *g) for k, g in groupbyelem(tickets, itemgetter('sub_category_id'))]
        elif groupby == 'subject':
            grouped_tickets = [HelpdeskTicket.concat(
                *g) for k, g in groupbyelem(tickets, itemgetter('subject_id'))]
        elif groupby == 'priority':
            grouped_tickets = [HelpdeskTicket.concat(
                *g) for k, g in groupbyelem(tickets, itemgetter('priority'))]
        elif groupby == 'state':
            grouped_tickets = [HelpdeskTicket.concat(
                *g) for k, g in groupbyelem(tickets, itemgetter('state'))]
        # content according to pager and archive selected
        values.update({
            'tickets': tickets,
            'grouped_tickets': grouped_tickets,
            'page_name': 'ticket',
            'default_url': '/my/sh_tickets',
            'ticket_count': ticket_count,
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'search_in': search_in,
            'sortby': sortby,
            'groupby': groupby,
            'searchbar_inputs': searchbar_inputs,
            'searchbar_groupby': searchbar_groupby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
        })

        return request.render("sh_helpdesk.portal_my_tickets", values)

    @http.route(['/my/sh_tickets/<int:ticket_id>'], type='http', auth="public", website=True)
    def portal_my_ticket_detail(self, ticket_id, report_type=None, access_token=None, message=False, download=False, **kw):
        try:
            ticket_sudo = self._document_check_access('sh.helpdesk.ticket', ticket_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(model=ticket_sudo, report_type=report_type, report_ref='sh_helpdesk.action_portal_report_helpdesk_ticket', download=download)

        # use sudo to allow accessing/viewing orders for public user
        # only if he knows the private token
        now = fields.Date.today()

        # Log only once a day
        # if ticket_sudo and request.session.get('Ticket viewed by customer %s' % ticket_sudo.id) != now and request.env.user.share and access_token:
        #     request.session['Ticket viewed by customer %s' %
        #                     ticket_sudo.id] = now
        #     print("\n\n\n\nmessage",message)
        #     body = _('Ticket viewed by customer')
        #     _message_post_helper(res_model='sh.helpdesk.ticket', res_id=ticket_sudo.id, message=body, token=ticket_sudo.access_token,
        #                          message_type='notification', subtype="mail.mt_note", partner_ids=ticket_sudo.user_id.sudo().partner_id.ids)
        values = {
            'ticket': ticket_sudo,
            'message': message,
            'token': access_token,
            'bootstrap_formatting': True,
            'report_type': 'html',
        }
        return request.render("sh_helpdesk.portal_ticket_page", values)

    @http.route(['/portal-subcategory-data'], type='json', auth='user')
    def portal_sub_category_data(self, **kw):
        dic = {}
        if kw.get('category_id') and kw.get('category_id') != 'category':
            sub_categ_list = []
            sub_categ_ids = request.env['helpdesk.subcategory'].sudo().search(
                [('parent_category_id', '=', int(kw.get('category_id')))])

            for sub in sub_categ_ids:
                sub_categ_dic = {
                    'id': sub.id,
                    'name': sub.name,
                }
                sub_categ_list.append(sub_categ_dic)
            dic.update({
                'sub_categories': sub_categ_list
            })
        else:
            dic.update({
                'sub_categories': []
            })
        return json.dumps(dic)

    @http.route(['/portal-partner-data'], type='json', auth='user')
    def portal_partner_data(self, **kw):
        dic = {}
        partner_list = []
        for partner in request.env['res.partner'].sudo().search([]):
            partner_dic = {
                'id': partner.id,
                'name': partner.name,
            }
            partner_list.append(partner_dic)
        dic.update({
            'partners': partner_list
        })
        return json.dumps(dic)

    @http.route('/selected-partner-data', type='json', auth='user')
    def selected_partner_data(self, **kw):
        dic = {}
        if kw.get('partner_id') and kw.get('partner_id') != '':
            partner = request.env['res.partner'].sudo().search(
                [('id', '=', int(kw.get('partner_id')))], limit=1)
            if partner:
                dic.update({
                    'name': partner.name,
                    'email': partner.email,
                })
        return json.dumps(dic)

    @http.route('/portal-user-data', type='json', auth='user')
    def portal_user_data(self, **kw):
        dic = {}
        if kw.get('team_id') and kw.get('team_id') != 'team':
            users_list = []
            team_id = request.env['sh.helpdesk.team'].sudo().search(
                [('id', '=', int(kw.get('team_id')))])
            for member in team_id.team_members:
                user_dic = {
                    'id': member.id,
                    'name': member.name,
                }
                users_list.append(user_dic)
            dic.update({
                'users': users_list
            })
        else:
            dic.update({
                'users': []
            })
        return json.dumps(dic)

    @http.route('/portal-create-ticket', type='http', auth='public', csrf=False)
    def portal_create_ticket(self, **kw):
        multi_users_value = request.httprequest.form.getlist(
            'portal_assign_multi_user')
        if 'users' in multi_users_value:
            del multi_users_value[0]
        login_user = request.env.user
        # if login_user and login_user.login != 'public':
        if not login_user._is_public():
            partner_id = False
            if kw.get('partner_id') and kw.get('partner_id') != '':
                partner_id = request.env['res.partner'].sudo().search(
                    [('id', '=', int(kw.get('partner_id')))], limit=1)
            else:
                partner_id = request.env['res.partner'].sudo().search(
                    [('email', '=', kw.get('portal_email'))], limit=1)
            if not partner_id:
                partner_id = request.env['res.partner'].sudo().create({
                    'name': kw.get('portal_contact_name'),
                    'company_type': 'person',
                    'email': kw.get('portal_email'),
                })
            if not partner_id:
                partner_id = request.env['res.partner'].sudo().create({
                    'name': kw.get('portal_contact_name'),
                    'company_type': 'person',
                    'email': kw.get('portal_email'),
                })
            if partner_id:
                ticket_dic = {'partner_id': partner_id.id}
                if len(multi_users_value) > 0:
                    users = []
                    for user in multi_users_value:
                        users.append(int(user))
                    multi_users = request.env['res.users'].sudo().browse(users)
                    if multi_users:
                        ticket_dic.update({
                            'sh_user_ids': [(6, 0, multi_users.ids)]
                        })
                if kw.get('portal_team') and kw.get('portal_team') != 'team':
                    team_id = request.env['sh.helpdesk.team'].sudo().browse(
                        int(kw.get('portal_team')))
                    if team_id:
                        ticket_dic.update({
                            'team_id': team_id.id,
                            'team_head': team_id.team_head.id,
                        })
                if kw.get('portal_assign_user') and kw.get('portal_assign_user') != 'user':
                    portal_user_id = request.env['res.users'].sudo().browse(
                        int(kw.get('portal_assign_user')))
                    if portal_user_id:
                        ticket_dic.update({
                            'user_id': portal_user_id.id,
                        })
                if not ticket_dic.get('team_id') or not ticket_dic.get('user_id'):
                    if login_user.sh_portal_user_access and request.env.user.has_group('base.group_portal') and login_user.sh_portal_user_access == 'user' or login_user.sh_portal_user_access == 'manager' or login_user.sh_portal_user_access == 'leader':
                        if request.env.user.company_id.sh_default_team_id:
                            ticket_dic.update({
                                'team_id': request.env.user.company_id.sh_default_team_id.id,
                                'team_head': request.env.user.company_id.sh_default_team_id.team_head.id,
                                'user_id': request.env.user.company_id.sh_default_user_id.id,
                            })
                        else:
                            team_id = request.env['sh.helpdesk.team'].sudo().search(
                                ['|', ('team_head', '=', login_user.id), ('team_members', 'in', [login_user.id])])
                            if team_id:
                                ticket_dic.update({
                                    'team_id': team_id[-1].id,
                                    'team_head': team_id[-1].team_head.id,
                                    'user_id': login_user.id,
                                })
                            else:
                                ticket_dic.update({
                                    'user_id': login_user.id,
                                })
                        ticket_dic.update({'state': 'staff_replied'})
                    else:
                        if request.env.user.company_id.sh_default_team_id:
                            ticket_dic.update({
                                'team_id': request.env.user.company_id.sh_default_team_id.id,
                                'team_head': request.env.user.company_id.sh_default_team_id.team_head.id,
                                'user_id': request.env.user.company_id.sh_default_user_id.id,
                            })
                        else:
                            if not login_user.has_group('base.group_portal') and not login_user.sh_portal_user_access:
                                team_id = request.env['sh.helpdesk.team'].sudo().search(
                                    ['|', ('team_head', '=', login_user.id), ('team_members', 'in', [login_user.id])])
                                if team_id:
                                    ticket_dic.update({
                                        'team_id': team_id[-1].id,
                                        'team_head': team_id[-1].team_head.id,
                                        'user_id': login_user.id,
                                    })
                                else:
                                    ticket_dic.update({
                                        'user_id': login_user.id,
                                    })
                if kw.get('portal_contact_name'):
                    ticket_dic.update({
                        'person_name': kw.get('portal_contact_name'),
                    })
                if kw.get('portal_email'):
                    ticket_dic.update({
                        'email': kw.get('portal_email'),
                    })
                if kw.get('portal_category') and kw.get('portal_category') != 'category':
                    ticket_dic.update({
                        'category_id': int(kw.get('portal_category')),
                    })
                if kw.get('portal_subcategory') and kw.get('portal_subcategory') != 'sub_category':
                    ticket_dic.update({
                        'sub_category_id': int(kw.get('portal_subcategory')),
                    })
                if kw.get('portal_subject') and kw.get('portal_subject') != 'subject':
                    ticket_dic.update({
                        'subject_id': int(kw.get('portal_subject')),
                    })
                if kw.get('portal_description'):
                    ticket_dic.update({
                        'description': kw.get('portal_description'),
                    })
                if kw.get('portal_priority') and kw.get('portal_priority') != 'priority':
                    ticket_dic.update({
                        'priority': int(kw.get('portal_priority')),
                    })
                ticket_id = request.env['sh.helpdesk.ticket'].sudo().create(
                    ticket_dic)
                if 'portal_file' in request.params:
                    attached_files = request.httprequest.files.getlist(
                        'portal_file')
                    attachment_ids = []
                    for attachment in attached_files:
                        result = base64.b64encode(attachment.read())
                        attachment_id = request.env['ir.attachment'].sudo().create({
                            'name': attachment.filename,
                            'res_model': 'sh.helpdesk.ticket',
                            'res_id': ticket_id.id,
                            'display_name': attachment.filename,
                            'datas': result,
                            'public': True,
                        })
                        attachment_ids.append(attachment_id.id)
                    ticket_id.attachment_ids = [(6, 0, attachment_ids)]
        return werkzeug.utils.redirect("/my/sh_tickets")
