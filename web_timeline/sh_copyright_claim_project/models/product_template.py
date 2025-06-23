# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    odoo_url = fields.Char(string='Appstore URL', compute='_compute_odoo_url')
    soft_url = fields.Char(string='Softhealer URL',
                           compute='_compute_soft_url')
    git_hub_url = fields.Char(
        string="Github URL", related="git_repo.repo_link")
    claim_created = fields.Boolean("Claim Created")

    def update_claim_user(self):
        return {
            'name': 'Claim Responsible User',
            'res_model': 'sh.claim.user.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('sh_copyright_claim_project.claim_user_wizard_form').id,
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {'default_product_ids': [(6, 0, self.env.context.get('active_ids'))]}
        }

    def _compute_odoo_url(self):
        for record in self:
            url = ''
            if record.sh_technical_name:
                url = 'https://apps.odoo.com/apps/modules/'
                if record.attribute_line_ids:
                    get_version_attributes = record.attribute_line_ids.filtered(
                        lambda r: r.attribute_id.name == 'Version')
                    if get_version_attributes:
                        len(get_version_attributes.value_ids)
                        get_latest_version = self.env[
                            'product.attribute.value'].browse(
                                get_version_attributes.value_ids.ids[
                                    len(get_version_attributes.value_ids) - 1])
                        if len(get_latest_version.name.split(' ')) > 1:
                            url += get_latest_version.name.split(' ')[
                                1] + '.0' + "/"
                            if record.sh_technical_name:
                                url += record.sh_technical_name
            record.odoo_url = url

    def _compute_soft_url(self):
        for record in self:
            url = ''
            domain = [('key', '=', 'web.base.url')]
            config = self.env['ir.config_parameter'].sudo().search(domain)
            url = config.value
            url += record.website_url
            record.soft_url = url

    def redirect_store(self):
        return {
            'type': 'ir.actions.act_url',
            'url': self.odoo_url,
            'target': 'new',
        }

    def redirect_shop(self):
        return {
            'type': 'ir.actions.act_url',
            'url': self.soft_url,
            'target': 'new',
        }
