# Part of Softhealer Technologies.

from odoo import http
from odoo.http import request


class SurveyController(http.Controller):

    @http.route(['/survey/get_many2many_field_data'], type='json', auth="public", methods=['POST'])
    def get_many2many_field_data(self, **kw):
        records = []
        rec_name = False
        if kw.get("model_id", False):
            modelRecord = request.env["ir.model"].sudo().search([
                ('id', '=', kw.get("model_id"))
            ], limit=1)
            if modelRecord:
                modelRecord = modelRecord.sudo()
                rec_name = modelRecord._rec_name
                rec_name = 'display_name'
                records = request.env[modelRecord.model].sudo(
                ).search_read([], fields=[rec_name, 'id'])

                # give any rec_name value to name key in record in order to use in js.
                if records:
                    records = [dict(item, name=item.get(rec_name))
                               for item in records]
        return dict(
            records=records,
            rec_name=rec_name,
        )

    @http.route(['/survey/get_many2one_field_data'], type='json', auth="public", methods=['POST'])
    def get_many2one_field_data(self, **kw):
        records = []
        rec_name = False
        if kw.get("model_id", False):
            modelRecord = request.env["ir.model"].sudo().search([
                ('id', '=', kw.get("model_id"))
            ], limit=1)
            if modelRecord:
                modelRecord = modelRecord.sudo()
                rec_name = modelRecord._rec_name
                records = request.env[modelRecord.model].sudo(
                ).search_read([], fields=[rec_name, 'id'])

                # give any rec_name value to name key in record in order to use in js.
                if records:
                    records = [dict(item, name=item.get(rec_name))
                               for item in records]

        return dict(
            records=records,
            rec_name=rec_name,
        )

    @http.route(['/survey/get_countries'], type='json', auth="public", methods=['POST'])
    def get_countries(self, **kw):
        return dict(
            countries=request.env["res.country"].sudo(
            ).search_read([], fields=['name', 'id']),
            country_states=request.env["res.country"].state_ids,
        )

    @http.route(['/survey/get_ountry_info/<model("res.country"):country>'], type='json', auth="public", methods=['POST'])
    def get_ountry_info(self, country, **kw):
        return dict(
            states=[(st.id, st.name, st.code) for st in country.state_ids],
            phone_code=country.phone_code,
            zip_required=country.zip_required,
            state_required=country.state_required,
        )

    @http.route('/survey/download/<string:answer_id>/<string:question_id>/<string:answer_token>', type='http', auth='public', website=True)
    def survey_download_file(self, **post):
        base_url = request.env['ir.config_parameter'].sudo(
        ).get_param('web.base.url')
        download_url = base_url
        if base_url and post.get('answer_id') and post.get('question_id') and post.get('answer_token'):
            input_line_id = request.env['survey.user_input.line'].sudo().search([('user_input_id.access_token', '=', post.get(
                'answer_token')), ('question_id', '=', int(post.get('question_id'))), ('user_input_id', '=', int(post.get('answer_id')))], limit=1)
            if input_line_id:
                download_url += '/web/content/survey.user_input.line/' + \
                    str(input_line_id.id)+'/value_ans_sh_file?download=true&access_token=' + \
                    post.get('answer_token')
        return request.redirect(download_url)
