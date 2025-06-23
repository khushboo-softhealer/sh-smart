from odoo import fields, models

class Template(models.Model):
    _name = 'sh.template'
    _description = "Template"

    name = fields.Char(string="Name", required=True)
    group_ids = fields.Many2many('res.groups', string="Groups",)
    menu_ids = fields.Many2many('ir.ui.menu', string="Hide Menus",)
