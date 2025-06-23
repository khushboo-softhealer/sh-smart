# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

class ShArticalCategories(models.Model):
    _name = 'sh.article.categories'
    _description = "Article Category"
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = 'sh_complete_name'
    _order = 'sh_complete_name'

    name = fields.Char(string="Name",index=True, required=True)
    parent_id = fields.Many2one("sh.article.categories",string="Parent Categories", index=True, ondelete='cascade')
    child_id = fields.One2many('sh.article.categories', 'parent_id', string='Children Categories')
    sh_complete_name = fields.Char(
        'Display Name', compute='_sh_compute_complete_name', recursive=True,
        store=True)
    parent_path = fields.Char(index=True)
    sh_responsible_user_id = fields.Many2one('res.users',string='Responsible',domain=[('share','=',False)])


    @api.depends('name', 'parent_id.sh_complete_name')
    def _sh_compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.sh_complete_name = '%s / %s' % (category.parent_id.sh_complete_name, category.name)
            else:
                category.sh_complete_name = category.name

    @api.constrains('parent_id')
    def _check_category_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_('You cannot create recursive article categories.'))
        
    @api.model
    def name_create(self, name):
        return self.create({'name': name}).name_get()[0]

    def name_get(self):
        if not self.env.context.get('hierarchical_naming', True):
            return [(record.id, record.name) for record in self]
        return super().name_get()