# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api


class ShGithubProductTempl(models.Model):
    _inherit = "product.template"

    latest_version = fields.Integer(
        'Latest Version', compute='_compute_latest_version')


    @api.depends('attribute_line_ids')
    def _compute_latest_version(self):
        '''
            Compute the latest product version,
            based on the module queue (Modules are available on github)
            not based on the product variant
            Because sometimes product variant created before the module developed
            Lime v17 migration process
        '''
        for rec in self:
            latest_version = 0
            if rec.sh_technical_name:
                modules = self.env['sh.module'].sudo().search([
                    ('name', '=', rec.sh_technical_name)
                ])
                if modules:
                    for module in modules:
                        if module.sh_branch_id:
                            try:
                                module_version = int(module.sh_branch_id.name.split('.')[0])
                                if module_version > latest_version:
                                    latest_version = module_version
                            except:
                                pass
            elif rec.attribute_line_ids:
                # if rec.attribute_line_ids[0].attribute_id.name == 'Version':
                for version in rec.attribute_line_ids[0].value_ids:
                    try:
                        if 'Odoo' in version.name:
                            version_int = int(version.name.split(' ')[1])
                            if latest_version < version_int:
                                latest_version = version_int
                    except:
                        pass
            rec.latest_version = latest_version

    def update_euro_price(self, vals):
        if 'euro_price_duplicate' in vals:
            products = self.env['product.product'].sudo().search([
                ('sh_technical_name', '=', self.sh_technical_name)
            ])
            for product in products:
                product.sudo().write({
                    'euro_price': vals.get('euro_price_duplicate')
                })

    def write(self, vals):
        for rec in self:
            rec.update_euro_price(vals)
        # return super(ShGithubProductTempl, self).sudo().write(vals)
        return super(ShGithubProductTempl, self).write(vals)
