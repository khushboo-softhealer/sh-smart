# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, SUPERUSER_ID,models, Command
from odoo.exceptions import UserError

class HelpdeskTicketSO(models.Model):
    _inherit = 'sh.helpdesk.ticket'

    sale_order_count = fields.Integer(
        'Order', compute='_compute_sale_order_count_helpdesk')
    estimation_hours = fields.Float('Estimation Hours')
    estimation_description = fields.Text('Description')
    sh_invoice_verified = fields.Selection([('yes','Yes'),('no','No')],string='Invoice Verified')
    sh_custom_module_conflict = fields.Selection([('yes','Yes'),('no','No')],string='Custom App/Theme Installed Verified')
    sh_need_to_setup_environment = fields.Selection([('yes','Yes'),('no','No')],string='Need to setup Environment')
    sh_latest_update = fields.Selection([('yes','Yes'),('no','No')],string='Feature Update Verified')
    sh_original_module_send = fields.Boolean('Original Module need to send ?')
    sh_estimation_product_id = fields.Many2one('product.product',string='Estimation Product', default=lambda self: self.env.user.company_id.sh_estimation_product_id)
    sh_estimation_respon_user_ids = fields.Many2many('res.users','res_users_ticket_rel',string='Responsible Users')
    sh_deployment_required = fields.Selection([('yes','Yes'),('no','No')],string='Deployment Verified')

    #Removed due to not use on 19th december 2024
    # def action_create_so(self):
    #     current_user=self.env.user
    #     self = self.with_user(SUPERUSER_ID)
    #     order_vals = {}
    #     if self.sh_default_sale_quotation_template and self.sh_default_sale_quotation_template.note:
    #         order_vals.update({'note':self.sh_default_sale_quotation_template.note})
    #     if self.sh_invoice_verified:
    #         order_vals.update({
    #             'sh_invoice_verified':self.sh_invoice_verified,
    #         })
    #     if self.sh_deployment_required:
    #         order_vals.update({
    #             'sh_deployment_required':self.sh_deployment_required,
    #         })
    #     if self.sh_custom_module_conflict:
    #         order_vals.update({
    #             'sh_custom_module_conflict':self.sh_custom_module_conflict,
    #         })
    #     if self.sh_need_to_setup_environment:
    #         order_vals.update({
    #             'sh_need_to_setup_environment':self.sh_need_to_setup_environment,
    #         })
    #     if self.sh_latest_update:
    #         order_vals.update({
    #             'sh_latest_update':self.sh_latest_update,
    #         })
    #     if self.sh_edition_id:
    #         order_vals.update({
    #             'sh_edition_id':self.sh_edition_id.id,
    #         })
    #     if self.sh_odoo_hosted_id:
    #         order_vals.update({
    #             'sh_odoo_hosted_id':self.sh_odoo_hosted_id.id,
    #         })
    #     if self.task_ids:
    #         order_vals.update({
    #             'sh_task_id':self.task_ids[0].id or False,
    #         })
    #     if self.partner_id:
    #         order_vals.update({
    #             'partner_id': self.partner_id.id,
    #         })
    #     if self.env.user.company_id.sh_estimation_pricelist_id:
    #         self.partner_id.property_product_pricelist = self.env.user.company_id.sh_estimation_pricelist_id.id
    #         order_vals.update({
    #             'pricelist_id':self.env.user.company_id.sh_estimation_pricelist_id.id,
    #         })
    #     else:
    #         order_vals.update({
    #             'pricelist_id':self.partner_id.property_product_pricelist and self.partner_id.property_product_pricelist.id or False,
    #         })
    #     if self:
    #         order_vals.update({
    #             'sh_sale_ticket_ids': [(6, 0, self.ids)],
    #         })
    #     if self.sh_estimation_respon_user_ids:
    #         order_vals.update({
    #             'sh_responsible_user_ids': [(6, 0, self.sh_estimation_respon_user_ids.ids)],
    #         })
    #     order_vals.update({
    #         'responsible_user_id': current_user.id,
    #     })
    #     if self.sh_version_id:
    #         order_vals.update({
    #             'odoo_version': self.sh_version_id.id,
    #         })

    #     order_vals.update({'user_id':current_user.id})    
        
    #     order_id = self.env['sale.order'].create(order_vals)
    #     if order_id:
    #         order_id.user_id = self.env.context.get('uid')
    #         return{
    #             'name': 'Sale Order',
    #             'type': 'ir.actions.act_window',
    #             'res_model': 'sale.order',
    #             'view_mode': 'form',
    #             'res_id': order_id.id,
    #             'target': 'current'
    #         }

    def action_sale_create_order(self):
        current_user=self.env.user
        self = self.with_user(SUPERUSER_ID)
        #removed the code due to not usable on 19th december 2024

        # required_fields = [
        #     (not self.sh_edition_id, 'Edition is required.'),
        #     (not self.sh_odoo_hosted_id, 'Hosted On is required.'),
        #     (not self.sh_version_id, 'Version is required.'),
        #     (not self.sh_invoice_verified, 'Please make sure Invoice Verified or not.'),
        #     (not self.sh_custom_module_conflict, 'Please make sure Custom Module Installed Verified or not.'),
        #     (not self.sh_need_to_setup_environment, 'Please make sure Need to setup Environment or not.'),
        #     (not self.sh_latest_update, 'Please make sure Feature Update Verified or not.'),
        #     (not self.sh_deployment_required, 'Please make sure deployment from our side or not.')
        # ]

        # warning_message = '\n'.join([message for condition, message in required_fields if condition])

        # if warning_message:
        #     raise UserError(warning_message)
        # else:
        order_vals = {
            'estimated_hrs' : self.estimation_hours,
        }
        # Add Quotation Template notes in Sale Order Notes
        if self.sh_default_sale_quotation_template and self.sh_default_sale_quotation_template.note:
            order_vals.update({'note':self.sh_default_sale_quotation_template.note})

        if self.custom_website_form_campaign_id:
            order_vals.update({'campaign_id' : self.custom_website_form_campaign_id.id})
        if self.custom_website_form_medium_id:
            order_vals.update({'medium_id' : self.custom_website_form_medium_id.id})
        if self.custom_website_form_source_id:
            order_vals.update({'source_id' : self.custom_website_form_source_id.id})
        if self.custom_website_form_url:
            order_vals.update({'ticket_url' : self.custom_website_form_url})


        if self.sh_invoice_verified:
            order_vals.update({
                'sh_invoice_verified':self.sh_invoice_verified,
            })
        if self.sh_deployment_required:
            order_vals.update({
                'sh_deployment_required':self.sh_deployment_required,
            })
        if self.sh_custom_module_conflict:
            order_vals.update({
                'sh_custom_module_conflict':self.sh_custom_module_conflict,
            })
        if self.sh_need_to_setup_environment:
            order_vals.update({
                'sh_need_to_setup_environment':self.sh_need_to_setup_environment,
            })
        if self.sh_latest_update:
            order_vals.update({
                'sh_latest_update':self.sh_latest_update,
            })
        if self.sh_edition_id:
            order_vals.update({
                'sh_edition_id':self.sh_edition_id.id,
            })
        if self.sh_odoo_hosted_id:
            order_vals.update({
                'sh_odoo_hosted_id':self.sh_odoo_hosted_id.id,
            })
        if self.task_ids:
            order_vals.update({
                'sh_task_id':self.task_ids[0].id or False,
            })
        if self.partner_id:
            order_vals.update({
                'partner_id': self.partner_id.id,
            })
        if self.env.user.company_id.sh_estimation_pricelist_id:
            self.partner_id.property_product_pricelist = self.env.user.company_id.sh_estimation_pricelist_id.id
            order_vals.update({
                'pricelist_id':self.env.user.company_id.sh_estimation_pricelist_id.id,
            })
        else:
            order_vals.update({
                'pricelist_id':self.partner_id.property_product_pricelist and self.partner_id.property_product_pricelist.id or False,
            })
        if self:
            order_vals.update({
                'sh_sale_ticket_ids': [(6, 0, self.ids)],
            })
        # if self.sh_estimation_respon_user_ids:
        #     order_vals.update({
        #         'sh_responsible_user_ids': [(6, 0, self.sh_estimation_respon_user_ids.ids)],
        #     })
        order_vals.update({
            'responsible_user_id': current_user.id,
        })
        if self.sh_version_id:
            order_vals.update({
                'odoo_version': self.sh_version_id.id,
            })

        order_vals.update({'user_id':current_user.id})    
        
        order_id = self.env['sale.order'].create(order_vals)
        
        if order_id:
            line_list = []
            if self.sh_original_module_send:
                if not self.product_ids:
                    raise UserError('Product is required.')
                if self.product_ids:
                    for product in self.product_ids:
                        price = self.company_id.sh_estimation_pricelist_id._compute_price_rule(
                                    # [(product, 1.0, partner)], date=fields.Date.today(), uom_id=product.uom_id.id)[product.id][0]
                                    product,qty=1.0, date=fields.Date.today(), uom_id=product.uom_id.id)[product.id][0]
                        # price = self.env.user.company_id.sh_estimation_pricelist_id._compute_price_rule(product,quantity = 1.0,uom_id=product.uom_id.id, date=fields.Date.today())[product.id][0]
                        line_vals = {
                            'product_id': product.id,
                            'name': product.name_get()[0][1],
                            'product_uom_qty': 1.0,
                            'price_unit': price,
                            'product_uom': product.uom_id.id,
                        }
                        if product.taxes_id:
                            line_vals.update({
                                'tax_id': [(6, 0, product.taxes_id.ids)]
                            })
                        line_list.append(Command.create(line_vals))
                        if product.depends:
                            for depend in product.depends:
                                if depend.technical_name and self.sh_version_id:
                                    depend_product_id = self.env['product.product'].sudo().search([
                                        ('product_template_variant_value_ids.attribute_id.name','=','Version'),
                                        ('product_template_variant_value_ids.product_attribute_value_id.name','=',self.sh_version_id.name),
                                        ('sh_technical_name','=',depend.technical_name)
                                    ])
                                    if depend_product_id:
                                        price = self.company_id.sh_estimation_pricelist_id._compute_price_rule(
                                            # [(product, 1.0, partner)], date=fields.Date.today(), uom_id=product.uom_id.id)[product.id][0]
                                            depend_product_id,qty=1.0, date=fields.Date.today(), uom_id=depend_product_id.uom_id.id)[depend_product_id.id][0]
                                        # price = self.env.user.company_id.sh_estimation_pricelist_id._compute_price_rule(product,quantity = 1.0,uom_id=product.uom_id.id, date=fields.Date.today())[product.id][0]
                                        line_vals = {
                                            'product_id': depend_product_id.id,
                                            'name': depend_product_id.name_get()[0][1],
                                            'product_uom_qty': 1.0,
                                            'price_unit': price,
                                            'product_uom': depend_product_id.uom_id.id,
                                        }
                                        if depend_product_id.taxes_id:
                                            line_vals.update({
                                                'tax_id': [(6, 0, depend_product_id.taxes_id.ids)]
                                            })
                                        line_list.append(Command.create(line_vals))
                if self.sh_estimation_product_id:
                    price = self.env.user.company_id.sh_estimation_pricelist_id._compute_price_rule(
                                    # [(product, 1.0, partner)], date=fields.Date.today(), uom_id=product.uom_id.id)[product.id][0]
                                    self.sh_estimation_product_id,qty=1.0, date=fields.Date.today(), uom_id=self.sh_estimation_product_id.uom_id.id)[self.sh_estimation_product_id.id][0]
                    # price = self.env.user.company_id.sh_estimation_pricelist_id._compute_price_rule(self.sh_estimation_product_id,quantity= 1.0,date=fields.Date.today())[self.sh_estimation_product_id.id][0]
                    line_vals = {
                        'product_id': self.sh_estimation_product_id.id,
                        'product_uom_qty': 1.0,
                        'price_unit': price,
                        'product_uom': self.sh_estimation_product_id.uom_id.id,
                    }
                    if self.estimation_description:
                        line_vals.update({
                            'name':self.estimation_description
                        })
                    else:
                        line_vals.update({
                            'name':self.sh_estimation_product_id.name_get()[0][1]
                        })
                    if self.sh_estimation_product_id.taxes_id:
                        line_vals.update({
                            'tax_id': [(6, 0, self.sh_estimation_product_id.taxes_id.ids)]
                        })
                    line_list.append(Command.create(line_vals))
                else:
                    if self.env.user.company_id.sh_estimation_product_id:
                        price = self.env.user.company_id.sh_estimation_pricelist_id._compute_price_rule(
                                    # [(product, 1.0, partner)], date=fields.Date.today(), uom_id=product.uom_id.id)[product.id][0]
                                    self.sh_estimation_product_id,qty=1.0, date=fields.Date.today(), uom_id=self.sh_estimation_product_id.uom_id.id)[self.sh_estimation_product_id.id][0]
                        line_list = []
                        line_vals = {
                            'product_id': self.env.user.company_id.sh_estimation_product_id.id,
                            'product_uom_qty': 1.0,
                            'price_unit': price,
                            'product_uom': self.env.user.company_id.sh_estimation_product_id.uom_id.id,
                        }
                        if self.estimation_description:
                            line_vals.update({
                                'name':self.estimation_description
                            })
                        else:
                            line_vals.update({
                                'name':self.env.user.company_id.sh_estimation_product_id.name_get()[0][1]
                            })
                        if self.env.user.company_id.sh_estimation_product_id.taxes_id:
                            line_vals.update({
                                'tax_id': [(6, 0, self.env.user.company_id.sh_estimation_product_id.taxes_id.ids)]
                            })
                        line_list.append(Command.create(line_vals))
            else:
                if self.sh_estimation_product_id:
                    price = self.env.user.company_id.sh_estimation_pricelist_id._compute_price_rule(
                                    # [(product, 1.0, partner)], date=fields.Date.today(), uom_id=product.uom_id.id)[product.id][0]
                                    self.sh_estimation_product_id,qty=1.0, date=fields.Date.today(), uom_id=self.sh_estimation_product_id.uom_id.id)[self.sh_estimation_product_id.id][0]
                    line_vals = {
                        'product_id': self.sh_estimation_product_id.id,
                        'product_uom_qty': 1.0,
                        'price_unit': price,
                        'product_uom': self.sh_estimation_product_id.uom_id.id,
                    }
                    if self.estimation_description:
                        line_vals.update({
                            'name':self.estimation_description
                        })
                    else:
                        line_vals.update({
                            'name':self.sh_estimation_product_id.name_get()[0][1]
                        })
                    if self.sh_estimation_product_id.taxes_id:
                        line_vals.update({
                            'tax_id': [(6, 0, self.sh_estimation_product_id.taxes_id.ids)]
                        })
                    line_list.append(Command.create(line_vals))
                else:
                    if self.env.user.company_id.sh_estimation_product_id:
                        price = self.env.user.company_id.sh_estimation_pricelist_id._compute_price_rule(
                                    # [(product, 1.0, partner)], date=fields.Date.today(), uom_id=product.uom_id.id)[product.id][0]
                                    self.sh_estimation_product_id,qty=1.0, date=fields.Date.today(), uom_id=self.sh_estimation_product_id.uom_id.id)[self.sh_estimation_product_id.id][0]
                        line_list = []
                        line_vals = {
                            'product_id': self.env.user.company_id.sh_estimation_product_id.id,
                            'product_uom_qty': 1.0,
                            'price_unit': price,
                            'product_uom': self.env.user.company_id.sh_estimation_product_id.uom_id.id,
                        }
                        if self.estimation_description:
                            line_vals.update({
                                'name':self.estimation_description
                            })
                        else:
                            line_vals.update({
                                'name':self.env.user.company_id.sh_estimation_product_id.name_get()[0][1]
                            })
                        if self.env.user.company_id.sh_estimation_product_id.taxes_id:
                            line_vals.update({
                                'tax_id': [(6, 0, self.env.user.company_id.sh_estimation_product_id.taxes_id.ids)]
                            })
                        line_list.append(Command.create(line_vals))
            if line_list:
                order_id.order_line = line_list
                if self.env.user.company_id.sh_estimation_stage_id:
                    self.stage_id = self.env.user.company_id.sh_estimation_stage_id.id
                order_id.user_id = self.env.context.get('uid')
                
                return{
                    'name': 'Sale Order',
                    'type': 'ir.actions.act_window',
                    'res_model': 'sale.order',
                    'view_mode': 'form',
                    'res_id': order_id.id,
                    'target': 'current'
                }
                

    def _compute_sale_order_count_helpdesk(self):
        for record in self:
            record.sale_order_count = 0
            tickets = self.env['sale.order'].search(
                [('id', 'in', record.sh_sale_order_ids.ids)], limit=None)
            record.sale_order_count = len(tickets.ids)

    def action_view_sale_orders(self):
        self.ensure_one()
        orders = self.env['sale.order'].sudo().search(
            [('id', 'in', self.sh_sale_order_ids.ids)])
        action = self.env.ref(
            "sale.action_orders").read()[0]
        if len(orders) > 1:
            action['domain'] = [('id', 'in', orders.ids)]
        elif len(orders) == 1:
            form_view = [(self.env.ref('sale.view_order_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + \
                    [(state, view)
                     for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = orders.id
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
