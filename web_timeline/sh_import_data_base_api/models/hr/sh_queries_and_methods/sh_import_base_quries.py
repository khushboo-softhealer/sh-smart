# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.


from odoo import models
from datetime import datetime

# ============================= hr.salary.rule.category =============================

hr_salary_rule_category_child = '''id,name,display_name,code,note'''

hr_salary_rule_category = '''%s,children_ids{%s}''' % (
    hr_salary_rule_category_child, hr_salary_rule_category_child)

# ================================== hr.rule.input ==================================

hr_rule_input = '''id,name,display_name,code,
input_id{id,name,code,condition_python,condition_select,amount_select,category_id}'''

# ================================== hr.salary.rule ==================================

hr_salary_rule_child = '''
    id,name,display_name,sequence,amount_fix,amount_percentage,amount_percentage_base,
    amount_python_compute,code,quantity,active,appears_on_payslip,amount_select,
    condition_range,condition_python,condition_range_min,condition_range_max,
    note,condition_select,
    parent_rule_id,register_id,analytic_account_id,account_tax_id,account_debit,account_credit,
    category_id,input_ids,
    child_ids
'''

hr_salary_rule = '''%s,child_ids{%s}''' % (
    hr_salary_rule_child, hr_salary_rule_child)

# ==========================================================================================================================

sh_college = '''id,name,street,street2,zip,city,colloge_contact_no,tpo_contact_no,email,display_name,
stage_id{id,name,display_name,fold,sequence},state_id{name,code},country_id{name},contact_person_ids'''

sh_placement = '''name,date,note,id,display_name,
    placement_line{id,display_name,total_candidate_applied,selected_candidate,present_candidate,absent_candidate,college_id}'''

partner_id_without_child_ids = '''
    id,name,vat,title,ref,type,website,supplier,street,street2,city,state_id{name,code},country_id{name},zip,email,
    is_company,phone,mobile,company_type,customer
'''

# res.partner
partner_id = '''%s,child_ids{%s}
            ''' % (partner_id_without_child_ids, partner_id_without_child_ids)

# res.user
user_id = '''id,active,active_partner,alias_contact,barcode,city,color,comment,contact_address,country_id{name},
            lang,login,mobile,name,new_password,partner_id{%s},credit_limit,customer,display_name,email,email_formatted,
            password,phone,state,state_id{name,code},street,street2,supplier,type,vat,tz,tz_offset
            ''' % (partner_id)

# hr.employee
hr_employee_without_child = '''
    id,active,additional_note,birthday,certificate,color,country_of_birth{name},display_name,emergency_contact,
    emergency_phone,gender,google_drive_link,identification_id,km_home_work,marital,name,notes,passport_id,
    permit_no,place_of_birth,sinid,spouse_birthdate,spouse_complete_name,ssnid,study_field,study_school,
    pf_acc_no,facilities_cmp_ids{id,name,display_name},skype,whatsapp,facebook,instagram,twitter,personal_email,sh_work_hours_notify,
    newly_hired_employee,payslip_count,is_remote_employee,timesheet_cost,attendance_activity,
    sh_bank_account,send_payslip,assets_count,requests_count,is_address_home_a_company,children,job_title,
    mobile_phone,work_email,sh_attendance_state,
    category_ids{id,name,color,display_name},barcode,pin,
    attendance_state,vehicle,contracts_count,remaining_leaves,current_leave_state,leave_date_from,
    leave_date_to,leaves_count,show_leaves,is_absent_totay,passport_issue,passport_expiry,height,
    weight,blood_group,age,joining_date,employment_date,confirmation_date,marriage_date,is_part_time,
    tz,visa_expire,visa_no,work_email,work_phone,country_id{name},user_id,
    contract_id{id,name,wage,activity_user_id,struct_id{id,name,code}},
    date_of_joining,
    resource_calendar_id,
    department_id,job_id,
    address_home_id,
    address_id,
    expense_manager_id,
    passport_country_id{name},
    currency_id{name},
    work_country_id{name},
    religion_id{id,name,display_name},
    current_leave_id{id,name,color_name,request_unit},
    coach_id{id,name},
    reference_by_id{id,name},
    hr_manager{id,name},
    resource_id{
        id,name,active,resource_type,time_efficiency,tz,display_name,user_id,calendar_id
    },
    skill_ids{
        id,level,display_name,skill_id{id,name,display_name}
    },
    non_tec_skill_ids{
        id,level,display_name,non_tec_skill_id{id,name,display_name}
    },
    pro_expe_ids{id,location,display_name,job_title_id{id,name},start_date,end_date},
    edu_qualification_ids,certification_ids,asset_ids,emergency_ids
'''


hr_employee = '''%s,child_ids{%s}''' % (
    hr_employee_without_child, hr_employee_without_child)

job_id = '''id,requirements,description,display_name,name,expected_employees,no_of_employee,no_of_recruitment,no_of_hired_employee,
    employee_ids'''

# hr.department
hr_department = '''id,name,display_name,color,complete_name,note,manager_id,member_ids,
                jobs_ids,*'''

# # hr.recruitment.stage
hr_recruitment_stage = '''id,name,sequence,requirements,fold,legend_blocked,legend_done,
    legend_normal,display_name,job_id{id,name}'''

# hr.applicant
hr_applicant = '''
        id,name,partner_name,email_from,email_cc,partner_phone,partner_mobile,salary_expected,salary_proposed,description,
        active,color,day_close,day_open,delay_close,display_name,employee_name,probability,salary_proposed_extra,
        salary_expected_extra,user_email,legend_blocked,legend_done,legend_normal,availability,date_closed,date_last_stage_update,
        date_open,priority,kanban_state,attachment_number,sh_hr_placement_is_confirm,hide_button_bool,interview_type,
        sh_hr_placement_schedule_datetime,placement_id,
        college_id,interview_ids,reject_reason_id,
        medium_id{id,name,display_name,active},
        categ_ids{id,name,color,display_name},
        type_id{id,name,sequence,display_name},
        source_id{id,name,display_name},
        partner_id,
        department_id{id,name},
        last_stage_id,
        stage_id,
        user_id
    '''

# hr.leave.type
hr_leave_type = '''id,name,sequence,active,max_leaves,leaves_taken,remaining_leaves,virtual_remaining_leaves,
                group_days_leave,valid,unpaid,display_name,color_name,time_type,request_unit,double_validation,
                validation_type,allocation_type,sh_leave_attachment,leave_before_day_alert,leave_before_days,
                no_of_days,timesheet_generate,timesheet_project_id,timesheet_task_id'''

hr_leave_allocation_without_child_ids = '''
    id,name,notes,number_of_days,number_of_days_display,number_of_hours_display,duration_display,
    can_reset,can_approve,display_name,state,type_request_unit,holiday_type,accrual,date_from,date_to,date_start,date_end,nextcall,
    holiday_status_id,department_id{id,name},first_approver_id,employee_id,category_id{id,name,color,display_name,employee_ids}
'''

hr_leave_allocation = '''%s, linked_request_ids{%s}
            ''' % (hr_leave_allocation_without_child_ids, hr_leave_allocation_without_child_ids)

# account.analytic.line (one2many)
timesheet_ids = '''*,employee_id,tag_ids{*},user_id,partner_id'''

hr_leave_without_child_ids = '''
    id,state,validation_type,tz,holiday_type,leave_type_request_unit,request_hour_from,request_hour_to,request_date_from_period,
    name,report_note,tz_mismatch,notes,number_of_days,number_of_days_display,number_of_hours_display,duration_display,can_reset,can_approve,
    request_unit_half,request_unit_hours,activity_summary,display_name,date_from,date_to,
    created_leave,automatic,sh_timesheet_count,sh_attendance_count,leaves_count,leave_taken_3_month,custom_hour_from,
    custom_hour_to,available_leaves,total_taken_leave_in_current_contract,bool_field,alert_leave,leave_days,warning,
    is_desc_hide,leave_attach,is_sick_leave,request_date_from,request_date_to,
    department_id{id,name},user_id,employee_id,holiday_status_id,manager_id,timesheet_ids{%s}
''' % (timesheet_ids)

hr_leave = '''%s,linked_request_ids{%s}
        ''' % (hr_leave_without_child_ids, hr_leave_without_child_ids)
# _________________________________________________________________________________________________

hr_payroll_structure_child = '''
				id,name,display_name,code,note,rule_ids
'''
# hr_payroll_structure
hr_payroll_structure = '''%s''' % (hr_payroll_structure_child)

hr_contract = '''
   id,name,sh_annexure_b_notes,sh_contract_bond_detail_report,signature_date,allocation_id{%s},display_name,wage,visa_no,permit_no,notes,state,bond,period,bond_duration,cheque_amount,cheque_number,contract_period,contract_type,days_extend,digital_signature,leave_payment_done,date,date_start,date_end,trial_date_end,
	employee_id,department_id,job_id,resource_calendar_id,type_id,degree_ids,struct_id,journal_id{*,account_control_ids{*,tag_ids{*},tax_ids{*},user_type_id{*}}},
    sh_contract_goal_ids{id,name,display_name,sequence},sh_contract_improvement_ids{id,name,display_name,sequence}
''' % (hr_leave_allocation)



hr_payslip_run = '''id,name,display_name,bank_format,bank_ref,credit_note,sh_payslip_count,trancation_date,state,date_start,date_end,
					
					slip_ids,journal_id{*,account_control_ids{*,tag_ids{*},tax_ids{*},user_type_id{*}}},default_payment{id,name,display_name,default_formate,total_amount}'''


hr_payslip_work_day = '''id,name,display_name,code,number_of_hours,number_of_days,sequence
	,payslip_id,contract_id{id,name,wage,activity_user_id,struct_id{id,name,code}}'''

hr_payslip = '''id,name,display_name,note,number,paid,payslip_count,credit_note,state,date,date_from,date_to,

	contract_id{id,name,wage,activity_user_id,struct_id{id,name,code}},employee_id,details_by_salary_rule_category,input_line_ids,line_ids,payslip_run_id,struct_id{id,name,code},
	journal_id{*,account_control_ids{*,tag_ids{*},tax_ids{*},user_type_id{*}}}'''

hr_payslip_line = '''id,name,display_name,note,code,quantity,rate,total,sequence,condition_python,condition_range,condition_range_max,condition_range_min,amount_select,appears_on_payslip,amount,amount_fix,amount_percentage,amount_percentage_base,amount_python_compute,condition_select,
	account_credit,account_debit,category_id,child_ids,contract_id{id,name,wage,activity_user_id,struct_id{id,name,code}},employee_id,employee_id,input_ids,salary_rule_id,register_id,
	slip_id{id,name,date_from,date_to,employee_id,journal_id}'''

hr_payslip_input = '''id,name,display_name,code,amount,sequence,payslip_id{id,name,date_from,date_to,employee_id,journal_id},
	contract_id{id,name,wage,activity_user_id,struct_id{id,name,code}}'''


hr_contribution_register = '''id,name,display_name,note,partner_id,register_line_ids'''


hr_attendance = '''id,display_name,worked_hours,att_duration,check_in_url,check_out_url,in_latitude,in_longitude,message_in,message_out,other_data,out_latitude,out_longitude,sh_break_reason,sh_break_duration,sh_break_over,sh_duration,sh_remark,total_time,check_in,check_out,sh_break_start_date,sh_break_start,sh_break_end,
        employee_id,department_id'''

# ==============================================  HR Basics ================================================================

# ============================= hr.salary.rule.category =============================

hr_salary_rule_category_child = '''id,name,display_name,code,note'''

hr_salary_rule_category = '''%s,children_ids{%s}''' % (
    hr_salary_rule_category_child, hr_salary_rule_category_child)

# ================================== hr.rule.input ==================================

hr_rule_input = '''id,name,display_name,code,
input_id{id,name,code,condition_python,condition_select,amount_select,category_id}'''

# ================================== hr.salary.rule ==================================

hr_salary_rule_child = '''
    id,name,display_name,sequence,amount_fix,amount_percentage,amount_percentage_base,
    amount_python_compute,code,quantity,active,appears_on_payslip,amount_select,
    condition_range,condition_python,condition_range_min,condition_range_max,
    note,condition_select,
    parent_rule_id,register_id,analytic_account_id,account_tax_id,account_debit,account_credit,
    category_id,input_ids,
    child_ids
'''

hr_salary_rule = '''%s,child_ids{%s}''' % (
    hr_salary_rule_child, hr_salary_rule_child)

# _________________________________________________________________________________________________

sh_certification = ''' id,display_name,course,comp_year,level_completion,certificate,cert_employee_id'''

sh_asset_without_parent = '''id,name,display_name,allocated,amount,bill_number,is_child,is_parent,sh_ebs_barcode,sh_ebs_barcode_img,warranty_month,state,
	warranty_date,warranty_expiry_date,
	vendor_id,asset_category_id{id,name,display_name}'''

sh_asset = '''%s,parent{%s}''' % (
    sh_asset_without_parent, sh_asset_without_parent)

sh_education_qualification = ''' id,display_name,institutes,score,transcript,quo_year,
								edu_employee_id,degree_id{id,name,display_name}'''

hr_emp_emmergancy = '''id,name,contact_number,display_name,relation_id{id,name,display_name}'''


class InheritImportBase(models.Model):
    _inherit = "sh.import.base"

    # ========================== Quries ==========================

    query = {
        'hr_salary_rule_category': hr_salary_rule_category,
        'hr_rule_input': hr_rule_input,
        'hr_salary_rule': hr_salary_rule,
        'sh_college': sh_college,
        'sh_placement': sh_placement,
        'partner_id_without_child_ids': partner_id_without_child_ids,
        'partner_id': partner_id,
        'user_id': user_id,
        'hr_employee': hr_employee,
        'hr_department': hr_department,
        'hr_recruitment_stage': hr_recruitment_stage,
        'hr_applicant': hr_applicant,
        'hr_leave_type': hr_leave_type,
        'hr_leave_allocation_without_child_ids': hr_leave_allocation_without_child_ids,
        'hr_leave_allocation': hr_leave_allocation,
        'timesheet_ids': timesheet_ids,
        'hr_leave_without_child_ids': hr_leave_without_child_ids,
        'hr_leave': hr_leave,
        'hr_emp_emmergancy': hr_emp_emmergancy,
    }

    query_dict = {
        'hr_salary_rule_category': hr_salary_rule_category,
        'hr_rule_input': hr_rule_input,
        'hr_salary_rule': hr_salary_rule,
        'hr_contract': hr_contract,
        'hr_payroll_structure': hr_payroll_structure,
        'hr_payslip_run': hr_payslip_run,
        'hr_payslip_work_day': hr_payslip_work_day,
        'hr_payslip': hr_payslip,
        'hr_payslip_line': hr_payslip_line,
        'hr_contribution_register': hr_contribution_register,
        'hr_payslip_input': hr_payslip_input,
        'hr_attendance': hr_attendance,
        'sh_certification': sh_certification,
        'sh_asset_without_parent': sh_asset_without_parent,
        'sh_asset': sh_asset,
        'sh_education_qualification': sh_education_qualification,
    }
