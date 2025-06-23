# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields,models
from datetime import datetime
import requests
import json

class ImportTask(models.Model):
    _inherit = "sh.import.base"
    

    import_timesheet=fields.Boolean("Import Timesheet")
    records_per_page_timesheet = fields.Integer("No of Timesheet per Page")
    current_import_page_timesheet = fields.Integer("Current Timesheet Page",default=0) 
    timesheet_ids = fields.Char("Timesheets")
    sh_from_date_timesheet=fields.Datetime("From Date(timesheet)")
    sh_to_date_timesheet=fields.Datetime("To Date(timesheet)")

    def import_timesheet_filtered_to_queue(self):
        ''' ========== Import Filtered tasks ================= 
        between from date and end date ==================  ''' 

        confid = self.env['sh.import.base'].search([],limit=1)  
        if confid.import_timesheet:
            response = requests.get('''%s/api/public/account.analytic.line?query={id,write_date}&filter=[["write_date",">=","%s"],["write_date","<=","%s"],["company_id","=",1]]''' 
                %(confid.base_url,str(confid.sh_from_date_timesheet),str(confid.sh_to_date_timesheet)))
            
            if response.status_code==200:
                response_json = response.json()
                print("\n\n=====response_json",response_json)
                if response_json.get('result'):
                    confid.timesheet_ids=[r['id'] for r in response_json.get('result')]
                else:
                    confid.timesheet_ids=False


    def import_timsheet_cron(self):
        ''' ========== Import Timesheet ============ '''
        
        confid = self.env['sh.import.base'].search([],limit=1)
        if confid.import_timesheet:
            confid.current_import_page_timesheet += 1
            response = requests.get('''%s/api/public/account.analytic.line?query={*}&page_size=%s&page=%s&filter=[["company_id","=",1]]''' 
                %(confid.base_url,confid.records_per_page_timesheet,confid.current_import_page_timesheet))
            response_json = response.json()
            count = 0
            failed = 0
            # if response.status_code==200:
            #     if 'count' in response_json and confid.records_per_page_timesheet != response_json['count'] : 
            #         confid.import_timesheet = False
            #         confid.current_import_page_timesheet = 0
            timesheets = confid.timesheet_ids.strip('][').split(', ')
            for timesheet in timesheets[0:200]:
                response = requests.get('''%s/api/public/account.analytic.line?query={*}&filter=[["company_id","=",1],["id","=",%s]]''' 
                    %(confid.base_url,timesheet))
                response_json = response.json()  
                if response.status_code==200:  
                    for data in response_json['result']:
                        timesheet_vals = confid.process_timesheet_data(data)
                        domain = [('remote_account_analytic_line_id', '=', data['id'])]
                        find_timesheet = self.env['account.analytic.line'].search(domain)
                        # try:
                        if find_timesheet:
                            count += 1
                            find_timesheet.write(timesheet_vals)                           
                        else:
                            count += 1
                            # print("\n\n\n",timesheet_vals)
                            if not timesheet_vals.get('employee_id') and timesheet_vals.get('account_id'): 
                                print("\n===e --------- employee not found")
                            elif not timesheet_vals.get('account_id'): 
                                print("\n===e --------- account_id not found")
                                

                            else:
                                create_timesheet=self.env['account.analytic.line'].create(timesheet_vals) 

                    # except Exception as e:
                    #     failed += 1
                    #     vals = {
                    #         "name": data['id'],
                    #         "error": e,
                    #         "import_json" : data,
                    #         "field_type": "timesheet",                           
                    #         "datetime": datetime.now(),
                    #         "base_config_id": confid.id,
                    #     }
                    #     self.env['sh.import.failed'].create(vals) 
            confid.timesheet_ids='['+', '.join([str(elem) for elem in timesheets[200:]])+']'           
            if count > 0:              
                vals = {
                    "name": confid.name,
                    "state": "success",
                    "field_type": "timesheet",
                    "error": "%s Timesheet Imported Successfully" %(count - failed),
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)
            if failed > 0:
                vals = {
                    "name": confid.name,
                    "state": "error",
                    "field_type": "timesheet",
                    "error": "%s Failed To Import" %(failed),
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)

            # else:
            #     vals = {
            #         "name": confid.name,
            #         "state": "error",
            #         "field_type": "timesheet",
            #         "error": response.text,
            #         "datetime": datetime.now(),
            #         "base_config_id": confid.id,
            #         "operation": "import"
            #     }
            #     self.env['sh.import.base.log'].create(vals)  

    def update_timsheet_cron(self):
        ''' ========== Import Timesheet ============ '''
        
        confid = self.env['sh.import.base'].search([],limit=1)
        if confid.import_timesheet:
            count = 0
            failed = 0
           
            timesheets = confid.timesheet_ids.strip('][').split(', ')
            for timesheet in timesheets[0:200]:
                response = requests.get('''%s/api/public/account.analytic.line?query={*}&filter=[["company_id","=",1],["id","=",%s]]''' 
                    %(confid.base_url,timesheet))
                response_json = response.json()  
                if response.status_code==200:  
                    for data in response_json['result']:
                        timesheet_vals = confid.process_timesheet_data(data)
                        domain = [('remote_account_analytic_line_id', '=', data['id'])]
                        find_timesheet = self.env['account.analytic.line'].search(domain)
                        # try:
                        if find_timesheet:
                            count += 1
                            find_timesheet.write(timesheet_vals)                           
                        else:
                            count += 1
                            # print("\n\n\n",timesheet_vals)
                            if not timesheet_vals.get('employee_id') and timesheet_vals.get('account_id'): 
                                print("\n===e --------- employee not found")
                            elif not timesheet_vals.get('account_id'): 
                                print("\n===e --------- account_id not found")
                                

                            else:
                                create_timesheet=self.env['account.analytic.line'].create(timesheet_vals) 

                    # except Exception as e:
                    #     failed += 1
                    #     vals = {
                    #         "name": data['id'],
                    #         "error": e,
                    #         "import_json" : data,
                    #         "field_type": "timesheet",                           
                    #         "datetime": datetime.now(),
                    #         "base_config_id": confid.id,
                    #     }
                    #     self.env['sh.import.failed'].create(vals) 
            confid.timesheet_ids='['+', '.join([str(elem) for elem in timesheets[200:]])+']'           
            if count > 0:              
                vals = {
                    "name": confid.name,
                    "state": "success",
                    "field_type": "timesheet",
                    "error": "%s Timesheet update Successfully" %(count - failed),
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)
            if failed > 0:
                vals = {
                    "name": confid.name,
                    "state": "error",
                    "field_type": "timesheet",
                    "error": "%s Failed To Import" %(failed),
                    "datetime": datetime.now(),
                    "base_config_id": confid.id,
                    "operation": "import"
                }
                self.env['sh.import.base.log'].create(vals)

            # else:
            #     vals = {
            #         "name": confid.name,
            #         "state": "error",
            #         "field_type": "timesheet",
            #         "error": response.text,
            #         "datetime": datetime.now(),
            #         "base_config_id": confid.id,
            #         "operation": "import"
            #     }
            #     self.env['sh.import.base.log'].create(vals)  
                



    def process_timesheet_data(self,timesheet):
        ''' ============= Prepare Timesheet data =============  '''
        # timesheet_list=[]
        # for timesheet in data:
        
        timesheet_vals={
            'amount':timesheet.get('amount'),
            'display_name':timesheet.get('display_name'),
            'remote_account_analytic_line_id':timesheet.get('id'),
            'name':timesheet.get('name'),
            'unit_amount':timesheet.get('unit_amount'),
            'unit_amount_invoice':timesheet.get('unit_amount_invoice'),
            'company_id':1,
            'is_so_line_edited':timesheet.get('is_so_line_edited'),
            'ref':timesheet.get('ref'),
        }
        # ======== Get Employee if already created or create =========
        if timesheet.get('employee_id') and timesheet.get('employee_id')!=0:
            domain = [('remote_hr_employee_id', '=', timesheet['employee_id'])]
            find_employee = self.env['hr.employee'].search(domain)
            if find_employee:
                timesheet_vals['employee_id'] = find_employee.id

        if timesheet.get('timesheet_invoice_type') and timesheet.get('timesheet_invoice_type').get('sh_api_current_state'):
            if timesheet.get('timesheet_invoice_type').get('sh_api_current_state')=='non_billable_project':
                timesheet_vals['timesheet_invoice_type'] = 'non_billable' 
            else:
                timesheet_vals['timesheet_invoice_type'] = timesheet.get('timesheet_invoice_type').get('sh_api_current_state')  


        if timesheet.get('manager_id') and timesheet.get('manager_id')!=0:
            domain = [('remote_hr_employee_id', '=', timesheet['manager_id'])]
            find_employee = self.env['hr.employee'].search(domain)
            if find_employee:
                timesheet_vals['manager_id'] = find_employee.id

        if timesheet.get('order_id') and timesheet.get('order_id')!=0:
            domain = [('remote_sale_order_id', '=', timesheet['order_id'])]
            find_order = self.env['sale.order'].search(domain)
            if find_order:
                timesheet_vals['order_id'] = find_order.id

        if timesheet.get('so_line') and timesheet.get('so_line')!=0:
            domain = [('remote_sale_order_line_id', '=', timesheet['so_line'])]
            find_order = self.env['sale.order.line'].search(domain)
            if find_order:
                timesheet_vals['so_line'] = find_order.id

        if timesheet.get('date'):
            date_time=datetime.strptime(timesheet.get('date'),'%Y-%m-%d')
            date_time=date_time.strftime('%Y-%m-%d')
            timesheet_vals['date']=date_time

        if timesheet.get('start_date'):

            date_time = datetime.strptime( timesheet.get('start_date'), '%Y-%m-%d-%H-%M-%S')
            date_time = date_time.strftime('%Y-%m-%d %H:%M:%S')
            # date_time=datetime.strptime(timesheet.get('start_date'),'%Y-%m-%d-%H-%M-%S')
            # date_time=date_time.strftime('%Y-%m-%d-%H-%M-%S')
            timesheet_vals['start_date']=date_time

        if timesheet.get('end_date'):
            date_time = datetime.strptime( timesheet.get('end_date'), '%Y-%m-%d-%H-%M-%S')
            date_time = date_time.strftime('%Y-%m-%d %H:%M:%S')
            timesheet_vals['end_date']=date_time

        # ======== Get Partner if already created or create =========
    
        if timesheet.get('partner_id'):
            domain = [('remote_res_partner_id', '=', timesheet['partner_id'])]
            find_customer = self.env['res.partner'].search(domain)
            if find_customer:
                timesheet_vals['partner_id'] = find_customer.id

        if timesheet.get('product_id'):
            domain = [('remote_product_product_id', '=', timesheet['product_id'])]
            find_product = self.env['product.product'].search(domain)
            if find_product:
                timesheet_vals['product_id'] = find_product.id

        if timesheet.get('project_id'):
            domain = [('remote_project_project_id', '=', timesheet['project_id'])]
            find_project = self.env['project.project'].search(domain)
            if find_project:
                timesheet_vals['project_id'] = find_project.id

                timesheet_vals['account_id'] = find_project.analytic_account_id.id

        if timesheet.get('task_id'):
            domain = [('remote_project_task_id', '=', timesheet['task_id'])]
            find_task = self.env['project.task'].search(domain)
            if find_task:
                timesheet_vals['task_id'] = find_task.id

        if timesheet.get('ticket_id'):
            domain = [('remote_sh_helpdesk_ticket_id', '=', timesheet['ticket_id'])]
            find_ticket = self.env['sh.helpdesk.ticket'].search(domain)
            if find_ticket:
                timesheet_vals['ticket_id'] = find_ticket.id

        if timesheet.get('timesheet_invoice_id'):
            domain = [('remote_account_move_id', '=', timesheet['timesheet_invoice_id'])]
            find_invoice = self.env['account.move'].search(domain)
            if find_invoice:
                timesheet_vals['timesheet_invoice_id'] = find_invoice.id

        if timesheet.get('department_id'):
            domain = [('remote_hr_department_id', '=', timesheet['department_id'])]
            find_department = self.env['hr.department'].search(domain)
            if find_department:
                timesheet_vals['department_id'] = find_department.id
                    
        # ======== Get User if already created or create =========
        
        if timesheet.get('user_id') and timesheet.get('user_id')!=0:
            domain_by_id = [('remote_res_user_id','=',timesheet['user_id'])]
            find_user_id=self.env['res.users'].search(domain_by_id)
            if find_user_id:
                timesheet_vals['user_id']=find_user_id.id 
    
        
        # ======== Get tags if already created or create =========            
                    
        if timesheet.get('tag_ids'):
            tag_ids=[]
            for tag in timesheet.get('tag_ids'):
                domain = [('remote_project_tag_id','=',tag['id'])]
                find_tag = self.env['project.tags'].search(domain)
                if find_tag:
                    tag_ids.append((4,find_tag.id))
                else:
                    tag_vals = {
                        'remote_project_tag_id' : tag['id'],
                        'color' : tag['color'],
                        'display_name':tag['display_name'],
                        'name':tag['name'],
                        }
                    tag_id=self.env['project.tags'].create(tag_vals)
                    if tag_id:
                        tag_ids.append((4,tag_id.id))
            if tag_ids:
                timesheet_vals['tag_ids']=tag_ids
        # if not find_timesheet:
        #     if timesheet_vals and timesheet_vals.get('employee_id'):
        return timesheet_vals

            #         timesheet_list.append((0,0,timesheet_vals))
            # else:
            #     find_timesheet.write(timesheet_vals)
        