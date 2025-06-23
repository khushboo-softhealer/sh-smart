# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.


from odoo import models, fields, api, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def action_create_sale_quotation_template(self):
        for record in self:
            template_line_list = []
            for line in record.order_line:
                template_line_list.append((0, 0,{
                    'product_id':line.product_id.id,
                    'name':line.name,
                    'product_uom_qty':line.product_uom_qty,
                    'product_uom_id':line.product_uom.id,
                    'display_type' : line.display_type,
                }))
            quotation_template = self.env['sale.order.template']
            quotation_template.create({
                'name': record.name,
                'require_signature':record.require_signature,
                'require_payment':record.require_payment,
                'sale_order_template_line_ids' : template_line_list,
            })
            
            order_template = self.env['sale.order.template'].search([('name','=',record.name)])
            for template in order_template:
                record.update({
                    'sale_order_template_id':template.id
                })


    @api.onchange('sale_order_template_id')
    def _onchange_sh_sale_order_template_id(self):
        if self.sale_order_template_id:
            template = self.sale_order_template_id
            self.project_manager = template.project_manager
            self.responsible_user_id = template.responsible_user_id
            self.sh_project_stage_tmpl_id = template.sh_project_stage_tmpl_id
            self.sh_pricing_mode = template.sh_pricing_mode
            self.sh_fp_based_on = template.sh_fp_based_on
            self.sh_tm_based_on = template.sh_tm_based_on
            self.sh_total_work_duration = template.sh_total_work_duration