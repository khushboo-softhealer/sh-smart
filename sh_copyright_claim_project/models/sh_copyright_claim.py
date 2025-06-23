# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class CopyRightClaim(models.Model):
    _name = "sh.copyright.claim"
    _description = "CopyRight Claim"
    _rec_name = "product_id"

    product_id = fields.Many2one(comodel_name='product.template',
                                 string='Product',
                                 required=True)
    sh_technical_name = fields.Char("Technical Name")
    claim_data = fields.Text(string='Claim Data')
    task_id = fields.Many2one(comodel_name='project.task', string='Task')

    git_hub_url = fields.Char(
        string="Github URL", related="product_id.git_hub_url")
    odoo_url = fields.Char(string='Appstore URL',
                           related="product_id.odoo_url")
    soft_url = fields.Char(string='Softhealer URL',
                           related="product_id.soft_url")
    product_ids = fields.Many2many(comodel_name='product.template',
                                   string='Products')
    odoo_urls = fields.Char(string='Appstore URLS',
                            compute='_compute_odoo_urls')
    git_hub_urls = fields.Char(string='Github URLS')
    is_claim = fields.Selection(
        [('pending', 'Pending'), ('found', 'Found'), ('not_found', 'Not Found')], default='pending')
    claim_data_search = fields.Char("Claim Data Check")
    product_technical_name = fields.Char("Product Techinal Name")
    company_id = fields.Many2one('res.company', string='Company',
        default=lambda self: self.env.company)
    
    def claim_found(self):
        self.is_claim = 'found'

    def claim_notfound(self):
        self.is_claim = 'not_found'

    # =======================
    # Compute Methods
    # =======================

    @api.depends('product_ids', 'odoo_urls', 'git_hub_urls')
    def _compute_odoo_urls(self):
        print('\n\n\n>>> _compute_odoo_urls')
        for rec in self:
            rec.odoo_urls = rec.git_hub_urls = ''
            odoo_url = git_url = []
            if rec.product_ids:
                print('\n>>> rec.product_ids: ', rec.product_ids)
                for products in rec.product_ids:
                    if products.odoo_url:
                        odoo_url.append(products.odoo_url)
                        odoo_source = ', '.join(odoo_url)
                        rec.odoo_urls = odoo_source
                    if products.git_hub_url:
                        git_url.append(products.git_hub_url)
                        git_source = ', '.join(git_url)
                        rec.git_hub_urls = git_source

    # =======================
    # Onchange Methods
    # =======================

    @api.onchange('product_technical_name')
    def search_product_tech_name(self):
        if self.product_technical_name:
            if ',' in self.product_technical_name:
                product_list = self.product_technical_name.split(',')
            else:
                product_list = [self.product_technical_name]
            for data in product_list:
                find_product = self.env['product.template'].search(
                    [('sh_technical_name', '=', data)], limit=1)
                if find_product:
                    self.product_ids = find_product.ids

    @api.onchange('claim_data_search')
    def check_claim_input(self):
        check_all_claims = self.env['sh.copyright.claim'].search([])
        claimed = 0
        for data in check_all_claims:
            if data.claim_data:
                claim_list = data.claim_data.split('\n')
                if self.claim_data_search in claim_list:
                    claimed += 1
        if self.claim_data:
            claim_list = self.claim_data.split('\n')
            if self.claim_data_search in claim_list:
                claimed += 1
        if claimed != 0:
            self.claim_data_search = ''
            raise UserError(_("This is already Claimed"))
        else:
            if self.claim_data:
                self.claim_data = self.claim_data + '\n' + self.claim_data_search
            else:
                self.claim_data = self.claim_data_search
            self.claim_data_search = ''

    @api.onchange('sh_technical_name')
    def onchange_sh_technical_name(self):
        if self.sh_technical_name:
            get_product = self.env['product.template'].search([
                ('sh_technical_name', '=', self.sh_technical_name)
            ])
            if len(get_product) > 1:
                raise UserError(
                    _('Multiple Product with same Technical name !!.'))
            else:
                if get_product:
                    self.product_id = get_product.id
                else:
                    self.product_id = False

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            if self.product_id.git_repo:
                if self.product_id.git_repo.repo_link:
                    self.git_hub_url = self.product_id.git_repo.repo_link
            if self.product_id.odoo_url:
                self.odoo_url = self.product_id.odoo_url
            if self.product_id.soft_url:
                self.soft_url = self.product_id.soft_url
