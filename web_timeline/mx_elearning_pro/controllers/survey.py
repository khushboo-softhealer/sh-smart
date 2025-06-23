from odoo import http
from odoo.http import request
from odoo.addons.survey.controllers.main import Survey


class ProctorSurvery(http.Controller):

    @http.route('/get/autoproctor/credentials', type='json', auth="user")
    def get_autoproctor_survey_creds(self):
        client_id = request.env['ir.config_parameter'].sudo().get_param('mx_elearning_pro.autoproctor_client_id')
        client_secret = request.env['ir.config_parameter'].sudo().get_param('mx_elearning_pro.autoproctor_client_secret')
        return {
            'client_id': client_id,
            'client_secret': client_secret,
        }

    @http.route('/get/autoproctor/enabled', type='json', auth="public")
    def get_autoproctor_enable(self, **params):
        survey_id = request.env['survey.survey'].with_context(active_test=False).sudo().search([('access_token', '=', params.get('survey_token'))])
        is_proctoring = False
        if survey_id.is_proctoring:
            is_proctoring = True
        return {
            'is_proctoring': is_proctoring
        }

    @http.route('/survey/save/proctor', type='json', auth="user")
    def get_survey_creds(self, survey_token, answer_token, proctor_data):
        survey_obj = request.env['survey.survey'].with_context(active_test=False).sudo().search([('access_token', '=', survey_token)])
        answer_obj = request.env['survey.user_input'].sudo().search([
            ('survey_id', '=', survey_obj.id),
            ('access_token', '=', answer_token)
        ], limit=1)
        score = proctor_data['attemptDetails']['trustScore'] * 100
        answer_obj.proctor_scoring_percentage = round(score, 2)
        if 'evidence' in proctor_data['reportData']:
            response_data = []
            for data in proctor_data['reportData']['evidence']:
                if isinstance(data, list):
                    for item in data:
                        response_data.append((0, 0, {
                            'evidence_url': item.get('evidenceUrl') if 'evidenceUrl' in data else '',
                            'message': item.get('message') if 'message' in data else '',
                            'label': item.get('label') if 'label' in data else '',
                            'violation': item.get('violation') if 'violation' in data else '',
                        }))
                elif isinstance(data, dict):
                    response_data.append((0, 0, {
                        'evidence_url': data.get('evidenceUrl') if 'evidenceUrl' in data else '',
                        'message': data.get('message') if 'message' in data else '',
                        'label': data.get('label') if 'label' in data else '',
                        'violation': data.get('violation') if 'violation' in data else '',
                    }))
                elif isinstance(data, type(None)):
                    pass
            answer_obj.sudo().write({'evidence_ids': response_data})
        return {
            'answer_id': answer_obj
        }