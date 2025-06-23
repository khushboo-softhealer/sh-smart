# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields, api
from odoo.osv import expression
import re
from datetime import timedelta, datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

class ProductProduct(models.Model):
    _inherit = "product.product"

    # @api.model

    # def name_get(self):
    #     # TDE: this could be cleaned a bit I think
    #     def _name_get(d):
    #         name = d.get('name', '')
    #         code = self._context.get('display_sh_technical_name', True) and d.get('sh_technical_name', False) or False
    #         if code:
    #             name = '[%s] %s' % (code, name)
    #         return (d['id'], name)

    #     partner_id = self._context.get('partner_id')
    #     if partner_id:
    #         partner_ids = [partner_id, self.env['res.partner'].browse(partner_id).commercial_partner_id.id]
    #     else:
    #         partner_ids = []
    #     company_id = self.env.context.get('company_id')

    #     # all user don't have access to seller and partner
    #     # check access and use superuser
    #     self.check_access_rights("read")
    #     self.check_access_rule("read")

    #     result = []

    #     # Prefetch the fields used by the `name_get`, so `browse` doesn't fetch other fields
    #     # Use `load=False` to not call `name_get` for the `product_tmpl_id`

    #     # self.sudo().read([
    #     #     'name', 'sh_technical_name', 'product_tmpl_id',
    #     #     'attribute_value_ids', 'attribute_line_ids'
    #     # ],
    #     #                  load=False)

    #     self.sudo().read(['name', 'sh_technical_name', 'product_tmpl_id'], load=False)

    #     product_template_ids = self.sudo().mapped('product_tmpl_id').ids

    #     if partner_ids:
    #         supplier_info = self.env['product.supplierinfo'].sudo().search([
    #             ('product_tmpl_id', 'in', product_template_ids),
    #             ('partner_id', 'in', partner_ids),
    #         ])
    #         # Prefetch the fields used by the `name_get`, so `browse` doesn't fetch other fields
    #         # Use `load=False` to not call `name_get` for the `product_tmpl_id` and `product_id`
    #         supplier_info.sudo().read(['product_tmpl_id', 'product_id', 'product_name', 'product_code'],load=False)
    #         supplier_info_by_template = {}
    #         for r in supplier_info:
    #             supplier_info_by_template.setdefault(r.product_tmpl_id,[]).append(r)
    #     for product in self.sudo():

    #         print("\n\n\n callingg name gert ")
    #         variant = product.product_template_attribute_value_ids._get_combination_name()
    #         print("\n\n\n callingg variantt ",variant)

    #         name = variant and "%s (%s)" % (product.name,variant) or product.name
    #         sellers = self.env['product.supplierinfo'].sudo().browse(self.env.context.get('seller_id')) or []

    #         if not sellers and partner_ids:
    #             product_supplier_info = supplier_info_by_template.get(product.product_tmpl_id, [])
    #             sellers = [x for x in product_supplier_info if x.product_id and x.product_id == product]
    #             if not sellers:
    #                 sellers = [x for x in product_supplier_info if not x.product_id]
    #             # Filter out sellers based on the company. This is done afterwards for a better
    #             # code readability. At this point, only a few sellers should remain, so it should
    #             # not be a performance issue.
    #             if company_id:
    #                 sellers = [x for x in sellers if x.company_id.id in [company_id, False]]
    #         if sellers:
    #             for s in sellers:
    #                 seller_variant = s.product_name and (
    #                     variant and "%s (%s)" % (s.product_name, variant) or s.product_name
    #                     ) or False
    #                 mydict = {
    #                           'id': product.id,
    #                           'name': seller_variant or name,
    #                           'sh_technical_name': s.sh_technical_name or product.sh_technical_name,
    #                           }
    #                 temp = _name_get(mydict)
    #                 if temp not in result:
    #                     result.append(temp)
    #         else:
    #             mydict = {
    #                       'id': product.id,
    #                       'name': name,
    #                       'sh_technical_name': product.sh_technical_name,
    #                       }
    #             result.append(_name_get(mydict))
    #     return result

########################################################################################

    # @api.model
    # def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        
    #     if not args:
    #         args = []
    #     if name:
    #         positive_operators = ['=', 'ilike', '=ilike', 'like', '=like']
    #         product_ids = []
    #         if operator in positive_operators:
    #             product_ids = self._search([('sh_technical_name', '=', name)] +
    #                                        args,
    #                                        limit=limit,
    #                                        access_rights_uid=name_get_uid)
    #             if not product_ids:
    #                 product_ids = self._search([('barcode', '=', name)] + args,
    #                                            limit=limit,
    #                                            access_rights_uid=name_get_uid)
    #         if not product_ids and operator not in expression.NEGATIVE_TERM_OPERATORS:
    #             # Do not merge the 2 next lines into one single search, SQL search performance would be abysmal
    #             # on a database with thousands of matching products, due to the huge merge+unique needed for the
    #             # OR operator (and given the fact that the 'name' lookup results come from the ir.translation table
    #             # Performing a quick memory merge of ids in Python will give much better performance
    #             product_ids = self._search(
    #                 args + [('sh_technical_name', operator, name)],
    #                 limit=limit)
    #             if not limit or len(product_ids) < limit:
    #                 # we may underrun the limit because of dupes in the results, that's fine
    #                 limit2 = (limit - len(product_ids)) if limit else False
    #                 product2_ids = self._search(
    #                     args + [('name', operator, name),
    #                             ('id', 'not in', product_ids)],
    #                     limit=limit2,
    #                     access_rights_uid=name_get_uid)
    #                 product_ids.extend(product2_ids)
    #         elif not product_ids and operator in expression.NEGATIVE_TERM_OPERATORS:
    #             domain = expression.OR([
    #                 [
    #                     '&', ('sh_technical_name', operator, name),
    #                     ('name', operator, name)
    #                 ],
    #                 [
    #                     '&', ('sh_technical_name', '=', False),
    #                     ('name', operator, name)
    #                 ],
    #             ])
    #             domain = expression.AND([args, domain])
    #             product_ids = self._search(domain,
    #                                        limit=limit,
    #                                        access_rights_uid=name_get_uid)
    #         if not product_ids and operator in positive_operators:
    #             ptrn = re.compile('(\[(.*?)\])')
    #             res = ptrn.search(name)
    #             if res:
    #                 product_ids = self._search(
    #                     [('sh_technical_name', '=', res.group(2))] + args,
    #                     limit=limit,
    #                     access_rights_uid=name_get_uid)
    #         # still no results, partner in context: search on supplier info as last hope to find something
    #         if not product_ids and self._context.get('partner_id'):
    #             suppliers_ids = self.env['product.supplierinfo']._search(
    #                 [('name', '=', self._context.get('partner_id')), '|',
    #                  ('product_code', operator, name),
    #                  ('product_name', operator, name)],
    #                 access_rights_uid=name_get_uid)
    #             if suppliers_ids:
    #                 product_ids = self._search(
    #                     [('product_tmpl_id.seller_ids', 'in', suppliers_ids)],
    #                     limit=limit,
    #                     access_rights_uid=name_get_uid)
    #     else:
    #         product_ids = self._search(args,
    #                                    limit=limit,
    #                                    access_rights_uid=name_get_uid)

    #     return self.browse(product_ids).name_get()

#####################################################################
    def add_product_extra_images(self):

        return {
                'name':'Add Extra Images',
                'res_model':'sh.product.extra.image',
                'view_mode':'form',
                'view_id': self.env.ref('sh_backend.sh_product_extra_image_wizard_form').id,
                'target':'new',
                'type':'ir.actions.act_window',
                'context':{'default_product_ids':[(6,0,self.env.context.get('active_ids'))]}
            }

    @api.onchange('last_updated_date')
    def last_update_date_onchange(self):
        active_product_template_ids = self.env['product.template'].browse(self.env.context.get('active_id'))
        update_dates = []
        for i in active_product_template_ids.product_variant_ids:
            if i.last_updated_date:
                update_dates.append(str(i.last_updated_date))

        if self.last_updated_date:      
            update_dates.append(str(self.last_updated_date))
        if update_dates :
            update_dates.sort(
                key=lambda date: datetime.strptime(date, "%Y-%m-%d"))
            latest_date_index = len(update_dates)
            latest_update_date = update_dates[latest_date_index - 1]
            product_template_id = self.product_tmpl_id
            datetime_object = datetime.strptime(latest_update_date, '%Y-%m-%d')
            next_date = datetime_object + timedelta(days=self.sh_scale_ids.days)       
            vals = {"module_last_updated_date": datetime_object.date(),  'last_updated_2':next_date}
            if self.env.context.get('active_model') == 'product.template' :
                active_product_template_ids.write(vals)
            else :
                 self.product_tmpl_id.write(vals)


##############################################################################


    # ============ added =========
    # product_variant_change_log_id = fields.One2many('product.change.log','product_variant_id','Product Change Log')
    # change_log_count = fields.Integer(
    #     'Promotions Count', compute='_compute_get_change_log_count')

    # @api.multi
    @api.model
    def link_product_to_task(self):
        active_product_ids = self.env['product.product'].sudo().browse(self.env.context.get('active_ids'))
        for data in active_product_ids:
            domain = [('parent_id', '=', data.related_task.id)]
            find_sub = self.env['project.task'].sudo().search(domain,limit=1,order = "id desc")               
            find_sub.sudo().write({"sh_product_id":data.id})

   
    def open_change_log(self):
        log = self.env['product.change.log'].search(
            [('product_variant_id', '=', self.id)])
        action = self.env.ref(
            'sh_backend.sh_chage_log_action_2').read()[0]
        action['context'] = {
            'domain': [('id', 'in', log.ids)],
            'product_variant_id': self.id,
        }
        action['domain'] = [('id', 'in', log.ids)]
        return action


    @api.onchange('product_variant_change_log_id')
    def onchange_variant_log(self):
        
        listt = []
        log_dates = self.mapped('product_variant_change_log_id.date')
        
        
        for log_date in log_dates:
            if log_date != False:
                listt.append(str(log_date))
        
        log_ids = self.mapped('product_variant_change_log_id')

        if listt and log_ids.filtered(lambda x:x.log_type != 'fix'):
            latest_log_ids = log_ids.filtered(lambda x:str(x.date)==max(listt))

            length = 0
            for latest_log_id in latest_log_ids:
                if latest_log_id:
                    length = length + 1
                
            if latest_log_ids:
                self.last_updated_date = latest_log_ids[length-1].date
                self.product_version = latest_log_ids[length-1].version
