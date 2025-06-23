# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import fields, models

class EmpAttendanceExcelExtended(models.Model):
    _name= "excel.extended"
    _description = "Excel Extended"
 
    excel_file = fields.Binary('Download report Excel')
    file_name = fields.Char('Excel File', size=64)
     
    def emp_download_report(self):
 
        return{
            'type' : 'ir.actions.act_url',
            'url':'web/content/?model=excel.extended&field=excel_file&download=true&id=%s&filename=%s'%(self.id,self.file_name),
            'target': 'new',
        }
