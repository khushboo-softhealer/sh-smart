# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api


PRIORITIES = [
    ('0', '1'),
    ('1', '2'),
    ('2', '3'),
    ('3', '4'),
    ('4', '5'),
    ('5', '6'),
]


class sh_testimonial(models.Model):
    _name = "sh.testimonial"
    _description = "Testimonial"
    _order = "id desc"

    comment = fields.Text(string="Comment", translate=True)
    name = fields.Char()
    active = fields.Boolean(string="Active", default=True)
    sh_image = fields.Image(string="Image")
    function = fields.Char(string="Job Position")
    priority = fields.Selection(
        PRIORITIES, default=PRIORITIES[0][0],
        index=True, string="Priority")
    
