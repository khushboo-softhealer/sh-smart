# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models
import xlwt
from odoo.exceptions import UserError
import base64
import io


class SaleProductAttributeWizard(models.TransientModel):

    _name = "sh.sale.product.attribute.wizard"
    _description = "Sale Product Attribute Wizard"

    sh_partner_ids = fields.Many2many(
        comodel_name='res.partner', string='Partner')
    sh_from_date = fields.Date(string='From Date', required=True)
    sh_to_date = fields.Date(string='To Date', required=True)
    sh_select_product_cat = fields.Selection([('product', 'Product'), (
        'category', 'Category')], string="Selection Product - Category", default='product')
    sh_category_ids = fields.Many2many(
        comodel_name='product.category', string='Product Category')
    sh_product_ids = fields.Many2many(
        comodel_name='product.product', string='Products')
    sh_vertical_attribute_id = fields.Many2one(
        comodel_name='product.attribute', string='Vertical Attribute', required=True)
    sh_horizontal_attribute_id = fields.Many2one(
        comodel_name='product.attribute', string='Horizontal Attribute', required=True)
    sh_sale_order_stage = fields.Selection([
        ('all', 'All'),
        ('draft', 'Quotation/Quatation sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
    ], string='Sale Stage', default='all', required=True)

    def sh_print_stock_report(self):
        if self.sh_vertical_attribute_id and self.sh_horizontal_attribute_id:
            if self.sh_vertical_attribute_id == self.sh_horizontal_attribute_id:
                raise UserError(
                    'You can not take same attribute in Horizontal attribute and Vertical attribute...')
            else:
                datas = self.read()[0]
                res = self.env.ref(
                    'sh_sale_reports.sh_sale_product_report_action').report_action([], data=datas)
                return res

    def get_xls_report(self):
        if self.sh_vertical_attribute_id and self.sh_horizontal_attribute_id:
            if self.sh_vertical_attribute_id == self.sh_horizontal_attribute_id:
                raise UserError(
                    'You can not take same attribute in Horizontal attribute and Vertical attribute...')
            else:
                if self.sh_partner_ids:
                    partner_ids = self.sh_partner_ids
                else:
                    partner_ids = self.env['res.partner'].sudo().search([
                        ('id', '>', 0)])
                if self.sh_sale_order_stage == 'all':
                    domain = [('date_order', '>=', self.sh_from_date), ('date_order',
                                                                        '<=', self.sh_to_date), ('partner_id', 'in', partner_ids.ids)]
                elif self.sh_sale_order_stage == 'draft':
                    domain = [('date_order', '>=', self.sh_from_date), ('date_order', '<=', self.sh_to_date), (
                        'state', 'in', ['draft', 'sent']), ('partner_id', 'in', partner_ids.ids)]
                elif self.sh_sale_order_stage == 'sale':
                    domain = [('date_order', '>=', self.sh_from_date), ('date_order', '<=',
                                                                        self.sh_to_date), ('state', '=', 'sale'), ('partner_id', 'in', partner_ids.ids)]
                elif self.sh_sale_order_stage == 'done':
                    domain = [('date_order', '>=', self.sh_from_date), ('date_order', '<=',
                                                                        self.sh_to_date), ('state', '=', 'done'), ('partner_id', 'in', partner_ids.ids)]
                sh_sale_order = self.env['sale.order'].sudo().search(domain)
                horizontal_attr_list = []
                vertical_attr_list = []
                horizontal_attr_ids_list = self.sh_horizontal_attribute_id.value_ids.ids
                vertical_attr_ids_list = self.sh_vertical_attribute_id.value_ids.ids
                for i in range(0, len(self.sh_horizontal_attribute_id.value_ids.ids)):
                    horizontal_attr_list.append(
                        self.sh_horizontal_attribute_id.value_ids[i].name)
                for j in range(0, len(self.sh_vertical_attribute_id.value_ids.ids)):
                    vertical_attr_list.append(
                        self.sh_vertical_attribute_id.value_ids[j].name)

                partner_list = []
                category_list = []
                product_list = []
                if self.sh_select_product_cat == 'product' and self.sh_product_ids:
                    product_ids = self.sh_product_ids
                else:
                    product_ids = self.env['product.product'].sudo().search([
                        ('id', '>', 0)])
                if self.sh_select_product_cat == 'category' and self.sh_category_ids:
                    category_ids = self.sh_category_ids
                else:
                    category_ids = self.env['product.category'].sudo().search([
                        ('id', '>', 0)])
                product_attribute_dict = {}
                if self.sh_select_product_cat == 'product' and product_ids:
                    order_lines = self.env['sale.order.line'].sudo().search(
                        [('product_id', 'in', product_ids.ids), ('order_id', 'in', sh_sale_order.ids)])
                if self.sh_select_product_cat == 'category' and category_ids:
                    order_lines = self.env['sale.order.line'].sudo().search(
                        [('product_id.categ_id', 'in', category_ids.ids), ('order_id', 'in', sh_sale_order.ids)])

                for order in order_lines:

                    x_qty = 0
                    y_qty = 0
                    x = -1
                    y = -1
                    attribute_list = []
                    for x in range(0, len(vertical_attr_ids_list)):
                        attribute_list.append([])
                        for y in range(0, len(horizontal_attr_ids_list)):
                            attribute_list[x].append(0)
                    if order.order_id.partner_id.name in partner_list:
                        pass
                    else:
                        partner_list.append(order.order_id.partner_id.name)
                        product_attribute_dict[order.order_id.partner_id.name] = {
                        }

                    if order.product_id:
                        if self.sh_select_product_cat == 'category':
                            if order.product_id.categ_id.display_name in product_attribute_dict[order.order_id.partner_id.name].keys():
                                pass
                            else:
                                category_list.append(
                                    order.product_id.categ_id.display_name)
                                product_attribute_dict[order.order_id.partner_id.name][order.product_id.categ_id.display_name] = {
                                }
                        if self.sh_select_product_cat == 'category':
                            temp_list = []
                            for k, v in product_attribute_dict[order.order_id.partner_id.name][order.product_id.categ_id.display_name].items():
                                temp_list.append(k)
                            if order.product_id.name in list(product_attribute_dict[order.order_id.partner_id.name][order.product_id.categ_id.display_name].keys()):
                                pass
                            else:
                                product_attribute_dict[order.order_id.partner_id.name][
                                    order.product_id.categ_id.display_name][order.product_id.name] = attribute_list
                        else:
                            if order.product_id.name in product_attribute_dict[order.order_id.partner_id.name].keys():
                                pass
                            else:
                                product_attribute_dict[order.order_id.partner_id.name][order.product_id.name] = attribute_list
                        if order.product_id.name in product_list:
                            pass
                        else:
                            product_list.append(order.product_id.name)

                        if self.sh_select_product_cat == 'category':
                            for att in order.product_id.product_template_attribute_value_ids:
                                if att.attribute_id.id == self.sh_horizontal_attribute_id.id:
                                    x = horizontal_attr_list.index(att.name)
                                    x_qty = order.product_uom_qty
                                if att.attribute_id.id == self.sh_vertical_attribute_id.id:
                                    y = vertical_attr_list.index(att.name)
                                    y_qty = order.product_uom_qty
                                if x_qty > 0 and y_qty > 0 and x > -1 and y > -1:
                                    product_attribute_dict[order.order_id.partner_id.name][
                                        order.product_id.categ_id.display_name][order.product_id.name][y][x] += y_qty
                        else:
                            for att in order.product_id.product_template_attribute_value_ids:
                                if att.attribute_id.id == self.sh_horizontal_attribute_id.id:
                                    x = horizontal_attr_list.index(att.name)
                                    x_qty = order.product_uom_qty
                                if att.attribute_id.id == self.sh_vertical_attribute_id.id:
                                    y = vertical_attr_list.index(att.name)
                                    y_qty = order.product_uom_qty
                                if x_qty > 0 and y_qty > 0 and x > -1 and y > -1:
                                    product_attribute_dict[order.order_id.partner_id.name][order.product_id.name][y][x] += y_qty

        workbook = xlwt.Workbook()
        normal_record = xlwt.easyxf('font:height 210;align: vert center')
        heading_format = xlwt.easyxf(
            'font:height 245,bold True;pattern: pattern solid, fore_colour gray25;align: horiz center')
        worksheet = workbook.add_sheet("Sale Product Report", heading_format)

        worksheet.col(0).width = 8000
        worksheet.col(1).width = 6000
        worksheet.col(2).width = 6000
        worksheet.col(3).width = 6000
        worksheet.col(4).width = 6000

        line_var = 1
        worksheet.write_merge(line_var, line_var, 1, 1,
                              'Sale Product Report', heading_format)
        line_var += 2
        worksheet.write_merge(
            line_var, line_var, 0, 1, 'From Date : ' + str(self.sh_from_date), heading_format)
        worksheet.write_merge(
            line_var, line_var, 2, 3, 'To Date : ' + str(self.sh_to_date), heading_format)
        line_var += 2
        if product_attribute_dict:
            for partner in range(0, len(product_attribute_dict)):
                part1 = list(product_attribute_dict.keys())
                if self.sh_select_product_cat == 'product':
                    worksheet.write_merge(
                        line_var, line_var, 0, 0, 'Partner : ', heading_format)
                    worksheet.write_merge(
                        line_var, line_var, 1, 1, part1[partner], heading_format)

                if self.sh_select_product_cat == 'category':
                    for cat in range(0, len(product_attribute_dict[partner_list[partner]])):
                        worksheet.write_merge(
                            line_var, line_var, 0, 0, 'Partner : ', heading_format)
                        worksheet.write_merge(
                            line_var, line_var, 1, 1, part1[partner], heading_format)
                        worksheet.write_merge(
                            line_var, line_var, 2, 2, 'Category : ', heading_format)
                        cat1 = list(
                            product_attribute_dict[partner_list[partner]].keys())
                        worksheet.write_merge(
                            line_var, line_var, 3, 4, cat1[cat], heading_format)
                        line_var += 2

                        worksheet.write_merge(
                            line_var, line_var, 0, 0, 'Product', heading_format)
                        worksheet.write_merge(
                            line_var, line_var, 1, 1, 'Attribute', heading_format)
                        temp_line = line_var
                        for h in range(0, len(horizontal_attr_list)):
                            worksheet.write_merge(
                                temp_line, temp_line, h+2, h+2, horizontal_attr_list[h], heading_format)
                        count = 1
                        product_list = list(
                            product_attribute_dict[partner_list[partner]][cat1[cat]].keys())
                        for rec in range(0, len(product_list)):
                            worksheet.write_merge(
                                line_var+1, line_var+1, 0, 0, product_list[rec], normal_record)
                            for x in range(0, len(vertical_attr_list)):
                                worksheet.write_merge(
                                    line_var+count, line_var+count, 1, 1, vertical_attr_list[x], normal_record)
                                for y in range(0, len(horizontal_attr_list)):
                                    worksheet.write_merge(
                                        line_var+count, line_var+count, y+2, y+2, product_attribute_dict[partner_list[partner]][cat1[cat]][product_list[rec]][x][y], normal_record)
                                line_var += 1
                            line_var += 1
                        line_var += 1

                if self.sh_select_product_cat == 'product':
                    line_var += 2
                    worksheet.write_merge(
                        line_var, line_var, 0, 0, 'Product', heading_format)
                    worksheet.write_merge(
                        line_var, line_var, 1, 1, 'Attribute', heading_format)
                    temp_line = line_var
                    for h in range(0, len(horizontal_attr_list)):
                        worksheet.write_merge(
                            temp_line, temp_line, h+2, h+2, horizontal_attr_list[h], heading_format)
                    count = 1
                    product_list = list(
                        product_attribute_dict[partner_list[partner]].keys())
                    for rec in range(0, len(product_list)):
                        worksheet.write_merge(
                            line_var+1, line_var+1, 0, 0, product_list[rec], normal_record)
                        for x in range(0, len(vertical_attr_list)):
                            worksheet.write_merge(
                                line_var+count, line_var+count, 1, 1, vertical_attr_list[x], normal_record)
                            for y in range(0, len(horizontal_attr_list)):
                                worksheet.write_merge(
                                    line_var+count, line_var+count, y+2, y+2, product_attribute_dict[partner_list[partner]][product_list[rec]][x][y], normal_record)
                            line_var += 1
                        line_var += 1
                    line_var += 1

        fp = io.BytesIO()
        workbook.save(fp)
        data = base64.encodebytes(fp.getvalue())
        IrAttachment = self.env['ir.attachment']
        attachment_vals = {
            "name": "sale product.xls",
            "res_model": "ir.ui.view",
            "type": "binary",
            "datas": data,
            "public": True,
        }
        fp.close()

        attachment = IrAttachment.search([('name', '=', 'sale_product'),
                                          ('type', '=', 'binary'),
                                          ('res_model', '=', 'ir.ui.view')],
                                         limit=1)
        if attachment:
            attachment.write(attachment_vals)
        else:
            attachment = IrAttachment.create(attachment_vals)
        # TODO: make user error here
        if not attachment:
            raise UserError('There is no attachments...')

        url = "/web/content/" + str(attachment.id) + "?download=true"
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }


# https://stackoverflow.com/questions/28205805/how-do-i-create-3x3-matrices
