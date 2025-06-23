# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
import logging
from odoo import models, fields, api
from odoo.tools.translate import html_translate
from odoo.osv import expression
_logger = logging.getLogger(__name__)


class ProductProductInherit(models.Model):
    _inherit = 'product.product'

    _rec_names_search = ['name', 'sh_technical_name','default_code','barcode']

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        '''
            Purpose of using this method is "_rec_names_search = product_tmpl_id.sh_technical_name" not working while development so
        '''
        try:
            args = args or []
            domain = []
            if name:
                domain = [
                    '|', '|','|',('name', 'ilike', name), ('product_tmpl_id.sh_technical_name', 'ilike', name),('barcode','like',name),('default_code','like',name)
                ]
                if operator in expression.NEGATIVE_TERM_OPERATORS:
                    domain = ['&', '!'] + domain[1:]

            records = self.search(domain + args, limit=limit)
            return records.name_get()
        except Exception as e:
            _logger.error("There is an Error in custom_name_search: %s", e)
            return super(ProductProductInherit,self).name_search(name=name,args=args,operator=operator,limit=limit)




    product_variant_image_ids = fields.One2many(
        'product.image', 'product_variant_id', string='Images')

    banner = fields.Binary('Banner')
    tag_ids = fields.Many2many(
        'product.tags', 'rel_tag_ids_product', string='Tags')
    depends = fields.Many2many(
        'sh.depends', 'rel_depends_product', string='Depends')
    required_apps = fields.Many2many(
        'sh.required.apps', 'rel_apps_product', string="Required Apps")
    sh_demo_db_template_name = fields.Char('Demo DB Template Name')
    license = fields.Many2one('sh.license', string='License')
    product_version = fields.Char('Product Version')
    supported_browsers = fields.Many2many(
        'product.browsers', 'rel_supported_browsers_product', string='Supported Browsers')
    released_date = fields.Date('Released')
    last_updated_date = fields.Date('Last Updated')
    live_demo = fields.Char('Live Demo')
    user_guide = fields.Char('User Guide')
    related_video = fields.Many2many(
        'blog.post.video', 'rel_related_video_product', string='video')
    qty_show = fields.Boolean('QTY Show')
    sh_features = fields.Html(
        'Features', sanitize_attributes=False, translate=html_translate)
    sh_blog_post_ids = fields.Many2many('blog.post', string='Blogs')
    euro_price = fields.Float("Euro Price")
    usd_price = fields.Float("USD Price", compute="convert_usd_price")
    sh_edition_ids = fields.Many2many(
        'sh.edition', 'rel_edition_product', string="Edition")
    sh_scale_ids = fields.Many2one('sh.scale', string="Product Scale")
    website_description = fields.Html(
        'Description for the website', sanitize_attributes=False, translate=html_translate)
    sh_sub_task_created = fields.Boolean(string="Sub Task created", copy=False)
    related_sub_task = fields.Many2one(
        'project.task', string="Relatd Sub Task", copy=False)
    sh_blog_post_id = fields.Many2one("blog.post", string="Blog")

    product_variant_change_log_id = fields.One2many(
        'product.change.log', 'product_variant_id', 'Product Change Log ')
    change_log_count = fields.Integer(
        'Promotions Count', compute='_compute_get_change_log_count')

    @api.depends('euro_price')
    def convert_usd_price(self):
        for rec in self:
            rec.usd_price = 0.0
            if rec.euro_price > 0.0 and self.env.user.company_id.current_usd_rate > 0.0:
                rec.usd_price = rec.euro_price * self.env.user.company_id.current_usd_rate

    def _compute_get_change_log_count(self):
        if self:
            for rec in self:
                rec.change_log_count = 0
                pr = self.env['product.change.log'].search(
                    [('product_variant_id', '=', rec.id)])
                rec.change_log_count = len(pr.ids)

    def get_product_image_ids(self):

        return {
            "type": "ir.actions.act_window",
            "name": "Images",
            "view_mode": "kanban,tree,form",
            "res_model": "product.image",
            "domain": [("product_variant_id", "=", self.id)],
        }

    def get_dependent_product_in_variants(self, technical_name, product_list, product):
        if technical_name:
            product=self.env['product.product'].search([
                ('sh_technical_name','=',technical_name),
                ('product_template_attribute_value_ids.product_attribute_value_id.id','=', product.product_template_attribute_value_ids.product_attribute_value_id.id)
                ], limit=1)
            if product and product not in product_list:
                product_list.append(product)
                if product.depends:
                    for dependency in product.depends:
                        product_list = self.get_dependent_product_in_variants(
                            dependency.technical_name, product_list, product)

        return product_list
