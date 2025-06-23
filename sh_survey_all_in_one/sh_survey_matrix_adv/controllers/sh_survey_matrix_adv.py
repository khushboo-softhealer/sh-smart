# Copyright (C) Softhealer Technologies.

import json
import logging

from odoo import fields, http
from odoo.http import request
from odoo.addons.survey.controllers.main import Survey

_logger = logging.getLogger(__name__)


class SurveyController(http.Controller):

    @http.route('/survey/matrix/download/<string:question_id>/<string:row_label>/<string:col_label>/<string:answer_token>', type='http', auth='public', website=True)
    def survey_matrix_download_file(self, **post):
        base_url = request.env['ir.config_parameter'].sudo(
        ).get_param('web.base.url')
        download_url = base_url
        if base_url and post.get('question_id') and post.get('row_label') and post.get('col_label') and post.get('answer_token'):
            input_line_id = request.env['survey.user_input.line'].sudo().search([('user_input_id.access_token', '=', post.get('answer_token')),
                                                                                 ('question_id', '=', int(
                                                                                     post.get('question_id'))),
                                                                                 ('suggested_answer_id', '=', int(
                                                                                     post.get('col_label'))),
                                                                                 ('matrix_row_id', '=', int(
                                                                                     post.get('row_label')))
                                                                                 ], limit=1)
            if input_line_id:
                download_url += '/web/content/survey.user_input.line/' + \
                    str(input_line_id.id)+'/value_ans_sh_file?download=true'
        return request.redirect(download_url)
