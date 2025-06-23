from odoo import api, exceptions, fields, models, _

class Template(models.Model):
    _name = 'sh.template'

    name = fields.Char(string = "Name",required=True)
    group_ids = fields.Many2many('res.groups',string="Groups",)
    menu_ids = fields.Many2many('ir.ui.menu',string = "Hide Menus",)