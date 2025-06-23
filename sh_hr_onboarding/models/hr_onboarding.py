# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import api, fields, models, _
from datetime import date
from dateutil.relativedelta import relativedelta
from datetime import timedelta, datetime
from odoo.exceptions import ValidationError



class HROnboarding(models.Model):
    _name = 'sh.hr.onboarding'
    _description = "Onboarding"
    _inherit = ['mail.thread',
                'mail.activity.mixin']

    name = fields.Char("Employee Name",tracking=True)
    job_id = fields.Many2one("hr.job",string="Job Position",tracking=True)
    job_title = fields.Char("Job Title",related="job_id.name")
    category_ids = fields.Many2many("hr.employee.category",string="Category",tracking=True)
    department_id = fields.Many2one("hr.department", string="Department",tracking=True)
    parent_id = fields.Many2one("hr.employee",string="Manager",tracking=True)
    coach_id = fields.Many2one("hr.employee",string="Coach",tracking=True)
    work_email = fields.Char("Work Email",tracking=True)
    date_of_joining = fields.Date("Date Of joining",tracking=True)
    company_id = fields.Many2one("res.company",string="Company",tracking=True)
    address_home_id = fields.Many2one("res.partner",string="Address")
    private_email = fields.Char("Pesronal Email",tracking=True)
    gender = fields.Selection([('male','Male'),('female','Female'),('other','Other')],string="Gender")
    birthday = fields.Date("Date of Birth")
    hr_responsible_id = fields.Many2one("res.users",string="HR Responsible",tracking=True)
    date = fields.Date("Date",tracking=True)
    signature_date = fields.Date("Signature Date",tracking=True)
    date_start = fields.Date("Contract Start Date",tracking=True)
    date_end = fields.Date("Contract End Date",tracking=True)
    contract_type = fields.Selection([("month", "Month"), ("year", "Year")],
                                     default="month", string='Contract Type ', tracking=True)

    contract_period = fields.Integer(
        string="Period ", default=6, tracking=True)
    bond = fields.Selection([('none', 'None'), ('cheque', 'Cheque'),
                             ('certificate', 'Certificate'), ('both',
                                                              'Both')], default='none',tracking=True)
    bond_duration = fields.Selection([('month', 'Month'), ('year',
                                                           'Year')], default='year',tracking=True)
    cheque_amount = fields.Float(tracking=True)
    cheque_number = fields.Char(tracking=True)
    period = fields.Integer(tracking=True)
    degree_ids = fields.Many2many(comodel_name='sh.degree',
                                  string='Degree',tracking=True)

    sh_annexure_b_notes = fields.Html('Annexure - B',
                                      default=lambda self:
                                      self.env.user.company_id.annexure_b_notes, copy=True)



    sh_contract_bond_detail_report = \
        fields.Html('Contract Bond Details for Report', copy=True)
    employee_id = fields.Many2one("hr.employee",string="Related Employee")
    user_id = fields.Many2one("res.users",string="Related User")
    contract_id = fields.Many2one("hr.contract",string="Related Contract")

    state = fields.Selection([('draft','New'),('waiting','Waiting For Approve'),('approved','Approved'),('reject','Reject'),('confirm','Confirm'),('cancel','Cancel')],string="State",default="draft",tracking=True)
    template_ids = fields.Many2many('sh.template',string="Access Right Templates")

    signup_url = fields.Char("Signup url")
    resource_calendar_id = fields.Many2one("resource.calendar",string="Working Hours")
    contract_type_id = fields.Many2one("hr.contract.type",string="Contract Type ")
    structure_type_id = fields.Many2one("hr.payroll.structure.type",string="Salary Structure Type")

    adhar_card = fields.Binary("Adhar Card")
    bank_statement = fields.Binary("Bank Statement")
    pan_card = fields.Binary("Pan Card")
    past_payslip  = fields.Binary("Past Payslip")
    salary_offered = fields.Float("Salary Offered")
    mobile = fields.Char("Mobile Number")


    is_applicable_for_tds = fields.Boolean("Is applicable for TDS ?",related='company_id.is_applicable_for_tds')
    employee_contract_type = fields.Selection([('contractual','Contractual'),
                                      ('salaries','Salaried')], string="Contract Type")
    tds_scheme_type = fields.Selection([('old','Old Regime'),
                                      ('new','New Regime')],default='old', string="TDS Scheme")
    
    having_uan_number = fields.Boolean("Having UAN Number ?")
    uan_number = fields.Char("UAN Number")
    struct_id = fields.Many2one("hr.payroll.structure",string="Salary Structure")

    salary_structure_line = fields.One2many('sh.salary.structure',
                                            'onboarding_id')
    emp_pic = fields.Binary("Passport size Photo")

    @api.onchange("job_id")
    def _onchange_job(self):
        if self.job_id and self.job_id.sh_user_access_template:
            self.template_ids = [(6,0,[self.job_id.sh_user_access_template.id])]


    @api.onchange('employee_contract_type','salary_offered','tds_scheme_type','is_applicable_for_tds')
    def _onchange_contract_type(self):
        
        # Auto select salary structure based on selection
        if not self.is_applicable_for_tds and self.env.ref('sh_hr_payroll_tds.structure_base_employee'):

            self.struct_id = self.env.ref('sh_hr_payroll_tds.structure_base_employee').id

        if self.is_applicable_for_tds:
            if self.employee_contract_type == 'salaries':
                if self.tds_scheme_type == 'old' and self.env.ref('sh_hr_payroll_tds.structure_salaries_employee_old_scheme'):
                    self.struct_id = self.env.ref('sh_hr_payroll_tds.structure_salaries_employee_old_scheme').id
                elif self.tds_scheme_type == 'new' and self.env.ref('sh_hr_payroll_tds.structure_salaries_employee_new_scheme'):
                    self.struct_id = self.env.ref('sh_hr_payroll_tds.structure_salaries_employee_new_scheme').id
            elif self.employee_contract_type == 'contractual' and self.env.ref('sh_hr_payroll_tds.structure_contractual_employee'):
                    self.struct_id = self.env.ref('sh_hr_payroll_tds.structure_contractual_employee').id



    def action_quotation_send(self):
        """ Opens a wizard to compose an email, with relevant mail template loaded by default """
        self.ensure_one()

        template = self.env.ref('sh_hr_onboarding.email_template_approval')

        if template:
            template.sudo().send_mail(self.id, force_send=True)

        self.write({'state':'waiting'})
          

        
        # mail_template = self.env.ref('sh_hr_onboarding.email_template_approval', raise_if_not_found=False)
        # lang = self.env.context.get('lang')
        # ctx = {
        #     'default_model': 'sh.hr.onboarding',
        #     'default_res_id': self.id,
        #     'default_use_template': bool(mail_template),
        #     'default_template_id': mail_template.id if mail_template else None,
        #     'default_composition_mode': 'comment',
        #     'default_email_layout_xmlid': 'mail.mail_notification_layout_with_responsible_signature',
        #     'proforma': self.env.context.get('proforma', False),
        #     'force_email': True,
        # }
        # return {
        #     'type': 'ir.actions.act_window',
        #     'view_mode': 'form',
        #     'res_model': 'mail.compose.message',
        #     'views': [(False, 'form')],
        #     'view_id': False,
        #     'target': 'new',
        #     'context': ctx,
        # }


    def action_print_confirmation_report(self):
        contract_ids = [self.contract_id.id]
        datas = {
             'ids': contract_ids,
             'model': 'hr.contract',
        }
        return self.env.ref('sh_hr_contract.action_report_hr_confirmation').sudo().report_action(contract_ids, data={})


    def action_print_contract_report(self):
        contract_ids = [self.contract_id.id]
        datas = {
             'ids': contract_ids,
             'model': 'hr.contract',
        }
        return self.env.ref('sh_hr_contract.action_report_hr_contract').sudo().report_action(contract_ids, data={})


    def action_approve(self):
        #check few mandatory fields
        if not self.job_title or not self.company_id or not self.job_id or not self.department_id or not self.work_email or not self.date_of_joining or not self.struct_id:
            raise ValidationError("Please check these mandatory fields : Job Position, Job Title, Company, Work Email, Department etc !")
        self.write({'state':'approved'})

    def action_reject(self):
        self.write({'state':'reject'})

    def action_draft(self):
        self.write({'state':'draft'})

    def action_cancel(self):
        self.write({'state':'cancel'})

        

    def action_confirm(self):
        print
        

        #create User
        user_vals = {
            'name':self.name,
            'login':self.work_email,
            'template_ids':[(6,0,self.template_ids.ids)],
            'company_id':self.company_id.id,
            'company_ids':[(6,0,[self.company_id.id])],

        }
        user = self.env['res.users'].sudo().create(user_vals)
        if user and user.partner_id:
            user.partner_id.write({'email':self.work_email})
            user.action_reset_password()


        #create Employee
        emp_vals = {
            'name':self.name,
            'work_email':self.work_email,
            'company_id':self.company_id.id,
            'job_id':self.job_id.id,
            'category_ids':[(6,0,self.category_ids.ids)],
            'department_id':self.department_id.id,
            'parent_id':self.parent_id.id,
            'coach_id':self.coach_id.id,
            'date_of_joining':self.date_of_joining,
            'address_home_id':self.address_home_id.id,
            'private_email':self.private_email,
            'gender':self.gender,
            'birthday':self.birthday,
            'user_id':user.id,
            'resource_calendar_id':self.resource_calendar_id.id,
            'phone':self.mobile,
            'having_uan_number':self.having_uan_number,
            'uan_number':self.uan_number,
            'is_applicable_for_tds':self.is_applicable_for_tds,
            'employee_contract_type':self.employee_contract_type,
            'tds_scheme_type':self.tds_scheme_type,

        }
        employee = self.env['hr.employee'].sudo().create(emp_vals)

        #create contract
        contract_vals = {
            'name':self.name + '\'s Contract '+ str(self.date.year),
            'employee_id':employee.id,
            'company_id':self.company_id.id,
            'date':self.date,
            'signature_date':self.signature_date,
            'date_start':self.date_start,
            'date_end':self.date_end,
            'contract_type':self.contract_type,
            'contract_period':self.contract_period,
            'bond':self.bond,
            'bond_duration':self.bond_duration,
            'cheque_amount':self.cheque_amount,
            'cheque_number':self.cheque_number,
            'period':self.period,
            'degree_ids':[(6,0,self.degree_ids.ids)],
            'sh_contract_bond_detail_report':self.sh_contract_bond_detail_report,
            'hr_responsible_id':self.hr_responsible_id.id,
            'job_id':self.job_id.id,
            'department_id':self.department_id.id,
            'wage':self.salary_offered,
            'resource_calendar_id':self.resource_calendar_id.id,
            'contract_type_id':self.contract_type_id.id,
            'sh_annexure_b_notes':self.sh_annexure_b_notes,
            'is_applicable_for_tds':self.is_applicable_for_tds,
            'employee_contract_type':self.employee_contract_type,
            'tds_scheme_type':self.tds_scheme_type,
            'structure_type_id':self.structure_type_id.id,
            'struct_id':self.struct_id.id, 

        }

        contract = self.env['hr.contract'].sudo().create(contract_vals)
        if self.salary_structure_line:
            for line in self.salary_structure_line:
                self.env['sh.salary.structure'].sudo().create({
                    'name':line.name,
                    'sequence':line.sequence,
                    'amount':line.amount,
                    'contract_id':contract.id
                })

        self.write({'state':'confirm',
                    'user_id':user.id,
                    'employee_id':employee.id,
                    'signup_url':user.signup_url,
                    'contract_id':contract.id
                    })

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


    @api.onchange('contract_type', 'contract_period', 'date_start',)
    def _onchange_for_date_end(self):
        if self.date_start and self.contract_period:
            date = ' '
            if self.contract_type == 'month':
                date = self.date_start + \
                    relativedelta(months=self.contract_period, days=-1)
                self.date_end = date
            if self.contract_type == 'year':
                date = self.date_start + \
                    relativedelta(years=self.contract_period, days=-1)
                self.date_end = date



class SalaryStructure(models.Model):
    _inherit = 'sh.salary.structure'

    onboarding_id = fields.Many2one("sh.hr.onboarding",string="Onboarding")
