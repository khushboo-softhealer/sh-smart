# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields,api
from odoo.tools.translate import html_translate


class ProductTemplateInherit(models.Model):
    _inherit='product.template'

    _rec_names_search = ['name', 'sh_technical_name','default_code','barcode']


    # for sh_task_time
    sh_scale_ids=fields.Many2one('sh.scale',string="Product Scale")
    not_unique_product = fields.Boolean("Not Unique")
    git_repo = fields.Many2one('sh.git.repo',string="Git Repo", tracking=True)


    # sh_migration_check,sh_task_time
    sh_product_counter = fields.Integer("Product Downloads", tracking=True)

    # sh_migration_check,sh_task_time

    migrated_by = fields.Many2one('res.users',string="Migrated By", tracking=True)
    tested_by = fields.Many2one('res.users',string="Tested By", tracking=True)
    responsible_user = fields.Many2one('res.users',string="Responsible User ", tracking=True)
    status = fields.Selection([('done','Done'),('in_progress','In Progress'),('designing','Designing'),('testing','Testing'),('testing_issue', 'Testing Issue'),('final_testing', 'Final Testing'),('issue','Issue'),('major_issue','Major Issue'),('deprecated','Deprecated'),('unpublished','Unpublished'),('enterprise','Enterprise')],string="Status", tracking=True)
    pylint_score = fields.Float("Pylint Score",  tracking=True)
    multi_company = fields.Boolean("Multi Company", tracking=True)
    multi_language = fields.Boolean("Multi Lang", tracking=True)
    multi_website = fields.Boolean("Multi Website", tracking=True)
    index_state = fields.Selection([('no_change','No Change'),('new_video','New Video'),('new_index','New Index'),('ss_replaced','SS Replaced')],string="Index State", tracking=True)    
    ready_for_release = fields.Boolean("Ready For Release", tracking=True)
    warning_removed = fields.Boolean("Warning Removed", tracking=True)
    check_down_version = fields.Boolean("Check Downgrade Version", tracking=True)
    comment = fields.Text("Comment", tracking=True)
    last_update_by =fields.Many2one("res.users",string="Last Updated By")

    # sh_backend
    sh_technical_name = fields.Char("Technical Name")


    resposible_user_id=fields.Many2one('res.users',string="Assign To")
    other_responsible_users = fields.Many2many('res.users',string = "Other Responsible Users")
    sh_task_created = fields.Boolean(string="Task created", copy=False)
    related_task=fields.Many2one('project.task',string="Relatd Task",copy=False)
    copyright_claim_user = fields.Many2one('res.users',"Copyright Claim User")
    individual_modules = fields.Many2many('product.template','template_individual_all_in_one_rel','individual_id','all_in_one_id',string = "Individual Modules")
    

    sh_scale_ids=fields.Many2one('sh.scale',string="Product Scale")
 
    banner = fields.Binary('Banner', compute='_compute_sh_detail',store=True,  inverse='_set_sh_detail')
    tag_ids = fields.Many2many('product.tags', 'rel_tag_ids', string='Tags', compute='_compute_sh_detail',store=True,  inverse='_set_sh_detail')
    depends = fields.Many2many('sh.depends', 'rel_depends', string='Depends', compute='_compute_sh_detail',store=True,  inverse='_set_sh_detail')
    required_apps = fields.Many2many('sh.required.apps','rel_apps',string="Apps", compute='_compute_sh_detail',store=True,  inverse='_set_sh_detail')
    license = fields.Many2one('sh.license', string='License', compute='_compute_sh_detail',store=True,  inverse='_set_sh_detail')
    product_version = fields.Char('Product Version', compute='_compute_sh_detail',store=True,  inverse='_set_sh_detail')
    supported_browsers = fields.Many2many('product.browsers', 'rel_supported_browsers', string='Supported Browsers', compute='_compute_sh_detail',store=True,  inverse='_set_sh_detail')
    released_date = fields.Date('Released', compute='_compute_sh_detail',store=True,  inverse='_set_sh_detail')
    last_updated_date = fields.Date('Last Updated', compute='_compute_sh_detail',store=True,  inverse='_set_sh_detail')
    live_demo = fields.Char('Live Demo', compute='_compute_sh_detail',store=True,  inverse='_set_sh_detail')
    user_guide = fields.Char('User Guide', compute='_compute_sh_detail',store=True,  inverse='_set_sh_detail')
    related_video = fields.Many2many('blog.post.video', 'rel_related_video', string='video', compute='_compute_sh_detail',store=True,  inverse='_set_sh_detail')
    qty_show = fields.Boolean('QTY Show', compute='_compute_sh_detail',store=True,  inverse='_set_sh_detail')
    sh_features = fields.Html('Features', sanitize_attributes=False, translate=html_translate, compute='_compute_sh_detail',store=True,  inverse='_set_sh_detail')
    sh_blog_post_ids = fields.Many2many('blog.post', string='Blogs', compute='_compute_sh_detail',store=True,  inverse='_set_sh_detail')
    product_change_log_id = fields.One2many('product.change.log','product_id','Product Change Log')
    request_for_quotation = fields.Boolean("Request for Quotation ?", compute='_compute_sh_detail',store=True,  inverse='_set_sh_detail') 
    euro_price = fields.Float("Euro Price", compute='_compute_sh_detail',store=True,  inverse='_set_sh_detail')
    sh_edition_ids=fields.Many2many('sh.edition',string="Edition", compute='_compute_sh_detail',store=True,  inverse='_set_sh_detail')
    website_description = fields.Html('Description for the website', sanitize_attributes=False, translate=html_translate,compute="_compute_sh_detail",store=True,  inverse='_set_sh_detail')

    module_last_updated_date = fields.Date(string="Last Update Date") 

    #duplicate fields
    banner_duplicate = fields.Binary('Banner(D)')
    tag_ids_duplicate = fields.Many2many('product.tags', 'rel_tag_ids2', string='Tags(D)')
    depends_duplicate = fields.Many2many('sh.depends', 'rel_depends2', string='Depends(D)')
    required_apps_duplicate = fields.Many2many('sh.required.apps','rel_apps2',string="Apps(D)")
    license_duplicate = fields.Many2one('sh.license', string='License(D)')
    product_version_duplicate = fields.Char('Product Version(D)')
    supported_browsers_duplicate = fields.Many2many('product.browsers', 'rel_supported_browsers2', string='Supported Browsers(D)')
    released_date_duplicate = fields.Date('Released(D)')
    last_updated_date_duplicate = fields.Date('Last Updated(D)')
    live_demo_duplicate = fields.Char('Live Demo(D)')
    user_guide_duplicate = fields.Char('User Guide(D)')
    related_video_duplicate = fields.Many2many('blog.post.video', 'rel_related_video2', string='video(D)')
    qty_show_duplicate = fields.Boolean('QTY Show(D)')
    sh_features_duplicate = fields.Html('Features(D)', sanitize_attributes=False, translate=html_translate)
    sh_blog_post_ids_duplicate = fields.Many2many('blog.post','rel_product_blog2', string='Blogs(D)')
    request_for_quotation_duplicate = fields.Boolean("Request for Quotation ?(D)") 
    euro_price_duplicate = fields.Float("Euro Price(D)")
    sh_edition_ids_duplicate=fields.Many2many('sh.edition','rel_product_edition2',string="Edition(D)")
    website_description_duplicate = fields.Html('Description for the website(D)', sanitize_attributes=False, translate=html_translate)

    last_updated_2=fields.Date()

    def _set_sh_detail(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.banner = template.banner
                template.product_variant_ids.tag_ids = template.tag_ids.ids
                template.product_variant_ids.depends =  [(6,0,template.depends.ids)]
                template.product_variant_ids.required_apps =  [(6,0,template.required_apps.ids)]
                
                # template.product_variant_ids.license =  [(6,0,template.license.ids)]
                template.product_variant_ids.license =  template.license.id
                template.product_variant_ids.product_version = template.product_version
                template.product_variant_ids.supported_browsers = [(6,0,template.supported_browsers.ids)]
                template.product_variant_ids.released_date = template.released_date
                template.product_variant_ids.last_updated_date = template.last_updated_date
                template.product_variant_ids.live_demo = template.live_demo
                template.product_variant_ids.user_guide = template.user_guide
                template.product_variant_ids.related_video = [(6,0,template.related_video.ids)]
                template.product_variant_ids.qty_show = template.qty_show
                template.product_variant_ids.sh_features = template.sh_features
                template.product_variant_ids.euro_price = template.euro_price
                template.product_variant_ids.sh_edition_ids = [(6,0,template.sh_edition_ids.ids)]
                template.product_variant_ids.sh_blog_post_ids = [(6,0,template.sh_blog_post_ids.ids)]
                template.product_variant_ids.website_description = template.website_description

    @api.depends('product_variant_ids', 'product_variant_ids.banner'
                 , 'product_variant_ids.tag_ids',  'product_variant_ids.depends','product_variant_ids.required_apps', 'product_variant_ids.license'
                 , 'product_variant_ids.product_version', 'product_variant_ids.supported_browsers','product_variant_ids.released_date', 'product_variant_ids.last_updated_date'
                 ,'product_variant_ids.live_demo', 'product_variant_ids.user_guide', 'product_variant_ids.related_video', 'product_variant_ids.qty_show',
                 'product_variant_ids.sh_features','product_variant_ids.euro_price',
                 'product_variant_ids.sh_blog_post_ids', 'product_variant_ids.sh_edition_ids',
                 'product_variant_ids.website_description')

    def _compute_sh_detail(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.banner = template.product_variant_ids.banner
            template.tag_ids = [(6,0,template.product_variant_ids.tag_ids.ids)]
            template.depends = [(6,0,template.product_variant_ids.depends.ids)]
            template.required_apps = [(6,0,template.product_variant_ids.required_apps.ids)]
             
            template.license = template.product_variant_ids.license.id
            template.product_version = template.product_variant_ids.product_version
            template.supported_browsers = [(6,0,template.product_variant_ids.supported_browsers.ids)]
            template.released_date = template.product_variant_ids.released_date
            template.last_updated_date = template.product_variant_ids.last_updated_date
            template.live_demo = template.product_variant_ids.live_demo
            template.user_guide = template.product_variant_ids.user_guide
            template.related_video = [(6,0,template.product_variant_ids.related_video.ids)]
            template.qty_show = template.product_variant_ids.qty_show
            template.sh_features = template.product_variant_ids.sh_features
            template.euro_price = template.product_variant_ids.euro_price
            template.sh_edition_ids = [(6,0,template.product_variant_ids.sh_edition_ids.ids)]
            template.sh_blog_post_ids = [(6,0,template.product_variant_ids.sh_blog_post_ids.ids)]
            template.website_description = template.product_variant_ids.website_description
        for template in (self - unique_variants):
            template.banner = False
            template.tag_ids = False
            template.depends = False
            template.required_apps  = False
            template.license = False
            template.product_version = False
            template.supported_browsers = False
            template.released_date = False
            template.last_updated_date =False
            template.live_demo = False
            template.user_guide =False
            template.related_video = False
            template.qty_show = False
            template.sh_features = False
            template.euro_price = False
            template.sh_edition_ids = False
            template.sh_blog_post_ids = False
            template.website_description = False

    def get_product_image_ids(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Images",
            "view_mode": "kanban,tree,form",
            "res_model": "product.image",
            "domain": [("product_tmpl_id", "=", self.id)],
        }
    
    @api.model
    def default_get(self, fields):

        res = super(ProductTemplateInherit, self).default_get(fields)
        res['detailed_type'] = 'service'
        return res

    def get_product_counter(self):
        active_product_ids = self.env['product.template'].search([])
        for product in active_product_ids:
            variant_list = []
            for res in product.product_variant_ids:
                variant_list.append(res.id)            
            if variant_list:
                domain = [('product_id', 'in', variant_list),('order_id.state','not in',['cancel'])]
                get_all_orders = self.env['sale.order.line'].search(domain)
                total_sold = 0
                for data in get_all_orders:
                    total_sold += data.product_uom_qty
                # if total_sold:
                #     product.sudo().write({'sh_product_counter':total_sold})
                product.sudo().write({'sh_product_counter':total_sold})

    # --------------------------------------------
    #  Multi Action: Add Responsible Users
    # --------------------------------------------

    def multi_action_add_responsible_users(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Add Responsible Users',
            'view_mode': 'form',
            'res_model': 'sh.responsible.users.wizard',
            'context': {
                'default_tmpl_ids': [(6, 0, self.ids)]
            },
            'target': 'new'
        }