# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import api, exceptions, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Employee Inherit


class ShEmployeeExtraFields(models.Model):
    _inherit = 'hr.employee'

    work_country_id = fields.Many2one('res.country', string='Work Country')
    reference_by_id = fields.Many2one('hr.employee', string='Reference By')
    previous_nationality_id = fields.Many2one(
        'res.country', string='Previous Nationality')
    passport_country_id = fields.Many2one(
        'res.country', string='Passport Country')
    passport_issue = fields.Date(string='Passport Issue Date', default=lambda self: self._context.get(
        'date', fields.Date.context_today(self)))
    passport_expiry = fields.Date(string='Passport Expiry Date', default=lambda self: self._context.get(
        'date', fields.Date.context_today(self)))
    religion_id = fields.Many2one('sh.employee.religion', string='Religion')
    height = fields.Float("Height")
    weight = fields.Float("Weight")
    blood_group = fields.Selection([('A +ve', 'A +ve'), ('A -ve', 'A -ve'),
                                    ('B +ve', 'B +ve'), ('B -ve', 'B -ve'),
                                    ('AB +ve', 'AB +ve'), ('AB -ve', 'AB -ve'),
                                    ('O +ve', 'O +ve'), ('O -ve', 'O -ve'), ],
                                   string='Blood Group', copy=False)
    age = fields.Integer('Age')
    employment_date = fields.Date(string="Employment Date")
    confirmation_date = fields.Date(string="Confirmation Date")
    marriage_date = fields.Date(string="Marriage Date")
    is_part_time = fields.Boolean("Is Part Time")
    pf_acc_no = fields.Char('PF Account No.')
    facilities_cmp_ids = fields.Many2many(
        'sh.company.facilities', string="Facilities By Company")
    skype = fields.Char('Skype')
    whatsapp = fields.Char('Whatsapp')
    facebook = fields.Char('Facebook')
    instagram = fields.Char('Instagram')
    twitter = fields.Char('Twitter')
    personal_email = fields.Char('Personal Email')

    language_known_ids = fields.One2many('language.known', 'employee_id')
    skill_ids = fields.One2many('sh.emp.technical.skill', 'employee_id')
    non_tec_skill_ids = fields.One2many(
        'sh.emp.non.technical.skill', 'employee_id')
    pro_expe_ids = fields.One2many(
        'sh.emp.professional.experience', 'exp_employee_id')
    edu_qualification_ids = fields.One2many(
        'sh.education.qualification', 'edu_employee_id')
    certification_ids = fields.One2many('sh.certification', 'cert_employee_id')
    emergency_ids = fields.One2many(
        'hr.emp.emmergancy', 'employee_id', string='Employee Emergency Contact')
    hr_notifications = fields.Boolean(string="HR Notifications",default=True)
    project_notifications = fields.Boolean(string="Project Notifications",default=True)
    assignment_notifications = fields.Boolean(string="Assignment Notifications",default=True)
    support_notifications = fields.Boolean(string="Support Notifications",default=True)
    sales_notifications = fields.Boolean(string="Sales Notifications",default=True)


    @api.onchange('birthday')
    def compute_age(self):
        for rec in self:
            if rec.birthday:
                d1 = rec.birthday
                d2 = datetime.today()
                rec.age = relativedelta(d2, d1).years


class ShEmployeeExtraFields(models.Model):
    _inherit = 'hr.employee.public'

    work_country_id = fields.Many2one('res.country', string='Work Country')
    reference_by_id = fields.Many2one('hr.employee', string='Reference By')
    previous_nationality_id = fields.Many2one(
        'res.country', string='Previous Nationality')
    passport_country_id = fields.Many2one(
        'res.country', string='Passport Country')
    passport_issue = fields.Date(string='Passport Issue Date', default=lambda self: self._context.get(
        'date', fields.Date.context_today(self)))
    passport_expiry = fields.Date(string='Passport Expiry Date', default=lambda self: self._context.get(
        'date', fields.Date.context_today(self)))
    religion_id = fields.Many2one('sh.employee.religion', string='Religion')
    height = fields.Float("Height")
    weight = fields.Float("Weight")
    blood_group = fields.Selection([('A +ve', 'A +ve'), ('A -ve', 'A -ve'),
                                    ('B +ve', 'B +ve'), ('B -ve', 'B -ve'),
                                    ('AB +ve', 'AB +ve'), ('AB -ve', 'AB -ve'),
                                    ('O +ve', 'O +ve'), ('O -ve', 'O -ve'), ],
                                   string='Blood Group', copy=False)
    age = fields.Integer('Age')
    employment_date = fields.Date(string="Employment Date")
    confirmation_date = fields.Date(string="Confirmation Date")
    marriage_date = fields.Date(string="Marriage Date")
    is_part_time = fields.Boolean("Is Part Time")
    pf_acc_no = fields.Char('PF Account No.')
    facilities_cmp_ids = fields.Many2many(
        'sh.company.facilities', string="Facilities By Company")
    skype = fields.Char('Skype')
    whatsapp = fields.Char('Whatsapp')
    facebook = fields.Char('Facebook')
    instagram = fields.Char('Instagram')
    twitter = fields.Char('Twitter')
    personal_email = fields.Char('Personal Email')

    language_known_ids = fields.One2many('language.known', 'employee_id')
    skill_ids = fields.One2many('sh.emp.technical.skill', 'employee_id')
    non_tec_skill_ids = fields.One2many(
        'sh.emp.non.technical.skill', 'employee_id')
    pro_expe_ids = fields.One2many(
        'sh.emp.professional.experience', 'exp_employee_id')
    edu_qualification_ids = fields.One2many(
        'sh.education.qualification', 'edu_employee_id')
    certification_ids = fields.One2many('sh.certification', 'cert_employee_id')
    emergency_ids = fields.One2many(
        'hr.emp.emmergancy', 'employee_id', string='Employee Emergency Contact')
