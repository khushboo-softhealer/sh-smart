# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models, api


class UpdatemassTag(models.TransientModel):

    _name = "sh.product.variant.update.wizard"
    _description = "Mass Update Wizard"

    banner_bool = fields.Boolean(string="Banner", default=True)
    technical_name_bool = fields.Boolean(string="Technical Name", default=True)
    edition_bool = fields.Boolean(string="Edition", default=True)
    depends_bool = fields.Boolean(string="Depends", default=True)
    required_apps_bool = fields.Boolean(string="Required Apps", default=True)
    license_bool = fields.Boolean(string="License", default=True)
    product_version_bool = fields.Boolean(string="Product Version",
                                          default=True)
    supported_browser_bool = fields.Boolean(string="Supported Browser",
                                            default=True)
    relesed_bool = fields.Boolean(string="Relesed", default=True)
    last_update_bool = fields.Boolean(string="Last Update", default=True)
    live_demo_bool = fields.Boolean(string="Live Demo", default=True)
    user_guide_bool = fields.Boolean(string="User Guide", default=True)
    video_bool = fields.Boolean(string="Video", default=True)
    blogs_bool = fields.Boolean(string="Blogs", default=True)
    tags_bool = fields.Boolean(string="Tags", default=True)
    qty_show_bool = fields.Boolean(string="Qty Show", default=True)
    product_template_ids = fields.Many2many('product.template')
    website_description_bool = fields.Boolean('Description for the website', default=True)
    sh_features_bool = fields.Boolean('Features', default=True)
    euro_price_bool = fields.Boolean("Euro Price", default=True)
    extra_image_bool = fields.Boolean("Extra Image", default=True)

    def update_variant_record(self):
        version_variant_ids = self.env['product.product'].search([
            ('name', '=', self.product_template_ids.name)
        ])

        new_variant_ids = self.product_template_ids.product_variant_ids
        variant_ids = self.product_template_ids.product_variant_ids
        new_version_name = self.product_template_ids.product_version_duplicate
        version_name = self.product_template_ids.product_version_duplicate
        new_technical_name = self.product_template_ids.sh_technical_name
        technical_name = self.product_template_ids.sh_technical_name
        new_banner = self.product_template_ids.banner_duplicate
        banner = self.product_template_ids.banner_duplicate
        new_edition = self.product_template_ids.sh_edition_ids_duplicate
        edition = self.product_template_ids.sh_edition_ids_duplicate
        new_depends = self.product_template_ids.depends_duplicate
        depends = self.product_template_ids.depends_duplicate
        new_license = self.product_template_ids.license_duplicate
        license = self.product_template_ids.license_duplicate
        new_product_version = self.product_template_ids.product_version_duplicate
        product_version = self.product_template_ids.product_version_duplicate
        new_supported_browser = self.product_template_ids.supported_browsers_duplicate
        supported_browser = self.product_template_ids.supported_browsers_duplicate
        new_relesed = self.product_template_ids.released_date_duplicate
        relesed = self.product_template_ids.released_date_duplicate
        new_last_update = self.product_template_ids.last_updated_date_duplicate
        last_update = self.product_template_ids.last_updated_date_duplicate
        new_live_demo = self.product_template_ids.live_demo_duplicate
        live_demo = self.product_template_ids.live_demo_duplicate
        new_user_guide = self.product_template_ids.user_guide_duplicate
        user_guide = self.product_template_ids.user_guide_duplicate
        new_video = self.product_template_ids.related_video_duplicate
        video = self.product_template_ids.related_video_duplicate
        new_blogs = self.product_template_ids.sh_blog_post_ids_duplicate
        blogs = self.product_template_ids.sh_blog_post_ids_duplicate
        new_tags = self.product_template_ids.tag_ids_duplicate
        tags = self.product_template_ids.tag_ids_duplicate
        new_qty_show = self.product_template_ids.qty_show_duplicate
        qty_show = self.product_template_ids.qty_show_duplicate
        website_description = self.product_template_ids.website_description_duplicate
        sh_features = self.product_template_ids.sh_features_duplicate
        euro_price = self.product_template_ids.euro_price_duplicate
        required_apps = self.product_template_ids.required_apps_duplicate

        ###############################################################################

        for j in version_variant_ids:
            if self.product_version_bool == True:
                j.product_version = product_version
            if self.last_update_bool == True:
                j.last_updated_date = last_update
            if self.technical_name_bool == True:
                j.sh_technical_name = technical_name

        for i in variant_ids:
            if self.website_description_bool == True:
                i.website_description = website_description
                
            if self.sh_features_bool == True:
                i.sh_features = sh_features
                
            if self.euro_price_bool == True:
                i.euro_price = euro_price
                
            if self.required_apps_bool == True:
                i.required_apps = required_apps
                
                
            if self.banner_bool == True:
                i.banner = banner
            if self.edition_bool == True:
                i.sh_edition_ids = edition
            if self.depends_bool == True:
                i.depends = depends
            if self.license_bool == True:
                i.license = license
            if self.supported_browser_bool == True:
                i.supported_browsers = supported_browser
            if self.relesed_bool == True:
                i.released_date = relesed
            if self.live_demo_bool == True:
                i.live_demo = live_demo
            if self.user_guide_bool == True:
                i.user_guide = user_guide
            if self.video_bool == True:
                i.related_video = video
            if self.blogs_bool == True:
                i.sh_blog_post_ids = blogs
            if self.tags_bool == True:
                i.tag_ids = tags
            if self.qty_show_bool == True:
                i.qty_show = qty_show

            if self.extra_image_bool == True:
                variant_image_ids = []
                for image in self.product_template_ids.product_template_image_ids:
                    variant_image  = self.env['product.image'].sudo().create(
                                                    {'product_variant_id':i.id,
                                                        'name':image.name,
                                                        'image':image.image
                                                     })
                    variant_image_ids.append(variant_image.id)
                i.product_variant_image_ids = [(6,0,variant_image_ids)]

###################################################################################


            if self.technical_name_bool == True:
                self.product_template_ids.sh_technical_name = i.sh_technical_name
            else:
                self.product_template_ids.sh_technical_name = new_technical_name
            if self.edition_bool == True:
                self.product_template_ids.sh_edition_ids = i.sh_edition_ids
            else:
                self.product_template_ids.sh_edition_ids = new_edition
            if self.banner_bool == True:
                self.product_template_ids.banner = i.banner
            else:
                self.product_template_ids.banner = new_banner
            if self.depends_bool == True:
                self.product_template_ids.depends = i.depends
            else:
                self.product_template_ids.depends = new_depends
            if self.license_bool == True:
                self.product_template_ids.license = i.license
            else:
                self.product_template_ids.license = new_license
            if self.supported_browser_bool == True:
                self.product_template_ids.supported_browsers = i.supported_browsers
            else:
                self.product_template_ids.supported_browsers = new_supported_browser
            if self.relesed_bool == True:
                self.product_template_ids.released_date = i.released_date
            else:
                self.product_template_ids.released_date = new_relesed
            if self.live_demo_bool == True:
                self.product_template_ids.live_demo = i.live_demo
            else:
                self.product_template_ids.live_demo = new_live_demo
            if self.user_guide_bool == True:
                self.product_template_ids.user_guide = i.user_guide
            else:
                self.product_template_ids.user_guide = new_user_guide
            if self.video_bool == True:
                self.product_template_ids.related_video = i.related_video
            else:
                self.product_template_ids.related_video = new_video
            if self.blogs_bool == True:
                self.product_template_ids.sh_blog_post_ids = i.sh_blog_post_ids
            else:
                self.product_template_ids.sh_blog_post_ids = new_blogs
            if self.tags_bool == True:
                self.product_template_ids.tag_ids = i.tag_ids
            else:
                self.product_template_ids.tag_ids = new_tags
            if self.qty_show_bool == True:
                self.product_template_ids.qty_show = i.qty_show
            else:
                self.product_template_ids.qty_show = new_qty_show
            if self.last_update_bool == True:
                self.product_template_ids.last_updated_date = i.last_updated_date
            else:
                self.product_template_ids.last_updated_date = new_last_update
            if self.product_version_bool == True:
                self.product_template_ids.product_version = product_version
            else:
                self.product_template_ids.product_version = new_product_version
