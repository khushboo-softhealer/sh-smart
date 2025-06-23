# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields


class EmployeeWizard(models.TransientModel):
    _name = 'employee.wizard'
    _description = 'Employee Wizard'

    employees_ids = fields.Many2many('hr.employee',
                                     string="Employees",
                                     required=True)

    def generate_report(self):
        emp_datas = {}
        if self.employees_ids:
            for emp in self.employees_ids:
                if emp.asset_ids:
                    list_assets_dic = []
                    if emp.asset_ids:
                        for sh_asset in emp.asset_ids:
                            asset_dic = {
                                'sh_ebs_barcode': sh_asset.sh_ebs_barcode,
                                'category_name':
                                sh_asset.asset_category_id.name
                            }
                            list_assets_dic.append(asset_dic)
                    emp_datas[emp.name] = list_assets_dic
        datas = {}
        datas['dic_assets'] = emp_datas
        return self.env.ref(
            'sh_assets_manager.action_report_barcode_employee_assets'
        ).report_action([], data=datas)
