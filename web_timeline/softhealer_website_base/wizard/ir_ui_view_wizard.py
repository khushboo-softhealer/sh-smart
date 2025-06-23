# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields, api
from odoo.tools.translate import xml_translate

class IrUiViewWizard(models.TransientModel):
    _name = 'softhealer.website.base.ir.ui.view.wizard'
    _description = "Wizard for Ir Ui view"

    view_name = fields.Char(
        string='Name',
        readonly='1',
    )
    arch_base = fields.Text(string='Base View Architecture')
    arch_db = fields.Text(string='Arch Blob', translate=xml_translate,)


    # SEO FIELDS
    website_meta_title = fields.Char("Website meta title", translate=True)
    website_meta_description = fields.Text("Website meta description", translate=True)
    website_meta_keywords = fields.Char("Website meta keywords", translate=True)
    website_meta_og_img = fields.Char("Website opengraph image")


    @api.model
    def default_get(self, fields_list):
        values = super(IrUiViewWizard, self).default_get(fields_list)
        page_obj = self.env['website.page'].sudo()
        context = self.env.context or {}
        page_id = context.get("active_ids", False)[0]
        if context and page_id:
            page = page_obj.browse(page_id)
            if page:
                values["view_name"] = page.name
                values["arch_base"] = page.arch_base

                # SEO FIELDS
                values["website_meta_title"] = page.website_meta_title
                values["website_meta_description"] = page.website_meta_description
                values["website_meta_keywords"] = page.website_meta_keywords
                values["website_meta_og_img"] = page.website_meta_og_img                                                                
        
        return values

    def update_sh_ir_ui_view_code(self):
        page_obj = self.env['website.page'].sudo()
        context = self.env.context or {}
        page_id = context.get("active_ids", False)[0]
        if context and page_id:
            page = page_obj.browse(page_id)
            page.write({
               "arch_base": self.arch_base,
               "website_meta_title": self.website_meta_title,
               "website_meta_description": self.website_meta_description,
               "website_meta_keywords": self.website_meta_keywords,
               "website_meta_og_img": self.website_meta_og_img,
            })
        