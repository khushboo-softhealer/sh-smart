# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo.http import request
from odoo import http
from odoo.addons.http_routing.models.ir_http import slug
import base64
from odoo.tools import image_to_base64
from PIL import Image
try:
    from PIL import WebPImagePlugin
    assert WebPImagePlugin
except ImportError:
        pass

import io



class Main(http.Controller):

    @http.route('/theme_softhealer_website/get_data', type='json', auth="public",methods=['POST'], website=True)
    def get_data(self):
        self = request
        image_slider = self.env['sh.image.slider'].sudo().search([("website_published","=","True")],order="sequence asc")
        
        data = []
        for record in image_slider:

            record_dict = {}
            img_src = []
           
            img_src.append(record.img.decode())
            for attachment in record.images:
                if attachment.image_1920:
                    # Condition to check the image format
                    i = attachment.image_1920
                    image_base64 = i.decode() #base64.b64decode(i)
                    # image = Image.open(io.BytesIO(image_base64))
                    # webp_datas = image_to_base64(image, output_format="WEBP", quality=100)
                    img_src.append(image_base64)
            
            record_dict.update({'name':record.name,
                                'sub_title':record.sub_title,
                                'img_thumb': 'data:image/webp;base64,'+record.img.decode(), 
                                'image_src' : img_src,
                                'published':record.website_published,})
            data.append(record_dict)


        return {'data':self.env["ir.ui.view"].sudo()._render_template('theme_softhealer_website.sh_image_slider_snippet_tmpl', values={
                'data': data,
            })}
        

