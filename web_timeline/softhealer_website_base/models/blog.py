# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

import logging

from odoo import _, fields, models,api
from odoo.osv import expression


_logger = logging.getLogger(__name__)


class BlogBlog(models.Model):
    _inherit = "blog.blog"

    sh_is_this_career_blog = fields.Boolean(
        string='Is this career blog?',
    )
    sh_display_as_label = fields.Char("Display Label")

    softhealer_website_id = fields.Many2one('website', ondelete='set null', string="Softhealer Website")


    def search(self, args, **kwargs):
        if self.env.context.get('website_id',False) and kwargs:
            args = args or []
            domain = [('softhealer_website_id', '=', self.env.context.get('website_id')) ]
            args = expression.AND([domain, args])
        # if self.env.context.get('only_media'):
        #     args += [('name', '=', 'Media')]
        return super(BlogBlog, self).search(args, **kwargs)
    

class BlogPost(models.Model):
    _inherit = "blog.post"

    sh_image_attachment_id = fields.Many2one(
        'ir.attachment',
        string="Image Attachment",
        ondelete='set null'
    )

    sh_image_url = fields.Char(
        string="Image URL",
        store=True
    )

    # softhealer_website_id = fields.Many2one('website', ondelete='set null', string="Softhealer Website")
    softhealer_website_id = fields.Many2one(related='blog_id.softhealer_website_id',store=True)
    is_article = fields.Boolean(string="Is Article") 
    suggested_blog_by_categories = fields.Many2many('blog.post', relation="sh_suggested_blog_post_rel", column1="suggested_blog_id", column2="blog_id",string="Suggested Blogs(By Categories)")
    # random_blog_by_categories = fields.Many2many('blog.post', relation="sh_random_blog_post_rel", column1="random_blog_id", column2="blog_id",string="Random Blogs(By Categories)")
    suggestion_image = fields.Image(string="Blog Suggestion Image")

    @api.model
    def _search_get_detail(self, website, order, options):
        '''
            Purpose : We just want to search from the name field.
        '''
        result_dictonary = super(BlogPost,self)._search_get_detail(website=website,order=order,options=options)

        if result_dictonary and result_dictonary.get('search_fields'):
            result_dictonary.update({'search_fields':['name']})

        return result_dictonary

    def search(self, args, **kwargs):        
        if self.env.context.get('website_id',False) and kwargs:
            args = args or []
            domain = [('softhealer_website_id', '=', self.env.context.get('website_id')) ]
            args = expression.AND([domain, args])
        # if self.env.context.get('only_media'):
        #     args += [('name', '=', 'Media')]
        return super(BlogPost, self).search(args, **kwargs)
    


    def get_highest_digit(number):
        highest = 0
        while number > 0:
            digit = number % 10
            if digit > highest:
                highest = digit
            number //= 10
        return highest


    def update_sh_mass_meta_details(self):
        post_ids = self.env.context.get('active_ids')
        
        #### FOR PRODUCT BLOGS ####

        product_blogs = self.browse(post_ids).filtered(lambda x: not x.blog_id.sh_is_this_career_blog)
        
        for pro_blog in product_blogs:

            _logger.warning(" =============== Product individual blog %s", pro_blog)
            # print('\n\n =========== pro_blog',pro_blog)
            self.env.cr.execute("""select product_product_id from blog_post_product_product_rel 
                where blog_post_id in %s   """,[tuple(pro_blog.ids)])
            res = self.env.cr.dictfetchall()
            
            products = self.env['product.product'].sudo().browse([r['product_product_id'] for r in res])
            product_tmpl=products.mapped('product_tmpl_id')

            _logger.warning("=============== Product individual blog with products %s", products)
            _logger.warning("=============== Product individual blog with product_tmpl %s", product_tmpl)
            # print('\n\n =========== products',products)

            if product_tmpl:

                if len(products)>1:
                    _logger.warning("=============== Condition 1 =================")

                    # print(' \n\n =============== Condition 1 =================')
                    
                    value = products.product_template_attribute_value_ids.sorted(key='name', reverse=True)

                    digits = []
                    for rec in value:
                        digits.append(int(rec.name.split(' ')[1]))

                    final_products_attr = self.env['product.template.attribute.value'].search([('name', 'ilike', max(digits)),('product_tmpl_id','=',product_tmpl.id)])

                    # print(' \n\n =============== final_products_attr 1 ',final_products_attr)

                    highest_version_product = products.filtered(lambda x: final_products_attr[0].id in x.product_template_attribute_value_ids.ids)

                    #### If get multi produuct with same old blog, take higher version of product
                    _logger.warning("=============== products highest_version_product %s", highest_version_product)

                    # print(' \n\n =============== highest_version_product 1 ',highest_version_product)

                    if highest_version_product and len(highest_version_product.sh_blog_post_ids) == 1:
                        if highest_version_product.sh_blog_post_id:

                            highest_version_product.sh_blog_post_id.write({
                                'website_meta_title': highest_version_product.sh_blog_post_ids.website_meta_title,
                                'website_meta_description': highest_version_product.sh_blog_post_ids.website_meta_description,
                                'website_meta_keywords': highest_version_product.sh_blog_post_ids.website_meta_keywords,
                            })
                else:
                    _logger.warning("=============== Condition 2 =================")
                    # print(' \n\n =============== Condition 2 =================')
                    if products and len(products.sh_blog_post_ids) == 1:
                        if products.sh_blog_post_id:
                            products.sh_blog_post_id.write({
                                'website_meta_title': products.sh_blog_post_ids.website_meta_title,
                                'website_meta_description': products.sh_blog_post_ids.website_meta_description,
                                'website_meta_keywords': products.sh_blog_post_ids.website_meta_keywords,
                            })
    def action_code_blog_post_content(self):
        self.ensure_one()
        code_form = self.env.ref('softhealer_website_base.sh_website_editor_blog_post_form_wizard_code_view')
        return {
            'name': _('Blog Post Pages'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'blog.post',
            'res_id':self.id,
            'views': [(code_form.id, 'form')],
            'view_id': code_form.id,
            'target': 'new',
        }

    def open_image_cover_properties(self):
        return {
            'name': _('Generate Image URL'),
            'type': 'ir.actions.act_window',
            'res_model': 'sh.cover.property',
            'view_mode': 'form',
            'target': 'new',
            'context' : {
                'default_blog_id': self.id,
            },
        }