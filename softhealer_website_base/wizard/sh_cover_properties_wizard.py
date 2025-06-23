# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.json import scriptsafe as json_safe


class ShCoverProperties(models.TransientModel):
    _name = "sh.cover.property"
    _description = "Sh Cover Property"

    cover_image = fields.Binary(string="Cover Image",attachment=True,)
    image_name = fields.Char(string="Image Name",store=True)
    image_url = fields.Text(string="Image URL")
    blog_id = fields.Many2one('blog.post',string="Blog")
    def generate_image_url(self):

        self.blog_id.sh_image_attachment_id.sudo().unlink()

        attachment = self.env['ir.attachment'].sudo().create({
            'name': self.image_name,
            'datas':self.cover_image,
            'type':'binary',
            'res_model':self.env.context.get('active_model'),
            'public':True
        })
    
        if attachment:
            self.image_url = f"url(/web/image/{attachment.id}/{attachment.name})"
            
            self.blog_id.sudo().write({'cover_properties': json_safe.dumps({
                                                                        "background-image":self.image_url ,
                                                                        "background_color_class": "o_cc3",
                                                                        "opacity": "0.2",
                                                                        "resize_class": "o_half_screen_height"}
                                                                        ),
                                        'sh_image_attachment_id' : attachment.id }) 
    