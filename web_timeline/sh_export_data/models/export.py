# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models, _
from bs4 import BeautifulSoup
from itertools import groupby
from datetime import datetime
from odoo.exceptions import ValidationError
import re
from dateutil import parser

class SaleORder(models.Model):
    _inherit = 'sale.order'

    po_ref = fields.Char("PO Reference")
    export_id = fields.Many2one("sh.export.data")


class SaleORderLine(models.Model):
    _inherit = 'sale.order.line'

    country = fields.Char("Country")
    origin = fields.Char("Origin")
    version = fields.Char("Version")


class Export (models.Model):
    _name = 'sh.export.data'
    _description = 'Knowledge about exporting data'

    name = fields.Char(
        string="Name", default=lambda self: self.env['ir.sequence'].next_by_code('sh.export'))
    html = fields.Html(string="Data to Export", required=True)
    partner_id = fields.Many2one(
        'res.partner', string="Customer", required=True)
    ref_name = fields.Char(string="Refrence Number")
    so_ids = fields.Many2many('sale.order', string="SO Reference")
    error = fields.Text("Error Log")
    so_count = fields.Integer("So Count", compute='compute_so_count')
    state = fields.Selection([('new', 'New'), ('done', 'Done'), (
        'issue', 'Issue'), ('cancel', 'Cancel')], string="State", default='new')
    pricelist_id = fields.Many2one(comodel_name='product.pricelist', string="Pricelist",
                                   help="If you change the pricelist, only newly added lines will be affected.")

    def compute_so_count(self):
        for rec in self:
            domain = [('export_id', '=', rec.id)]
            find = self.env['sale.order'].search(domain)
            rec.so_count = len(find)

    def action_view_saleorder(self):
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            "res_model": "sale.order",
            'target': 'self',
            'domain': [('export_id', '=', self.id)],
            'views': [(self.env.ref('sale.view_quotation_tree_with_onboarding').id, 'tree'), (self.env.ref('sale.view_order_form').id, 'form')],
            'view_id': self.env.ref('sale.view_quotation_tree_with_onboarding').id,
        }

    def export_data_multi(self):
        for rec in self:
            rec.export_data()

    def export_data(self):
        if not self.pricelist_id:
            raise ValidationError(
                _("Please add Pricelist to Import %s", self.name))

        soup = BeautifulSoup(self.html, "html.parser")
        find_all_divs = soup.find_all('div', {'row purchases_vertical_align'})
        
        master_list_for_each_product_dict = []
       
        try:
            for each_div in find_all_divs:
                # print("\n =================================")
                all_divs_for_each_div = each_div.find_all('div')
                

                technical_name = re.search(r'\[(.*?)\]', each_div.find_all('img')[0].get('alt'))

                if technical_name:
                    technical_name = technical_name.group(1)

                param_dictonary = {
                    'name': all_divs_for_each_div[1].text.strip(),
                    'date': all_divs_for_each_div[2].text.strip(),
                    'origin': all_divs_for_each_div[3].text.strip(),
                    'country': all_divs_for_each_div[4].text.strip(),
                    'price': all_divs_for_each_div[5].text.strip(),
                    'qty': all_divs_for_each_div[6].text.strip(),
                    'technical_name': technical_name,
                }

                master_list_for_each_product_dict.append(param_dictonary)

            date_wise_master_dictonary = {}
            if master_list_for_each_product_dict:
                for key, value in groupby(master_list_for_each_product_dict, key=lambda d: d['date']):
                    
                    # key = '12/12/2012'
                    date_object = parser.parse(key)
                    # print("\n\n =----date_object-->",date_object)

                    # date_order = datetime.strptime(key, "%m/%d/%Y") 

                    # date_obj = datetime.strptime(key, '%m/%d/%Y')
                    # dt = datetime.combine(date_obj, datetime.min.time())

                    create_so_vals = {'partner_id': self.partner_id.id,
                                        'po_ref': self.ref_name, 'date_order': date_object, 'export_id': self.id, 'website_id' : 2}
                    find_so = self.env['sale.order'].search(
                        [('export_id', '=', self.id), ('date_order', '=', date_object),('state','=','draft')])

                    order_lines = []    
                    for each_value in value:
                        final_product = False

                        version = each_value['name'].partition('for version')[2].strip()
                        product_name = each_value['name'].partition('by Softhealer')[0].strip()

                        product_data = self.env['product.product'].search([('sh_technical_name', '=', each_value['technical_name'])])
                                                                                        
                        for product in product_data:
                            
                            for attribute in product.product_template_variant_value_ids:

                                attribute_name = attribute.name
                                
                                if version == '12.0 or older' and '12' in attribute_name:
                                    final_product = product
                                elif version == '12.0 and older' and '12' in attribute_name:
                                    final_product = product
                                else:
                                    for ver in range(13,101):
                                        ver1 = str(ver)+".0"
                                        ver2 = str(ver)
                                        if version == ver1 and ver2 in attribute_name:
                                            final_product = product
                                            break

                                # if version == '12.0 or older' and '12' in attribute_name:
                                #     final_product = product
                                # elif version == '12.0 and older' and '12' in attribute_name:
                                #     final_product = product
                                # elif version == '13.0' and '13' in attribute_name:
                                #     final_product = product
                                # elif version == '14.0' and '14' in attribute_name:
                                #     final_product = product
                                # elif version == '15.0' and '15' in attribute_name:
                                #     final_product = product
                                # elif version == '16.0' and '16' in attribute_name:
                                #     final_product = product
                                # elif version == '17.0' and '17' in attribute_name:
                                #     final_product = product
                                # elif version == '18.0' and '18' in attribute_name:
                                #     final_product = product

                                if not final_product:
                                    for rec in product.product_template_variant_value_ids:
                                        if '12' in rec.name:
                                            final_product = product
                                        elif '11' in rec.name:
                                            final_product = product
                                        elif '10' in rec.name:
                                            final_product = product

                                
                                if final_product and len(final_product) > 1:
                                    raise ValidationError(_("Multiple Product Found for %s with %s attribute", each_value['technical_name'], attribute_name))

                        if not final_product:                            
                            raise ValidationError(_("Unable to found %s with %s version", product_name, version))

                        
                        # Step 1: Remove any non-numeric or non-decimal separator characters
                        numeric_string = re.sub(r'[^\d.,-]', '', each_value['price'])

                        # Step 2: Replace the decimal separator (comma) with a dot
                        numeric_string = numeric_string.replace(',', '.')

                        # Step 3: Convert the numeric string to a float value
                        price = float(numeric_string)
                        
                        # Check for sale.order.line with existing product_id
                        so_line_with_product_id = self.env['sale.order.line'].sudo().search([('origin','=',each_value['origin']),('product_id','=', final_product.id)])
                        
                        if not so_line_with_product_id:
                            order_lines.append((0,0,{
                                'product_id': final_product.id,
                                'name': each_value['name'],
                                'product_uom_qty': each_value['qty'],
                                'version': version,
                                'price_unit': price,
                                'country': each_value['country'],
                                'origin': each_value['origin'],
                                'tax_id': False
                            }))
                            

                    if order_lines:
                        if find_so:
                            find_so.pricelist_id = self.pricelist_id.id
                            find_so._onchange_pricelist_id_show_update_prices()
                            find_so.write({'order_line': order_lines})

                        if not find_so:
                            sale_order_id = self.env['sale.order'].create(create_so_vals)
                            sale_order_id.pricelist_id = self.pricelist_id.id
                            sale_order_id._onchange_pricelist_id_show_update_prices()
                            sale_order_id.write({'order_line': order_lines})


                self.error = False
                
                # Display Success Notifiction
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'type': 'success',
                        'sticky': False,
                        'message': _("Exported"),
                    }
                }


        except Exception as e:
            self.error = str(e)

            # Display Error Notifiction
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'type': 'danger',
                    'sticky': True,
                    'message': _("Failed to Export"),
                }
            }
        # return False

        # for x in find_final:
        #     pp = x.find_all('div')

        #     count = 0
        #     thisdict = {}

        #     for y in pp:
        #         if count == 1:
        #             thisdict["name"] = y.text.strip()

        #         if count == 2:
        #             thisdict["date"] = y.text.strip()

        #         if count == 3:
        #             thisdict["origin"] = y.text.strip()

        #         if count == 4:
        #             thisdict["country"] = y.text.strip()

        #         if count == 5:
        #             thisdict["price"] = y.text.strip()

        #         if count == 6:
        #             thisdict["qty"] = y.text.strip()
        #         if count == 7:
        #             break
        #         count += 1

        #     if not '-' in thisdict['price']:
        #         link = x.find('a')
        #         link_list = link['href'].split('/')
        #         tech_name = link_list[len(link_list)-2]
        #         thisdict["technical_name"] = tech_name

        #     master_list_for_each_product_dict.append(thisdict)

        # master_dictoanry_date_wise = {}
        # sorted_date = sorted(
        #     master_list_for_each_product_dict, key=lambda d: d['date'])

        # for k, v in groupby(sorted_date, key=lambda d: d['date']):
        #     master_dictoanry_date_wise[k] = list(v)
        # so_ids = []
        # error_log = ''
        # count = 1

        # for key, items in master_dictoanry_date_wise.items():

        #     count = 1
        #     for item in items:
        #         if not '-' in item['price']:
        #             tech_name = item['technical_name']
        #             product_data = self.env['product.template'].search(
        #                 [('sh_technical_name', '=', tech_name)], limit=1)
        #             error_name = tech_name
        #         else:
        #             partion_word = 'by Softhealer'
        #             item_name = item['name'].partition(partion_word)[0]
        #             ppp = item_name.strip()
        #             error_name = ppp
        #             product_data = self.env['product.template'].search(
        #                 [('name', 'ilike', ppp)], limit=1)
        #         if not product_data:
        #             error_log += str(count)+')'+error_name + '\n'
        #             count += 1

        # self.error = error_log

        # for key, items in master_dictoanry_date_wise.items():
        #     date_obj = datetime.strptime(key, '%m/%d/%Y')
        #     dt = datetime.combine(date_obj, datetime.min.time())

        #     vals = {'partner_id': self.partner_id.id,
        #             'po_ref': self.ref_name, 'date_order': dt, 'export_id': self.id}

        #     error_log = ''

        #     count = 1

        #     for item in items:

        #         if not '-' in item['price']:
        #             tech_name = item['technical_name']
        #             error_name = tech_name
        #             product_data = self.env['product.template'].search(
        #                 [('sh_technical_name', '=', tech_name)], limit=1)
        #         else:
        #             partion_word = 'by Softhealer'
        #             oooo = item['name'].partition(partion_word)[0]
        #             ppp = oooo.strip()
        #             error_name = ppp
        #             product_data = self.env['product.template'].search(
        #                 [('name', 'ilike', ppp)], limit=1)
        #         if not product_data:
        #             error_log += str(count)+')'+error_name + '\n'
        #             count += 1

        #     if error_log != '':
        #         # open the new success message box
        #         view = self.env.ref('sh_message.sh_message_wizard')
        #         view_id = view and view.id or False
        #         context = dict(self._context or {})
        #         dic_msg = 'Product Not Found !\n'
        #         dic_msg += '\n Please check Error Log !'
        #         context['message'] = dic_msg
        #         return {
        #             'name': 'Error',
        #             'type': 'ir.actions.act_window',
        #             'view_type': 'form',
        #             'view_mode': 'form',
        #             'res_model': 'sh.message.wizard',
        #             'views': [(view.id, 'form')],
        #             'view_id': view.id,
        #             'target': 'new',
        #             'context': context,
        #         }

        #     # self.error = error_log

        #     # some = 0
        #     for item in items:

        #         count = 0
        #         date_order = datetime.strptime(item['date'], "%m/%d/%Y")

        #         domain = [('export_id', '=', self.id),
        #                   ('date_order', '=', date_order)]

        #         find_so = self.env['sale.order'].search(domain)

        #         # print(f"\n\n\n ==>>find_so: {find_so}")

        #         lets_create_new_lines = False

        #         if find_so:
        #             for each_so in find_so:
        #                 for each_so_line in each_so.order_line:
        #                     if each_so_line.origin == item['origin']:
        #                         count += 1
        #         else:
        #             lets_create_new_lines = True
        #             find_so = self.env['sale.order'].create(vals)

        #         # if count != 0:
        #         #     continue

        #         split_word = 'for version'
        #         version = item['name'].partition(split_word)[2]
        #         version = version.strip()
        #         final_product = False
        #         if not '-' in item['price']:
        #             tech_name = item['technical_name']
        #             product_data = self.env['product.product'].search(
        #                 [('sh_technical_name', '=', tech_name)])
        #         else:
        #             partion_word = 'by Softhealer'
        #             item_name = item['name'].partition(partion_word)[0]
        #             product_name = item_name.strip()
        #             product_data = self.env['product.product'].search(
        #                 [('name', 'ilike', product_name)])

        #         for data in product_data:

        #             for rec in data.product_template_variant_value_ids:
        #                 if version == '12.0 or older' and '12' in rec.name:
        #                     final_product = data
        #                 elif version == '12.0 and older' and '12' in rec.name:
        #                     final_product = data
        #                 elif version == '13.0' and '13' in rec.name:
        #                     final_product = data
        #                 elif version == '14.0' and '14' in rec.name:
        #                     final_product = data
        #                 elif version == '15.0' and '15' in rec.name:
        #                     final_product = data
        #                 elif version == '16.0' and '16' in rec.name:
        #                     final_product = data
        #                 elif version == '17.0' and '17' in rec.name:
        #                     final_product = data

        #             if not final_product:
        #                 for rec in data.product_template_variant_value_ids:
        #                     if '12' in rec.name:
        #                         final_product = data
        #                         # version = '12.0 or older'
        #                     elif '11' in rec.name:
        #                         final_product = data
        #                         # version = '12.0 or older'
        #                     elif '10' in rec.name:
        #                         final_product = data
        #                         # version = '12.0 or older'

        #         if not final_product:

        #             ppp = item['name']
        #             # raise UserError(_("Product '%s' related version not found ! ") %(product_data[0].name))
        #             error_log += str(count)+')'+ppp + '\n'
        #             count += 1
        #             # continue
        #         else:
        #             # some += 1

        #             if item['price'].split('\xa0€')[0].find('-') == -1:
        #                 line_vals = {
        #                     'product_id': final_product.id,
        #                     'name': item['name'],
        #                     'product_uom_qty': item['qty'],
        #                     'version': version,
        #                     'price_unit': float(item['price'].split('\xa0€')[0]),
        #                     'order_id': find_so.id,
        #                     'country': item['country'],
        #                     'origin': item['origin'],
        #                     'tax_id': False
        #                 }

        #             else:
        #                 line_vals = {
        #                     'product_id': final_product.id,
        #                     'name': item['name'],
        #                     'product_uom_qty': item['qty'],
        #                     'version': version,
        #                     'price_unit': float(item['price'].split('\xa0€')[0].split('\ufeff')[1]) * (-1),
        #                     'order_id': find_so.id,
        #                     'country': item['country'],
        #                     'origin': item['origin'],
        #                     'tax_id': False
        #                 }
        #             self.env['sale.order.line'].create(line_vals)

        #         if error_log != '':
        #             # open the new success message box
        #             view = self.env.ref('sh_message.sh_message_wizard')
        #             view_id = view and view.id or False
        #             context = dict(self._context or {})
        #             dic_msg = 'Version Not Found !\n'
        #             dic_msg += '\n Please check Error Log !'
        #             context['message'] = dic_msg
        #             self.error = error_log
        #             return {
        #                 'name': 'Error',
        #                 'type': 'ir.actions.act_window',
        #                 'view_type': 'form',
        #                 'view_mode': 'form',
        #                 'res_model': 'sh.message.wizard',
        #                 'views': [(view.id, 'form')],
        #                 'view_id': view.id,
        #                 'target': 'new',
        #                 'context': context,
        #             }
        #         if find_so:
        #             find_so.pricelist_id = self.pricelist_id.id
        #             find_so._onchange_pricelist_id_show_update_prices()

        # self.so_ids = [(6, 0, so_ids)]
