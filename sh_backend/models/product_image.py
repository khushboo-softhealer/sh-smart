# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields,api
from odoo.tools.translate import html_translate
from odoo.exceptions import ValidationError
from datetime import timedelta, datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class ProductImage(models.Model):
    _inherit = 'product.image'

    product_variant_id = fields.Many2one("product.product",string="product")


    @api.model
    def default_get(self,default_fields):
        
        """ Compute default partner_bank_id field for 'out_invoice' type,
        using the default values computed for the other fields.
        """

        res = super(ProductImage, self).default_get(default_fields)

        if self._context.get('active_model')=='product.template' and self._context.get('active_id'):
            get_template_id=self.env['product.template'].search([('id','=',self._context.get('active_id'))])
            res.update({'name':get_template_id.name})
       
        if self._context.get('active_model')=='product.product' and self._context.get('active_id'):
            get_product_id=self.env['product.product'].search([('id','=',self._context.get('active_id'))])
            res.update({'name':get_product_id.name})
        
        if self._context.get('active_model')=='product.template' and self._context.get('active_id'):
            get_template_id=self.env['product.template'].search([('id','=',self._context.get('active_id'))])
            res.update({'product_tmpl_id':get_template_id.id})
        
        if self._context.get('active_model')=='product.product' and self._context.get('active_id'):
            get_product_id=self.env['product.product'].search([('id','=',self._context.get('active_id'))])
            res.update({'product_variant_id':get_product_id.id})
        
        return res
