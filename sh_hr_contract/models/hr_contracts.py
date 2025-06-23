# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields, api, _
from datetime import date
from dateutil.relativedelta import relativedelta
from datetime import timedelta, datetime
from odoo.exceptions import ValidationError


class Contract(models.Model):
    _inherit = 'hr.contract'

    state = fields.Selection(selection_add=[('pending', 'To Renew'),('close',)])
    date = fields.Date(tracking=True)
    signature_date = fields.Date(tracking=True)
    bond = fields.Selection([('none', 'None'), ('cheque', 'Cheque'),
                             ('certificate', 'Certificate'), ('both',
                                                              'Both')], default='none',tracking=True)
    bond_duration = fields.Selection([('month', 'Month'), ('year',
                                                           'Year')], default='year',tracking=True)
    cheque_amount = fields.Float(tracking=True)
    cheque_number = fields.Char(tracking=True)
    period = fields.Integer(tracking=True)
    digital_signature = fields.Binary(attachment=True,tracking=True)
    salary_structure_line = fields.One2many('sh.salary.structure',
                                            'contract_id')
    degree_ids = fields.Many2many(comodel_name='sh.degree',
                                  string='Degree')

    print_in_report = fields.Boolean(string='print in report')

    sh_annexure_b_notes = fields.Html('Annexure - B',
                                      default=lambda self:
                                      self.env.user.company_id.annexure_b_notes, copy=True,tracking=True)

    sh_contract_bond_detail_report = \
        fields.Html('Contract Bond Details for Report', copy=True)

    sh_contract_improvement_ids = fields.One2many(
        "hr.contract.improvement", 'contract_id', string="Improvements")
    sh_contract_goal_ids = fields.One2many(
        "hr.contract.goals", 'contract_id', string="Goals")
    
    renew_contract = fields.Boolean("Want to Renew Contract Automatically ?",tracking=True)
    renew_start_date = fields.Date("Renewal Contract Start Date")
    renew_end_date = fields.Date("Renewal Contract End Date")
    renew_contract_type = fields.Selection([("month", "Month"), ("year", "Year")],
                                     default="month", string='Contract Type ', tracking=True)

    renew_contract_period = fields.Integer(
        string="Renewal Period ", default=6, tracking=True)
    
    
    @api.onchange("renew_contract")
    def onchange_renew_contract(self):
        if self.renew_contract:
            self.renew_start_date = self.date_end + timedelta(days=1)
                        
    
    @api.onchange('renew_contract_type', 'renew_contract_period', 'renew_start_date',)
    def _onchange_for_renew_end_date(self):
        if self.renew_start_date and self.renew_contract_period:
            date = ' '
            if self.renew_contract_type == 'month':
                date = self.renew_start_date + \
                    relativedelta(months=self.renew_contract_period, days=-1)
                self.renew_end_date = date
            if self.renew_contract_type == 'year':
                date = self.renew_start_date + \
                    relativedelta(years=self.renew_contract_period, days=-1)
                self.renew_end_date = date


    @api.model
    #update date of joining in employee if not set
    def create(self, vals):
        res = super().create(vals)
        if res.employee_id:
            # find total number of contract
            if res.employee_id.contracts_count >=2 and not res.employee_id.date_of_joining:
                res.employee_id.write({'date_of_joining':res.date_start})
        return res


    @api.model
    def update_state(self):
        # Called by a cron
        # Override standard method
        # It schedules an activity before the expiration of a credit time contract
        # res = super(Contract, self).update_state()
        from_cron = 'from_cron' in self.env.context
        # contracts_to_close = self.search([
        #     ('state', 'in', ['open','pending']),
        #     '|',
        #     ('date_end', '<=', fields.Date.to_string(date.today())),
        #     ('visa_expire', '<=', fields.Date.to_string(date.today())),
        # ])
        # print("\n\=contracts_to_close",contracts_to_close)
        # if contracts_to_close:
        #     contracts_to_close._safe_write_for_cron({'state': 'close'}, from_cron)

        hr_contracts=self.search([
            ('state', '=', 'open'),
            ('date_end', '<=', fields.Date.to_string(
                date.today() + relativedelta(days=15))),
           
        ])
        hr_contracts._safe_write_for_cron({'state': 'pending'}, from_cron)
        # hr_contracts.write({
        #     'state': 'pending'
        # })

        

        #code to create renewal contract automatically
        try:
            for hr_contract in hr_contracts:
                if hr_contract.renew_contract:
            
                    if not hr_contract.renew_start_date or not hr_contract.renew_end_date:
                        raise ValidationError('Renewal Start and End date not set for employee %s !' %(hr_contract.employee_id.name))
                    new_contract = hr_contract.copy()
                    new_contract.write({
                        'date_start':hr_contract.renew_start_date,
                        'date_end':hr_contract.renew_end_date,
                        'contract_type':hr_contract.renew_contract_type,
                        'contract_period':hr_contract.renew_contract_period,
                        'name':hr_contract.employee_id.name + '\'s Contract from '+str(hr_contract.renew_start_date) + ' To '+str(hr_contract.renew_end_date),
                        'days_extend':0,
                        # 'state':'open',
                        'wage':hr_contract.wage,
                        'resource_calendar_id':hr_contract.resource_calendar_id.id
                    })
                    new_contract.onchange_renew_contract()
                    new_contract._onchange_for_renew_end_date()
                    new_contract._onchange_contract_type()


                    #leave allocation
                    if hr_contract.allocation_id:
                        leave_allocation_wizard = self.env['sh.employee.leave.allocation.wizard'].sudo().create({
                            'type':'last',
                            'allocation_id':hr_contract.allocation_id.id,
                            'employee_id':new_contract.employee_id.id,
                            'contract_id':new_contract.id
                        })
                        leave_allocation_wizard.allocate_leave_wizard()
                    else:
                        leave_allocation_wizard = self.env['sh.employee.leave.allocation.wizard'].sudo().create({
                            'type':'new',
                            'employee_id':new_contract.employee_id.id,
                            'contract_id':new_contract.id
                        })
                        leave_allocation_wizard.allocate_leave_wizard()
                    
                    #validate allocation
                    if new_contract and new_contract.allocation_id:
                        new_contract.allocation_id.action_confirm()

                    new_contract.write({'state':'open'})
        
                #generate goal sheet for old contract
                
                goal_sheet_wizard_id = self.env['sh.generate.goal.sheet.wizard.contract'].sudo().create({
                    'date_from': hr_contract.date_start ,
                    'date_to':hr_contract.date_end,
                    'employee_id':hr_contract.employee_id.id,
                    'contract_id':hr_contract.id

                })
                    
                goal_sheet_wizard_id.generate_goals()
        
        
        except Exception as e:
                message = f'Error for renewal contract: {e}\n'
                print(">>>>>>>>>>>>>>>>EXCEption", message)
                listt = []
                users = self.env['res.users'].search([])
                for user in users:
                    if user.has_group('hr.group_hr_manager'):
                        for hr_contract in hr_contracts:
                            self.env['mail.activity'].sudo().create({
                                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                                'user_id': user.id,
                                'res_id': hr_contract.id,
                                'res_model_id': self.env['ir.model'].sudo().search([('model', '=', 'hr.contract')], limit=1).id,
                                'summary': message,
                            })

                
                

        
        return True

    @api.onchange(
        'bond',
        'bond_duration',
        'period',
        'degree_ids',
        'cheque_amount',
        'cheque_number',
    )
    def onchange_for_report(self):
        detail = ' '
        if self.bond == 'none':
            detail = ' '
        if self.bond == 'cheque':
            detail = ' '

            detail += '<div style="font-size:12px">' \
                + '<span> You have deposit us cheque </span>' \
                + str(self.cheque_number) + '<span> of </span>' \
                + str(self.cheque_amount) \
                + '<span> as security for the time period of </span>' \
                + str(self.period) + '&nbsp;' + str(self.bond_duration) \
                + '<span> which will be given back after </span>' \
                + str(self.period) + '&nbsp;' + str(self.bond_duration) \
                + '<span>. If employee resigns before term end. </span>' \
                + str(self.env.user.company_id.name) \
                + '<span> will have rights to deposit cheque and legal action against employee. </span>' + ' </div> '

        if self.bond == 'certificate':
            detail = ' '

            detail += '<div style="font-size:12px">' \
                + '<span> You have deposit us Certificate of your </span>'

            for degree in self.degree_ids:
                detail += str(degree.name) + ',' + '&nbsp;'

            detail += '<span> as security for the time period of </span>' \
                + str(self.period) + '&nbsp;' + str(self.bond_duration) \
                + '<span> which will be given back after </span>' \
                + str(self.period) + '&nbsp;' + str(self.bond_duration) \
                + '<span>. If employee resigns before term end. </span>' \
                + str(self.env.user.company_id.name) \
                + '<span> will have rights to forfeit the certificate and legal action against employee. </span>' + ' </div> '

        if self.bond == 'both':
            detail = ' '

            detail += '<div style="font-size:12px">' \
                + '<span> You have deposit us cheque </span>' \
                + str(self.cheque_number) + '<span> of </span>' \
                + str(self.cheque_amount) \
                + '<span>. And deposit us Certificate of your </span>'
            for degree in self.degree_ids:
                detail += str(degree.name) + ',' + '&nbsp;'

            detail += '<span> as security for the time period of </span>' \
                + str(self.period) + '&nbsp;' + str(self.bond_duration) \
                + '<span> which will be given back after </span>' \
                + str(self.period) + '&nbsp;' + str(self.bond_duration) \
                + '<span>. If employee resigns before term end. </span>' \
                + str(self.env.user.company_id.name) \
                + '<span> will have rights to deposit cheque OR forfeit the certificate and legal action against employee. </span>' + ' </div> '

        self.sh_contract_bond_detail_report = detail

    # @api.onchange('state')
    # def onchange_stage(self):
    #     users = self.env['res.users'].search([])
    #     listt = []
    #     for user in users:
    #         if user.has_group('hr.group_hr_manager'):
    #             listt.append(user)

    #     base_url = self.env['ir.config_parameter'
    #                         ].sudo().get_param('web.base.url')

    #     self.env['user.push.notification'].push_notification(listt, 'Contract Stage Changed', 'Contract : %s:' % (
    #         self.name), base_url+"/mail/view?model=hr.contract&res_id="+str(self._origin.id), 'hr.contract', self._origin.id, 'hr')

    def write(self, vals):
        for rec in self:
            if vals.get('state'):
                users = self.env['res.users'].search([])
                listt = []
                for user in users:
                    if user.has_group('hr.group_hr_manager'):
                        listt.append(user)

                base_url = self.env['ir.config_parameter'
                                    ].sudo().get_param('web.base.url')
                self.env['user.push.notification'].push_notification(listt, 'Contract Stage Changed', 'Contract : %s:' % (
                    rec.name), base_url+"/mail/view?model=hr.contract&res_id="+str(rec.id), 'hr.contract', rec.id, 'hr')

        return super(Contract, self).write(vals)

    def action_send_contract(self):
        self.ensure_one()
        template_id = self.env['ir.model.data'
                               ]._xmlid_to_res_id('sh_hr_contract.email_template_hr_contract', raise_if_not_found=False)
        try:
            compose_form_id = self.env.ref(
                'mail.email_compose_message_wizard_form').id
        except ValueError:
            compose_form_id = False

        ctx = {
            'default_model': 'hr.contract',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'custom_layout': 'mail.mail_notification_light',
        }
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    def action_send_confirmation(self):
        self.ensure_one()
        template_id = self.env['ir.model.data'
                               ]._xmlid_to_res_id('sh_hr_contract.email_template_hr_cofirmation', raise_if_not_found=False)
        try:
            compose_form_id = self.env.ref(
                'mail.email_compose_message_wizard_form').id
        except ValueError:
            compose_form_id = False

        ctx = {
            'default_model': 'hr.contract',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'custom_layout': 'mail.mail_notification_light',
        }
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }
