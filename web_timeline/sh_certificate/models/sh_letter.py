# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api


class LetterTemplate(models.Model):
    _name = "sh.letter.template"
    _description = "Letter Template"

    name = fields.Char(string="Name")
    content_html = fields.Html(string="")
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        default=lambda self: self.env.company)


class ShLetter(models.Model):
    _name = "sh.letter"
    _inherit = ["mail.thread"]
    _description = "Letter"

    name = fields.Char("Main Subject")
    sh_layout_selection = fields.Selection([
        ('without_layout', 'Without Layout'),
        ('with_layout', 'With Layout')
    ], string='Layout Selection',default="without_layout")
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        default=lambda self: self.env.company)
    date = fields.Date("Date")
    letter_template = fields.Many2one(
        "sh.letter.template", string="Letter Template")
    reference = fields.Text("References")
    sh_partner_id = fields.Many2one("res.partner", string="Partner")
    employee_id = fields.Many2one("hr.employee", string="Employee")
    letter_content_html = fields.Html(string="")
    state = fields.Selection([
        ("draft", "Draft"),
        ("approve", "Approved"),
        ("cancel", "Cancel")], string="Status",
        readonly=True, index=True, copy=False, default="draft")
    sh_sequence = fields.Char("Sequence",default="Draft")

    @api.model
    def create(self, vals):
        vals.update(
            {"sh_sequence": self.env["ir.sequence"].next_by_code("letter.entry")})
        res = super(ShLetter, self).create(vals)
        res.onchange_template_letter()
        return res

    def button_approve(self):
        self.write({"state": "approve"})

    def button_set_to_draft(self):
        self.write({"state": "draft"})

    def button_cancel(self):
        self.write({"state": "cancel"})

    def action_letter_send(self):

        self.ensure_one()
        template_id = False
        template_id = self.env.ref("sh_certificate.email_template_edi_letter").id
        if template_id:
            key_count = True
        # try:
        #     compose_form_id = self.env.ref("mail.email_compose_message_wizard_form")
        # except ValueError:
        compose_form_id = False

        ctx = {
            "default_model": "sh.letter",
            "default_res_id": self.ids[0],
            "default_use_template":True,
            "default_template_id": template_id,
            "default_composition_mode": "comment",
            "mark_so_as_sent": True,
            "force_email": True
        }

        return {
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(compose_form_id, "form")],
            "view_id": compose_form_id,
            "target": "new",
            "context": ctx,
        }

    @api.onchange("letter_template", "sh_partner_id", "employee_id","sh_sequence")
    def onchange_template_letter(self):
        print("\n\n",self._fields)
        addr = ""
        addrs = ""
        emp_addrs = ""
        sh_emp_addrs = ""
        sh_partner_address = ""
        sh_address = ""
        emp_pc_addr = ""
        sh_emp_pc_addr = ""
        sh_street = ""
        sh_street2 = ""
        sh_city = ""
        sh_state = ""
        sh_country = ""
        sh_zips = ""
        sh_website = ""
        sh_email = ""
        sh_phone = ""
        sh_mobile = ""
        if self and self.letter_template and self.sh_partner_id and self.employee_id:
            #partner Details
            if self.sh_partner_id.street:
                addr += self.sh_partner_id.street+","
            if self.sh_partner_id.street2:
                addr += self.sh_partner_id.street2 + ","
            if self.sh_partner_id.city:
                addr += self.sh_partner_id.city + ","
            if self.sh_partner_id.state_id.name:
                addr += self.sh_partner_id.state_id.name + ","
            if self.sh_partner_id.country_id.name:
                addr += self.sh_partner_id.country_id.name + ","
            if self.sh_partner_id.zip:
                addr += self.sh_partner_id.zip
            sh_address = addr

            if self.sh_partner_id.street:
                sh_street = self.sh_partner_id.street
            else:
                sh_street = ""
            if self.sh_partner_id.street2:
                sh_street2 = self.sh_partner_id.street2
            else:
                sh_street2 = ""
            if self.sh_partner_id.city:
                sh_city = self.sh_partner_id.city
            else:
                sh_city = ""
            if self.sh_partner_id.state_id:
                sh_state = self.sh_partner_id.state_id.name
            else:
                sh_state = ""
            if self.sh_partner_id.country_id:
                sh_country = self.sh_partner_id.country_id.name
            else:
                sh_country = ""
            if self.sh_partner_id.zip:
                sh_zips = self.sh_partner_id.zip
            else:
                sh_zips = ""
            if self.sh_partner_id.website:
                sh_website = self.sh_partner_id.website
            else:
                sh_website = ""
            if self.sh_partner_id.email:
                sh_email = self.sh_partner_id.email
            else:
                sh_email = ""
            if self.sh_partner_id.phone:
                sh_phone = self.sh_partner_id.phone
            else:
                sh_phone = ""
            if self.sh_partner_id.mobile:
                sh_mobile = self.sh_partner_id.mobile
            else:
                sh_mobile = ""

            #Employee Details
            if self.employee_id.job_title:
                sh_job = self.employee_id.job_title
            else:
                sh_job = ""

            if self.employee_id.mobile_phone:
                emp_mobile_no = self.employee_id.mobile_phone
            else:
                emp_mobile_no = ""

            if self.employee_id.work_phone:
                emp_phone_no = self.employee_id.work_phone
            else:
                emp_phone_no = ""

            if self.employee_id.work_email:
                emp_work_email = self.employee_id.work_email
            else:
                emp_work_email = ""

            if self.employee_id.work_location_id.name:
                emp_work_location = self.employee_id.work_location_id.name
            else:
                emp_work_location = ""

            if self.employee_id.department_id.name:
                emp_department = self.employee_id.department_id.name
            else:
                emp_department = ""

            if self.employee_id.job_id.name:
                emp_job_position = self.employee_id.job_id.name
            else:
                emp_job_position = ""

            if self.employee_id.parent_id.name:
                emp_manager = self.employee_id.parent_id.name
            else:
                emp_manager = ""

            if self.employee_id.private_email:
                emp_private_email = self.employee_id.private_email
            else:
                emp_private_email = ""

            if self.employee_id.bank_account_id.acc_number:
                emp_account_number = self.employee_id.bank_account_id.acc_number
            else:
                emp_account_number = ""

            if self.employee_id.country_id.name:
                emp_nationality = self.employee_id.country_id.name
            else:
                emp_nationality = ""

            if self.employee_id.identification_id:
                emp_id_no = self.employee_id.identification_id
            else:
                emp_id_no = ""

            if self.employee_id.passport_id:
                employe_passport_id = self.employee_id.passport_id
            else:
                employe_passport_id = ""

            if self.employee_id.gender:
                emp_gender = self.employee_id.gender
            else:
                emp_gender = ""

            if self.employee_id.birthday:
                emp_birthday = self.employee_id.birthday
            else:
                emp_birthday = ""

            if self.employee_id.place_of_birth:
                emp_pob = self.employee_id.place_of_birth
            else:
                emp_pob = ""

            if self.employee_id.marital:
                emp_marital_status = self.employee_id.marital
            else:
                emp_marital_status = ""

            if self.employee_id.children:
                emp_children = self.employee_id.children
            else:
                emp_children = ""

            if self.employee_id.emergency_contact:
                emp_emergency_contact = self.employee_id.emergency_contact
            else:
                emp_emergency_contact = ""

            if self.employee_id.visa_no:
                emp_visa_no = self.employee_id.visa_no
            else:
                emp_visa_no = ""

            if self.employee_id.emergency_phone:
                emp_emergency_phone = self.employee_id.emergency_phone
            else:
                emp_emergency_phone = ""
            if self.employee_id.address_home_id:
                if self.employee_id.address_home_id.name:
                    emp_pc_addr += self.employee_id.address_home_id.name
                if self.employee_id.address_home_id.street:
                    emp_pc_addr += self.employee_id.address_home_id.street
                if self.employee_id.address_home_id.street2:
                    emp_pc_addr += self.employee_id.address_home_id.street2
                if self.employee_id.address_home_id.city:
                    emp_pc_addr += self.employee_id.address_home_id.city
                if self.employee_id.address_home_id.state_id.name:
                    emp_pc_addr += self.employee_id.address_home_id.state_id.name
                if self.employee_id.address_home_id.country_id.name:
                    emp_pc_addr += self.employee_id.address_home_id.country_id.name
                if self.employee_id.address_home_id.zip:
                    emp_pc_addr += self.employee_id.address_home_id.zip
                sh_emp_pc_addr = emp_pc_addr
            if self.letter_template.content_html:
                replace_temp = self.letter_template.content_html.replace("partner_name", self.sh_partner_id.name).replace("sh_sequence", self.sh_sequence).replace("partner_address", sh_address).replace("partner_street", sh_street).replace("partner_street2", sh_street2).replace("partner_city", sh_city).replace("partner_zip", str(sh_zips)).replace("partner_state", sh_state).replace("partner_email", sh_email).replace("partner_website", sh_website).replace("partner_country", sh_country).replace("partner_mobile", str(sh_mobile)).replace("partner_phone", str(sh_phone)).replace("employee_name", self.employee_id.name).replace("employee_job", sh_job).replace("employee_mobile", str(emp_mobile_no)).replace("employee_phone", str(emp_phone_no)).replace("employee_email", emp_work_email).replace("employee_address", emp_work_location).replace("employee_department", emp_department).replace("employee_job_position", emp_job_position).replace(
                    "employee_manager_name", emp_manager).replace("employee_pc_address", sh_emp_pc_addr).replace("emp_pc_private_email", emp_private_email).replace("employee_pc_account_number", str(emp_account_number)).replace("employee_citizenship_nationality", emp_nationality).replace("employee_citizenship_id_number", str(emp_id_no)).replace("empoyee_citizenship_passport_number", str(employe_passport_id)).replace("employee_citizenship_gender", emp_gender).replace("employee_citizenship_dob", str(emp_birthday)).replace("employee_citizenship_pob", str(emp_pob)).replace("employee_ms_marital_status", emp_marital_status).replace("employee_dependent_no_of_children", str(emp_children)).replace("employee_ec_emergency_contact", str(emp_emergency_contact)).replace("employee_wp_visa_no", str(emp_visa_no)).replace("employee_ec_emergency_phone", str(emp_emergency_phone))

                self.letter_content_html = replace_temp

        elif self and self.letter_template and not self.sh_partner_id and self.employee_id:
            #Employee Details

            if self.employee_id.job_title:
                sh_job = self.employee_id.job_title
            else:
                sh_job = ""

            if self.employee_id.mobile_phone:
                emp_mobile_no = self.employee_id.mobile_phone
            else:
                emp_mobile_no = ""

            if self.employee_id.work_phone:
                emp_phone_no = self.employee_id.work_phone
            else:
                emp_phone_no = ""

            if self.employee_id.work_email:
                emp_work_email = self.employee_id.work_email
            else:
                emp_work_email = ""

            if self.employee_id.work_location_id.name:
                emp_work_location = self.employee_id.work_location_id.name
            else:
                emp_work_location = ""

            if self.employee_id.department_id.name:
                emp_department = self.employee_id.department_id.name
            else:
                emp_department = ""

            if self.employee_id.job_id:
                emp_des_1 = self.employee_id.job_id.name
            else:
                emp_des_1 = ""

            if self.employee_id.parent_id.name:
                emp_manager = self.employee_id.parent_id.name
            else:
                emp_manager = ""

            if self.employee_id.private_email:
                emp_private_email = self.employee_id.private_email
            else:
                emp_private_email = ""

            if self.employee_id.bank_account_id.acc_number:
                emp_account_number = self.employee_id.bank_account_id.acc_number
            else:
                emp_account_number = ""

            if self.employee_id.country_id.name:
                emp_nationality = self.employee_id.country_id.name
            else:
                emp_nationality = ""

            if self.employee_id.identification_id:
                emp_id_no = self.employee_id.identification_id
            else:
                emp_id_no = ""

            if self.employee_id.passport_id:
                employe_passport_id = self.employee_id.passport_id
            else:
                employe_passport_id = ""

            if self.employee_id.gender:
                emp_gender = self.employee_id.gender
            else:
                emp_gender = ""

            if self.employee_id.birthday:
                emp_birthday = self.employee_id.birthday
            else:
                emp_birthday = ""

            if self.employee_id.place_of_birth:
                emp_pob = self.employee_id.place_of_birth
            else:
                emp_pob = ""

            if self.employee_id.marital:
                emp_marital_status = self.employee_id.marital
            else:
                emp_marital_status = ""

            if self.employee_id.children:
                emp_children = self.employee_id.children
            else:
                emp_children = ""

            if self.employee_id.emergency_contact:
                emp_emergency_contact = self.employee_id.emergency_contact
            else:
                emp_emergency_contact = ""

            if self.employee_id.visa_no:
                emp_visa_no = self.employee_id.visa_no
            else:
                emp_visa_no = ""

            if self.employee_id.emergency_phone:
                emp_emergency_phone = self.employee_id.emergency_phone
            else:
                emp_emergency_phone = ""
            if self.employee_id.address_home_id:
                if self.employee_id.address_home_id.name:
                    emp_addrs += self.employee_id.address_home_id.name
                if self.employee_id.address_home_id.street:
                    emp_addrs += self.employee_id.address_home_id.street
                if self.employee_id.address_home_id.street2:
                    emp_addrs += self.employee_id.address_home_id.street2
                if self.employee_id.address_home_id.city:
                    emp_addrs += self.employee_id.address_home_id.city
                if self.employee_id.address_home_id.state_id.name:
                    emp_addrs += self.employee_id.address_home_id.state_id.name
                if self.employee_id.address_home_id.country_id.name:
                    emp_addrs += self.employee_id.address_home_id.country_id.name
                if self.employee_id.address_home_id.zip:
                    emp_addrs += self.employee_id.address_home_id.zip
                sh_emp_addrs = emp_addrs

            if self.letter_template.content_html:
                replace_temp = self.letter_template.content_html.replace("employee_name", self.employee_id.name).replace("sh_sequence", self.sh_sequence).replace("employee_job", sh_job).replace("employee_mobile", str(emp_mobile_no)).replace("employee_phone", str(emp_phone_no)).replace("employee_email", emp_work_email).replace("employee_address", emp_work_location).replace("employee_department", emp_department).replace("employee_job_position", emp_des_1).replace("employee_manager_name", emp_manager).replace("employee_pc_address", sh_emp_addrs).replace("emp_pc_private_email", emp_private_email).replace("employee_pc_account_number", str(emp_account_number)).replace(
                    "employee_citizenship_nationality", emp_nationality).replace("employee_citizenship_id_number", str(emp_id_no)).replace("empoyee_citizenship_passport_number", str(employe_passport_id)).replace("employee_citizenship_gender", emp_gender).replace("employee_citizenship_dob", str(emp_birthday)).replace("employee_citizenship_pob", str(emp_pob)).replace("employee_ms_marital_status", emp_marital_status).replace("employee_dependent_no_of_children", str(emp_children)).replace("employee_ec_emergency_contact", str(emp_emergency_contact)).replace("employee_wp_visa_no", str(emp_visa_no)).replace("employee_ec_emergency_phone", str(emp_emergency_phone))

                self.letter_content_html = replace_temp

        elif self and self.letter_template and self.sh_partner_id and not self.employee_id:
            #partner Details
            if self.sh_partner_id.street:
                addrs += self.sh_partner_id.street+","
            if self.sh_partner_id.street2:
                addrs += self.sh_partner_id.street2 + ","
            if self.sh_partner_id.city:
                addrs += self.sh_partner_id.city + ","
            if self.sh_partner_id.state_id.name:
                addrs += self.sh_partner_id.state_id.name + ","
            if self.sh_partner_id.country_id.name:
                addrs += self.sh_partner_id.country_id.name + ","
            if self.sh_partner_id.zip:
                addrs += self.sh_partner_id.zip
            sh_partner_address = addrs

            if self.sh_partner_id.street:
                sh_street = self.sh_partner_id.street
            else:
                sh_street = ""
            if self.sh_partner_id.street2:
                sh_street2 = self.sh_partner_id.street2
            else:
                sh_street2 = ""
            if self.sh_partner_id.city:
                sh_city = self.sh_partner_id.city
            else:
                sh_city = ""
            if self.sh_partner_id.state_id:
                sh_state = self.sh_partner_id.state_id.name
            else:
                sh_state = ""
            if self.sh_partner_id.country_id:
                sh_country = self.sh_partner_id.country_id.name
            else:
                sh_country = ""
            if self.sh_partner_id.zip:
                sh_zips = self.sh_partner_id.zip
            else:
                sh_zips = ""
            if self.sh_partner_id.website:
                sh_website = self.sh_partner_id.website
            else:
                sh_website = ""
            if self.sh_partner_id.email:
                sh_email = self.sh_partner_id.email
            else:
                sh_email = ""
            if self.sh_partner_id.phone:
                sh_phone = self.sh_partner_id.phone
            else:
                sh_phone = ""
            if self.sh_partner_id.mobile:
                sh_mobile = self.sh_partner_id.mobile
            else:
                sh_mobile = ""

            if self.letter_template.content_html:
                replace_temp = self.letter_template.content_html.replace(
                    "partner_name",self.sh_partner_id.name).replace("partner_address", sh_partner_address).replace("sh_sequence", self.sh_sequence).replace("partner_street", sh_street).replace("partner_street2", sh_street2).replace("partner_city", sh_city).replace("partner_zip", str(sh_zips)).replace("partner_state", sh_state).replace("partner_email", sh_email).replace("partner_website", sh_website).replace(
                    "partner_country", sh_country).replace("partner_mobile", str(sh_mobile)).replace("partner_phone", str(sh_phone))  # .replace("partner_id",self.sh_partner_id.name).replace("partner_address",sh_partner_address).replace("mobile",str(self.sh_partner_id.mobile))#.replace("empaddress",sh_emp_addr).replace("employee_id",self.employee_id.name).replace("contact",self.employee_id.mobile_phone)
                self.letter_content_html = replace_temp

        else:
            if self.letter_template.content_html:
                self.letter_content_html = self.letter_template.content_html
