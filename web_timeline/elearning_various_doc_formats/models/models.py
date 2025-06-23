# -*- coding: utf-8 -*-

import requests
from odoo import api, fields, models
from odoo.http import request


class SlideInherit(models.Model):
    _inherit = 'slide.slide'

    various_doc_formats = fields.Boolean(string='Office Doc Formats', required=False, default=False)
    type_viewer = fields.Selection(
        selection=[('google_drive', 'Google Drive'), ('Microsoft_Office', 'Microsoft Office')], default='google_drive')
    filename = fields.Char("Filename")

    @api.depends('slide_category', 'google_drive_id', 'video_source_type', 'youtube_id')
    def _compute_embed_code(self):
        res = super()._compute_embed_code()
        request_base_url = request.httprequest.url_root if request else False
        for record in self:
            base_url = request_base_url or record.get_base_url()
            if not base_url:
                base_url = record.get_base_url()
            if base_url[-1] == '/':
                base_url = base_url[:-1]

            if record.various_doc_formats and record.slide_category == 'document' and record.source_type == 'local_file':
                base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                access_url = base_url + "/my/elearning/file/download/%s/%s" % (record.id, record.filename)

                # Usa Google Docs Viewer en lugar del visor de Office
                if record.type_viewer == 'google_drive':
                    encoded_url = requests.utils.quote(access_url, safe='')
                    record.embed_code = '<iframe src="https://docs.google.com/viewer?url=%s&embedded=true" class="o_wslides_iframe_viewer" allowFullScreen="true" height="%s" width="%s" frameborder="0"></iframe>' % (
                        encoded_url, 315, 420)
                else:
                    # Para otros tipos de archivos, usar el visor de Office
                    record.embed_code = '<iframe src="https://view.officeapps.live.com/op/embed.aspx?src=%s" class="o_wslides_iframe_viewer" allowFullScreen="true" height="%s" width="%s" frameborder="0"></iframe>' % (
                        access_url, 315, 420)

        return res
