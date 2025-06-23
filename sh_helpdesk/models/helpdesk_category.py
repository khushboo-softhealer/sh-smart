# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, _,tools
from datetime import datetime


class HelpdeskCategory(models.Model):
    _name = 'sh.helpdesk.category'
    _description = 'Helpdesk Category'
    _rec_name = 'name'

    sequence = fields.Integer(string="Sequence")
    name = fields.Char(required=True, translate=True, string='Name')
    category_id = fields.Many2one(
        'product.category', string='Product Category')
    sh_product_options = fields.Html('Product options')

    @api.model_create_multi
    def create(self, values):
        for val in values:
            sequence = self.env['ir.sequence'].next_by_code('sh.helpdesk.category')
            val['sequence'] = sequence
        res = super(HelpdeskCategory, self).create(values)
        return res

    def mass_update_products(self):
        for rec in self:
            option = "<label class='control-label' for='sh_multiple_products'>Products</label><select class='form-control form-field o_website_form_required_custom' id='sh_multiple_products' name='sh_multiple_products' required='True'>"
            if rec.category_id:
                rec.sh_product_options = False
                product_ids = self.env['product.template'].sudo().search(
                    [('categ_id', '=', rec.category_id.id),('is_published','=',True)])
                if product_ids:
                    for product in product_ids:
                        option += "<option value=" + \
                            str(product.id)+">"+str(product.name_get()[0][1])
                        if product.sh_technical_name:
                            option += ' ('+str(product.sh_technical_name)+')'
                        option += "</option>"
            option += "</select><p class='alert alert-danger' id='error_products' style='display:none;'>Product is Required.</p>"
            rec.sh_product_options = option

    # def update_products(self):
    #     self.ensure_one()
    #     option = "<label class='control-label' for='sh_multiple_products'>Products</label><select class='form-control form-field o_website_form_required_custom selectized' id='sh_multiple_products' name='sh_multiple_products' required='True'><option value='product'>Select Product</option>"
    #     if self.category_id:
    #         self.sh_product_options = False
    #         product_ids = self.env['product.template'].sudo().search(
    #             [('categ_id', '=', self.category_id.id)])
    #         if product_ids:
    #             for product in product_ids:
    #                 option += "<option value=" + \
    #                     str(product.id)+">"+str(product.name_get()[0][1])
    #                 if product.sh_technical_name:
    #                     option += ' ('+str(product.sh_technical_name)+')'
    #                 option += "</option>"
        
    #     option += "</select><p class='alert alert-danger' id='error_products' style='display:none;'>Product is Required.</p>"
        
    #     self.sh_product_options = option

    def update_products(self):
        self.ensure_one()
        options = []
        options.append("<label class='control-label form-label' for='sh_multiple_products'>Products</label><select class='form-control form-field o_website_form_required_custom selectized' id='sh_multiple_products' name='sh_multiple_products' required='True'>")
        options.append("<option value='product'>Select Product</option>")
        if self.category_id:
            self.sh_product_options = False
            product_ids = self.env['product.template'].sudo().search(
                [('categ_id', '=', self.category_id.id),('is_published','=',True)])
            if product_ids:
                products = [(product.id, product.name) for product in product_ids]
                options += ["<option value='{}'>{}</option>".format(id, name) for id, name in products]
        options.append("</select><p class='alert alert-danger' id='error_products' style='display:none;'>Product is Required.</p>")
        self.sh_product_options =tools.plaintext2html("\n".join(options)) 



    @api.model
    def update_prod(self):
        for category in self.sudo().search([]):
            category.sudo().update_products()
        # Update change log
        product_template_ids = self.env['product.template'].sudo().search([])
        for product_template_id in product_template_ids:
            update_dates = []
            for i in product_template_id.product_variant_ids:
                if i.last_updated_date:
                    update_dates.append(str(i.last_updated_date))

            if update_dates:
                update_dates.sort(
                    key=lambda date: datetime.strptime(date, "%Y-%m-%d"))
                latest_date_index = len(update_dates)
                latest_update_date = update_dates[latest_date_index - 1]

                datetime_object = datetime.strptime(
                    latest_update_date, '%Y-%m-%d')
                vals = {"module_last_updated_date": datetime_object.date()}
                product_template_id.write(vals)

        # update currency
        currency_obj = self.env['res.currency'].sudo().search([], limit=1)
        currency_obj._dynamic_currency_price()

        return True
