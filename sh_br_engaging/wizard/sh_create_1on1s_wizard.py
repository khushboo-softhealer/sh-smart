# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import _, api, fields, models
from datetime import datetime
from odoo.exceptions import ValidationError, AccessError
# from odoo.exceptions import AccessError





class Create1ons(models.TransientModel):
    _name = "sh.create.1on1s.wizard"
    _description = "Model for Create 1-on-1s from kanban and list view"
    _managers_level = 10


    def _get_employee_domain(self):
        list_of_child_ids = []
        # === FIND THE EMPLOYEE OF CURRENT LOGIN USER ===  
        employee=self.env.user.employee_id
        if employee:
            # ==========================================================================
            # === CHECK IF WE FOUND CHILD RECORD OF EMPLOYEE OF NOT ===  
            # ==========================================================================
            if employee.subordinate_ids :
                for child in employee.subordinate_ids :
                    list_of_child_ids.append(child.id)
            else : 
                list_of_child_ids = list_of_child_ids

            # ==========================================================================
            # === GET THE ALL PARENT IDS FROM THIS CUSTOM METHOD ===
            # ==========================================================================
            result=self.get_employee_organisation(employee.id)


            # Extract ids of managers and children
            manager_ids = [manager['id'] for manager in result.get('managers', [])]

            # Combine manager ids and children ids into one list
            final_ids_list = manager_ids + list_of_child_ids
            domain= [('id', 'in', final_ids_list)]

            return domain

    name = fields.Char("Agenda")
    sh_agenda_ids = fields.Many2many('sh.manage.agenda',string='Agenda Ids')
    # sh_store_domain = fields.Char("Used To Store The Domain", compute="get_related_employee_data")
    sh_employee_id = fields.Many2one('hr.employee', "Employee Name",domain=_get_employee_domain)
    sh_your_notes = fields.Text("Your Notes")
    sh_my_notes = fields.Text("My Notes")
    sh_private_notes = fields.Text("Private Notes")




    # sh_talking_point_id=fields.Many2one('sh.talking.points','Talking Point Id')

    def _prepare_employee_data(self, employee):
        job = employee.sudo().job_id
        return dict(
            id=employee.id,
            name=employee.name,
            link='/mail/view?model=%s&res_id=%s' % ('hr.employee.public', employee.id,),
            job_id=job.id,
            job_name=job.name or '',
            job_title=employee.job_title or '',
            direct_sub_count=len(employee.child_ids - employee),
            indirect_sub_count=employee.child_all_count,
        )


    def _check_employee(self, employee_id):
        if not employee_id:  # to check
            return None
        employee_id = int(employee_id)

        if 'allowed_company_ids' in self.env.context:
            cids = self.env.context['allowed_company_ids']
        else:
            cids = [self.env.company.id]

        Employee = self.env['hr.employee.public'].with_context(allowed_company_ids=cids)
        # check and raise
        if not Employee.check_access_rights('read', raise_exception=False):
            return None
        try:
            Employee.browse(employee_id).check_access_rule('read')
        except AccessError:
            return None
        else:
            return Employee.browse(employee_id)


    def get_employee_organisation(self,employee_id):
        employee = self._check_employee(employee_id)
        if not employee:  # to check
            return {
                'managers': [],
                'children': [],
            }

        # compute employee data for org chart
        ancestors, current = self.env['hr.employee.public'].sudo(), employee.sudo()
        while current.parent_id and len(ancestors) < self._managers_level+1 and current != current.parent_id:
            ancestors += current.parent_id
            current = current.parent_id

        values = dict(
            self=self._prepare_employee_data(employee),
            managers=[
                self._prepare_employee_data(ancestor)
                for idx, ancestor in enumerate(ancestors)
                if idx < self._managers_level
            ],
            managers_more=len(ancestors) > self._managers_level,
            children=[self._prepare_employee_data(child) for child in employee.child_ids if child != employee],
        )
        values['managers'].reverse()
        return values

    def create_1on1s_record(self):
        if self.sudo().sh_employee_id:
            talking_point_vals = {
                'name' : 'test',
                'sh_employee_id' : self.sudo().sh_employee_id.id,
                'sh_create_date' : datetime.now(),
            }
            # if self.sudo().sh_employee_id.sudo().user_id:
            talking_point_vals.update({
                # 'sh_user_id':self.sh_employee_id.sudo().user_id.id,
                'sh_user_id':self.env.user.id,
            })
        
            agenda_vals = []
                
            default_agenda=self.env['sh.manage.agenda'].sudo().search([('sh_is_active','=',True)])
            if default_agenda:
                for agenda in default_agenda:
                    vals={
                            'sh_agenda_id':agenda.id,
                            'sh_checked':False,
                    }
                    agenda_vals.append((0,0,vals))
            # if self.sh_agenda_ids:
            #     for agenda in self.sh_agenda_ids:
            #         vals={
            #                 'sh_agenda_id':agenda.id,
            #                 'sh_checked':True,
            #         }
            #         agenda_vals.append((0,0,vals))
            if agenda_vals:    
                talking_point_vals['sh_manage_agenda_line']=agenda_vals
            talking_point=self.env['sh.talking.points'].sudo().create(talking_point_vals)

            # if one_on_ones_records :
            return {
                # 'name': "",
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'views': [(False, 'form')],
                'res_model': "sh.talking.points",
                'target': 'current',
                'res_id': talking_point.id
            }

            # return {'type': 'ir.actions.client', 'tag': 'soft_reload'}
        else :
            raise ValidationError(_('Please Fill Required Fields'))
    

    def discard_1on1s_record(self) :
        return {'type': 'ir.actions.client', 'tag': 'soft_reload'}
    


    # @api.depends('sh_store_domain','sh_employee_id')
    # def get_related_employee_data(self):
    #     for record in self:
    #         list_of_child_ids = []

    #         # === FIND THE EMPLOYEE OF CURRENT LOGIN USER ===  
    #         employee=self.env.user.employee_id

    #         if employee:

    #             # ==========================================================================
    #             # === CHECK IF WE FOUND CHILD RECORD OF EMPLOYEE OF NOT ===  
    #             # ==========================================================================
    #             if employee.subordinate_ids :
    #                 for child in employee.subordinate_ids :
    #                     list_of_child_ids.append(child.id)
    #             else : 
    #                 list_of_child_ids = list_of_child_ids

    #             # ==========================================================================
    #             # === GET THE ALL PARENT IDS FROM THIS CUSTOM METHOD ===
    #             # ==========================================================================
    #             result=self.get_employee_organisation(employee.id)


    #             # Extract ids of managers and children
    #             manager_ids = [manager['id'] for manager in result.get('managers', [])]

    #             # Combine manager ids and children ids into one list
    #             final_ids_list = manager_ids + list_of_child_ids
    #             domain= ['id', 'in', final_ids_list]
    #             record.sh_store_domain = domain
    #             # ==========================================================================

    #         else:
    #             record.sh_store_domain=False
