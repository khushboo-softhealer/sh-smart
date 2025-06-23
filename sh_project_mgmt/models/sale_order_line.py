# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from datetime import datetime, timedelta

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProjectMgmtSaleLine(models.Model):
    _inherit = 'sale.order.line'

    sale_line_estimation_template_line = fields.One2many('sh.sale.line.estimation.template.line', 'sale_order_line_id', string='Estimation Template Lines')
    estimation_template_id=fields.Many2one('sh.estimation.template','Estimation Template Id')
    

    def btn_add_detail_estimation(self):
        self.ensure_one()    
        view = self.env.ref('sh_project_mgmt.sh_project_mgmt_sale_order_line_view')
        return {
            'name': _('Estimation Templates'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'sale.order.line',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'res_id': self.id,
            # 'context': dict(
            #     self.env.context,
            #     show_owner=self.picking_type_id.code != 'incoming',
            #     show_lots_m2o=self.has_tracking != 'none' and (self.picking_type_id.use_existing_lots or self.state == 'done' or self.origin_returned_move_id.id),  # able to create lots, whatever the value of ` use_create_lots`.
            # ),
        }
    
    def btn_show_line_project(self):
        if not self.project_id:
            return
        view = self.env.ref('project.edit_project')
        return {
            'name': _('Line Project'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'project.project',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'current',
            'res_id': self.project_id.id,
            'context': {
                'create': False,
                'delete': False
            }
        }
    
    @api.onchange('estimation_template_id')
    def onchange_estimation_template_id(self):
        for order_line in self:

            # Remove the Already existing lines from the one2many
            if order_line.sale_line_estimation_template_line:
                order_line.sale_line_estimation_template_line = False

            # Add the lines of template in one2many
            if order_line.estimation_template_id and order_line.estimation_template_id.estimation_template_line:
                for line in order_line.estimation_template_id.estimation_template_line:
                    self.env['sh.sale.line.estimation.template.line'].sudo().create({
                        'department_id':line.department_id.id,
                        'estimated_hours':line.estimated_hours,
                        'accountable_user_ids':line.accountable_user_ids,
                        'responsible_user_ids':line.responsible_user_ids,
                        'other_details':line.other_details,
                        'sale_order_line_id':order_line.id,
                        'label_id':line.label_id.id
                    })


    def write(self, vals_list):

        res=super(ProjectMgmtSaleLine, self).write(vals_list)

        for vals in vals_list:
            
            # TO ADD ESTIMATION LINE TOTAL HOURS AS A SALE ORDER QUANTITY
            # ===========================================================
            total_hours = 0
            if 'sale_line_estimation_template_line' in vals:
                for rec in self:
                    if rec.sale_line_estimation_template_line:
                        total_hours=0
                        for line in rec.sale_line_estimation_template_line:
                            total_hours+=line.estimated_hours
                        
                    if rec.product_uom_qty < total_hours:  
                        raise ValidationError("You cannot add more quantity in Estimation then defined in sale order line !")

        return res
    
    # def _compute_price_unit(self):
    #     # on change qty price get change--- need to stop
    #     olf_price_unit = self.price_unit
    #     super(ProjectMgmtSaleLine, self)._compute_price_unit()
    #     self.price_unit = olf_price_unit


