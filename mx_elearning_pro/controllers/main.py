# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
import werkzeug
from odoo import http
from odoo.http import request
from datetime import datetime, date
from odoo import http, tools, _, exceptions
from odoo.tools import plaintext2html
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website_slides.controllers.main import WebsiteSlides


class SWebsitelideController(http.Controller):

    @http.route(['/website/publish/slide'], type='json', auth="user", website=True)
    def publish(self, id):
        slide_id = request.env['slide.slide'].browse(id)
        return bool(slide_id.website_published)
    
    @http.route(['/slides/slide/mx/like'], type='json', auth="public", website=True)
    def slide_like_dislike(self, slide_id):
        slide = request.env['slide.slide'].browse(slide_id)
        return {
            'user_vote': slide.user_vote,
            'likes': tools.format_decimalized_number(slide.likes),
            'dislikes': tools.format_decimalized_number(slide.dislikes),
        }

    def _portal_post_has_content(self, res_model, res_id, message, attachment_ids=None, **kw):
        """ Tells if we can effectively post on the model based on content. """
        return bool(message) or bool(attachment_ids)
    
    @http.route(['/mail/slide/comment'], type='json', methods=['POST'], auth='public', website=True)
    def portal_chatter_post(self, res_model, res_id, message, attachment_ids=None, attachment_tokens=None, **kw):
        """Create a new `mail.message` with the given `message` and/or `attachment_ids` and return new message values."""
        if not self._portal_post_has_content(res_model, res_id, message,
                                             attachment_ids=attachment_ids, attachment_tokens=attachment_tokens,
                                             **kw):
            return
        res_id = int(res_id)
        result = {'default_message': message}
        # message is received in plaintext and saved in html
        if message:
            message = plaintext2html(message)
        vals = ({
            'email_from': request.env.user.email_formatted,
            'author_id': request.env.user.partner_id.id,
            'message_type':'comment',
            'body':message if message else '',
            'subtype_id': 1,
            'model':res_model,
            'res_id': res_id,
            # 'attachment_ids': False,
            'record_name': (request.env[str(res_model)].browse(res_id)).name
        })
        message=request.env['mail.message'].sudo().create(vals)
        result.update({'default_message_id': message.id})

        if attachment_ids:
            # sudo write the attachment to bypass the read access
            # verification in mail message
            record = request.env[res_model].browse(res_id)
            message_values = {'res_id': res_id, 'model': res_model}
            attachments = record._message_post_process_attachments([], attachment_ids, message_values)

            if attachments.get('attachment_ids'):
                message.sudo().write(attachments)

            result.update({'default_attachment_ids': message.attachment_ids.sudo().read(['id', 'name', 'mimetype', 'file_size', 'access_token'])})
        return result

class SlideController(WebsiteSlides):
    
    @http.route('/slides/slide/like', type='json', auth="public", website=True)
    def slide_like(self, slide_id, upvote):
        res = super(SlideController, self).slide_like(slide_id, upvote)
        return res

    @http.route('/website/channel/resume', type='json', auth="user", website=True)
    def update_channel_resume(self, slide_id):
        slide_id = request.env['slide.slide'].browse(int(slide_id))
        partner_id = request.env.user.partner_id
        partner_channel_obj_sudo = request.env['slide.channel.partner'].sudo()
        partner_channel_id = partner_channel_obj_sudo.search([
            ('channel_id', '=', slide_id.channel_id.id),
            ('partner_id', '=', partner_id.id)
        ], limit=1)
        if partner_channel_id:
            partner_channel_id.mx_resume_slide_id = slide_id.id

    @http.route()
    def slide_view(self, slide, **kwargs):
        res = super(SlideController, self).slide_view(slide, **kwargs)
        self.update_channel_resume(slide)
        return res

    @http.route(['/slides/channel/join'], type='json', auth='public', website=True)
    def slide_channel_join(self, channel_id):
        if request.website.is_public_user():
            return {'error': 'public_user', 'error_signup_allowed': request.env['res.users'].sudo()._get_signup_invitation_scope() == 'b2c'}
        channel = request.env['slide.channel'].browse(channel_id)
        error_dic = {'error_courses': {}}
        for depend_course in channel.mx_slide_channel_ids:
            for course in depend_course.mx_course_id:
                if not course.is_member or depend_course.mx_completion_percent > course.completion:
                    error_dic['error_courses'][depend_course.mx_course_id.name] = depend_course.mx_completion_percent
        if error_dic['error_courses']:
            error_dic['error'] = 'dependency_error'
            return error_dic
        success = request.env['slide.channel'].browse(channel_id).action_add_member()
        if not success:
            return {'error': 'join_done'}
        return success

    def _prepare_additional_channel_values(self, values, **kwargs):
        res = super(SlideController, self)._prepare_additional_channel_values(values)
        partner_id = request.env.user.partner_id
        partner_channel_obj_sudo = request.env['slide.channel.partner'].sudo()
        partner_channel_id = partner_channel_obj_sudo.search([
            ('channel_id', '=', res['channel'].id),
            ('partner_id', '=', partner_id.id)
        ], limit=1)
        if partner_channel_id and partner_channel_id.mx_resume_slide_id:
            res.update({
                'resume_slide_id': '/slides/slide/%s' % (slug(partner_channel_id.mx_resume_slide_id))
            })
        course_ids = request.env['slide.channel'].sudo().search([('id', '=', res['channel'].id)])
        if course_ids:
            for data in course_ids:
                current_date = date.today()
                if data.enrollment_start_date and data.enrollment_end_date:
                    res.update({
                        'check_enroll_start_date':True if (current_date >= data.enrollment_start_date) else False,
                        'check_enroll_end_date': True if (current_date <= data.enrollment_end_date) else False,
                        'enrollment_start_date': data.enrollment_start_date if data.enrollment_start_date else '',
                        'enrollment_end_date': data.enrollment_end_date if data.enrollment_end_date else '',
                        'start_date': data.start_date if data.start_date else '',
                        'end_date': data.end_date if data.end_date else ''
                    })
                res.update({
                    'is_sequential': data.is_sequential if data.is_sequential else False,
                    'is_timer': data.is_timer if data.is_timer else False,
                })
        dependent_courses = {}
        for course in res['channel'].mx_slide_channel_ids:
            dependent_courses.setdefault(course.mx_course_id, {})
            dependent_courses[course.mx_course_id]['slug'] = '/slides/%s' % (slug(course.mx_course_id))
            dependent_courses[course.mx_course_id]['member'] =  course.mx_course_id.is_member
        res.update({
            'dependent_courses': dependent_courses
        })
        return res

    @http.route('/slides/slide/get_scorm_tincan_version', type="json", auth="public", website=True)
    def get_scorm_tincan_version(self, slide_id):
        slide_dict = self._fetch_slide(slide_id)
        scorm_datas = request.env['statement.scorm'].sudo().search([('activityId', '=', int(slide_id)),('user_id','=',request.uid)])
        if scorm_datas:
            return {
                'scorm_version': slide_dict['slide'].scorm_version,
                'type' : slide_dict['slide'].slide_type,
                'is_tincan' : slide_dict['slide'].is_tincan,
                'hasQuestion' : True if slide_dict['slide'].question_ids else None,
                'completed': slide_dict['slide'].user_membership_id.sudo().completed
            }
        else:
            return {
                'scorm_version': slide_dict['slide'].scorm_version,
                'type' : slide_dict['slide'].slide_type,
                'is_tincan' : slide_dict['slide'].is_tincan,
                'hasQuestion' : True if slide_dict['slide'].question_ids else None,
                'completed' : False
            }

    @http.route('/slides/slide/<model("slide.slide"):slide>/set_completed', website=True, type="http", auth="user")
    def slide_set_completed_and_redirect(self, slide, next_slide_id=None):
        if slide.slide_type == 'scorm' and slide.is_tincan:
            scorm_datas = request.env['statement.scorm'].sudo().search([('activityId', '=', int(slide.id)),('user_id','=',request.uid)])
            if scorm_datas:
                if any('passed' in rec.verb_type for rec in scorm_datas):
                    self._slide_mark_completed(slide)
                    next_slide = None
                    if next_slide_id:
                        next_slide = self._fetch_slide(next_slide_id).get('slide', None)
                    return werkzeug.utils.redirect("/slides/slide/%s" % (slug(next_slide) if next_slide else slug(slide)))
                if any('failed' in rec.verb_type for rec in scorm_datas):
                    self._slide_mark_completed(slide)
                    next_slide = None
                    if next_slide_id:
                        next_slide = self._fetch_slide(next_slide_id).get('slide', None)
                    return werkzeug.utils.redirect("/slides/slide/%s" % (slug(next_slide) if next_slide else slug(slide)))
                else:
                    return werkzeug.utils.redirect("/slides/slide/%s" % slug(slide))
            else:
                return werkzeug.utils.redirect("/slides/slide/%s" % slug(slide))
        else:
            res = super(SlideController, self).slide_set_completed_and_redirect(slide,next_slide_id)
            return res

    @http.route('''/slides/slide/<model("slide.slide"):slide>''', type='http', auth="public", website=True, sitemap=True)
    def slide_view(self, slide, **kwargs):
        if not slide.channel_id.can_access_from_current_website() or not slide.active:
            raise werkzeug.exceptions.NotFound()
        # redirection to channel's homepage for category slides
        scorm_completion_on_finish = False
        if slide._fields.get('scorm_completion_on_finish'):
            scorm_completion_on_finish = slide.scorm_completion_on_finish
        if slide.is_category:
            return request.redirect(slide.channel_id.website_url)

        if slide.channel_id.is_timer and slide.can_self_mark_completed and not slide.user_has_completed \
           and slide.channel_id.channel_type == 'training' :
           pass
        elif(not slide.channel_id.is_timer and slide.can_self_mark_completed and not slide.user_has_completed \
            and slide.channel_id.channel_type == 'training' and not scorm_completion_on_finish):
            self._slide_mark_completed(slide)
        else:
            self._set_viewed_slide(slide)

        values = self._get_slide_detail(slide)
        # quiz-specific: update with karma and quiz information
        if slide.question_ids:
            values.update(self._get_slide_quiz_data(slide))
        # sidebar: update with user channel progress
        values['channel_progress'] = self._get_channel_progress(slide.channel_id, include_quiz=True)

        # Allows to have breadcrumb for the previously used filter
        values.update({
            'search_category': slide.category_id if kwargs.get('search_category') else None,
            'search_tag': request.env['slide.tag'].browse(int(kwargs.get('search_tag'))) if kwargs.get('search_tag') else None,
            'slide_categories': dict(request.env['slide.slide']._fields['slide_category']._description_selection(request.env)) if kwargs.get('search_slide_category') else None,
            'search_slide_category': kwargs.get('search_slide_category'),
            'search_uncategorized': kwargs.get('search_uncategorized'),
        })

        values['channel'] = slide.channel_id
        values = self._prepare_additional_channel_values(values, **kwargs)
        values['signup_allowed'] = request.env['res.users'].sudo()._get_signup_invitation_scope() == 'b2c'
        values['scorm_completion_on_finish'] = scorm_completion_on_finish
        if kwargs.get('fullscreen') == '1':
            values.update(self._slide_channel_prepare_review_values(slide.channel_id))
            return request.render("website_slides.slide_fullscreen", values)

        values.pop('channel', None)
        return request.render("website_slides.slide_main", values)
       
    @http.route('/slides/slide/scorm_set_completed', website=True, type="json", auth="user")
    def state_scorm(self, slide_id):
        try:
            scorm_datas = request.env['statement.scorm'].sudo().search([('activityId', '=', int(slide_id)),('user_id','=',request.uid)])
            if scorm_datas:
                if request.website.is_public_user():
                    return {'error': 'public_user'}
                fetch_res = self._fetch_slide(slide_id)
                slide = fetch_res['slide']
                if fetch_res.get('error'):
                    return fetch_res
                if slide.website_published and slide.channel_id.is_member:
                    if any('passed' in rec.verb_type for rec in scorm_datas):
                        return {
                            'channel_completion': fetch_res['slide'].channel_id.completion,
                            'result_passed': True if any('passed' in rec.verb_type for rec in scorm_datas) else False,
                            'result_failed': True if any('failed' in rec.verb_type for rec in scorm_datas) else False,
                            'slide_id':slide_id
                        }
                    if any('failed' in rec.verb_type for rec in scorm_datas):
                         return {
                            'channel_completion': fetch_res['slide'].channel_id.completion,
                            'result_passed': True if any('passed' in rec.verb_type for rec in scorm_datas) else False,
                            'result_failed': True if any('failed' in rec.verb_type for rec in scorm_datas) else False,
                            'slide_id':slide_id
                        }
                    else:
                        return {
                            'channel_completion':fetch_res['slide'].channel_id.completion,
                            'result_passed': False ,
                            'result_failed': False ,
                            'slide_id':slide_id
                        }
            else:
                return {
                    'channel_completion': 0.0,
                    'result_passed': False,
                    'result_failed': False,
                    'slide_id':slide_id
                }
        except(SyntaxError) as e:
            return json.dumps(res = {
                                    "error": str(e)
            })
    
    @http.route(['/slides/channel/leave'], type='json', auth='user', website=True)
    def slide_channel_leave(self, channel_id):
        scorm_slide_ids = request.env['slide.slide'].sudo().search([('channel_id','=',int(channel_id))])
        for data in scorm_slide_ids:
            if data.slide_type == 'scorm' and data.is_tincan:
                scorm_datas = request.env['statement.scorm'].sudo().search([('activityId', '=', int(data.id)),('user_id','=',request.env.user.id)])
                if any('passed' in rec.verb_type for rec in scorm_datas):
                    slide_user_id = request.env['slide.slide'].sudo().search([('id','=',data.id)])
                    user_id = request.env['res.users'].sudo().search([('id','=',int(slide_user_id.user_id.id))])
                    if slide_user_id.tincan_xp:
                        score = request.env['statement.scorm'].sudo().search([('completion','=','True'),('activityId', '=', int(data.id)),('user_id','=',int(user_id))])
                        if len(score)>1:
                            user_id.karma -= int(score[0].scaled_score)*100
                        else:
                            user_id.karma -= int(score.scaled_score)*100
                    else:
                        if slide_user_id.scorm_passed_xp:
                            user_id.karma -= slide_user_id.scorm_passed_xp
                request.env['statement.scorm'].sudo().search([('activityId','=',int(data.id)),('user_id','=',request.uid)]).unlink()
                request.env['state.scorm'].sudo().search([('activityId','=',int(data.id)),('user_id','=',request.uid)]).unlink()
                request.env['user.tincan.response'].sudo().search([('activityId','=',int(data.id)),('user_id','=',request.uid)]).unlink()
                request.env['user.question.choice'].sudo().search([('activity_id','=',int(data.id)),('user_id','=',request.uid)]).unlink()
                request.env['question.attempt'].sudo().search([('activity_id','=',int(data.id)),('user_id','=',request.uid)]).unlink()
                duration = 0
                user_scorm_rec = request.env['statement.scorm'].sudo().search([('completion','=','True'),('activityId','=',data.id)])
                duration_rec = request.env['statement.scorm'].sudo().search([('completion','=','True'),('user_id','=',request.env.user.id),('activityId','=',data.id)])
                if user_scorm_rec:
                    for rec in user_scorm_rec:
                        duration += rec.calculated_duration
                if duration_rec:
                    user_scrom_dur = duration_rec.calculated_duration
                    if duration != 0 and data.completed_user_count >= 2:
                        seconds = ((duration-user_scrom_dur)/(data.completed_user_count-1)) % (24 * 3600)
                        hour = seconds // 3600
                        seconds %= 3600
                        minutes = seconds // 60
                        seconds %= 60
                        data.completion_duration = "%d:%02d:%02d" % (hour, minutes, seconds)
                    elif (duration == 0 and data.completed_user_count) or  data.completed_user_count <= 1:
                        data.completion_duration = ''
            else:
                record = request.env['slide.slide.partner'].sudo().search([('completed','=',True),('slide_id','=',data.id)])
                user_rec = request.env['slide.slide.partner'].sudo().search([('completed','=',True),('partner_id','=',request.env.user.partner_id.id),('slide_id','=',data.id)])
                duration = 0
                if record:
                    for rec in record:
                        duration += (datetime.strptime(rec.write_date.strftime("%H:%M:%S"), "%H:%M:%S") - datetime.strptime(rec.create_date.strftime("%H:%M:%S"), "%H:%M:%S")).total_seconds()
                if user_rec:
                    user_dur = (datetime.strptime(user_rec.write_date.strftime("%H:%M:%S"), "%H:%M:%S") - datetime.strptime(user_rec.create_date.strftime("%H:%M:%S"), "%H:%M:%S")).total_seconds()
                if duration != 0 and data.completed_user_count >= 2:
                        seconds = ((duration-user_dur)/(data.completed_user_count-1)) % (24 * 3600)
                        hour = seconds // 3600
                        seconds %= 3600
                        minutes = seconds // 60
                        seconds %= 60
                        data.completion_duration = "%d:%02d:%02d" % (hour, minutes, seconds)
                elif (duration == 0 and data.completed_user_count) or  data.completed_user_count <= 1:
                        data.completion_duration = ''
        request.cr.execute('''SELECT question_user as question, choice_user as choice, SUM(user_attempts_count_user) AS user_attempts_count 
                    FROM user_question_choice
                    GROUP BY question_user, choice_user
                    ORDER BY question_user, choice_user''')
        result =  request.cr.fetchall()
        if result:
            record = request.env['question.choice'].sudo().search([])
            if record:
                record.unlink()
            for rec in result:
                request.env['question.choice'].sudo().create({'question':rec[0],'choice':rec[1],'user_attempts_count':rec[2]})
        else:
            record = request.env['question.choice'].sudo().search([])
            if record:
                record.unlink()
        request.cr.execute('''SELECT question as question, SUM(first_attempt_count) AS first_attempt_count,
                SUM(second_attempt_count) AS second_attempt_count,
                SUM(third_attempt_count) AS third_attempt_count,
                SUM(more_attempt_count) AS more_attempt_count,
                SUM(wrong_answer_count) AS wrong_answer_count
                FROM question_attempt
                GROUP BY question
                ORDER BY question''')
        result_attempt =  request.cr.fetchall()
        if result_attempt:
            record_attempt = request.env['question.attempt.view'].sudo().search([])
            if record_attempt:
                record_attempt.unlink()
            for rec in result_attempt:
                request.env['question.attempt.view'].sudo().create({'question':rec[0],
                                                                    'first_attempt_count':rec[1],
                                                                    'second_attempt_count':rec[2],
                                                                    'third_attempt_count':rec[3],
                                                                    'more_attempt_count':rec[4],
                                                                    'wrong_answer_count':rec[5]})
        else:
            record_attempt = request.env['question.attempt.view'].sudo().search([])
            if record_attempt:
                record_attempt.unlink() 
        res = super(SlideController, self).slide_channel_leave(channel_id)
        return res

    @http.route(['/slides/slide/activities/state'], type='http', auth='public',website=True,
                methods=['PUT'], csrf=False, cors='*')
    def set_state_scorm(self, **params):
        # try:
            request_payload = request.httprequest.data.decode('utf-8')
            activityId = params.get('activityId')
            stateId = params.get('stateId')
            agent = params.get('agent')
            agent = json.loads(agent)
            user_name = request.env.user.name
            user_email = request.env.user.login
            objectType=agent.get('objectType')
            channel_rec = request.env['slide.slide'].sudo().search([('id', '=', int(activityId))], limit=1)
            scorm_datas = request.env['statement.scorm'].search([('activityId', '=', int(activityId)),('user_id','=',request.env.user.id),('completion','=','True')])
            if not scorm_datas:
                if channel_rec:
                        vals = ({
                            'activityId':activityId,
                            'state':stateId,
                            'user_id':request.uid,
                            'agent_name':user_name,
                            'agent_email':user_email,
                            'object_type':objectType,
                            'request_payload':request_payload,
                            'request_type':'PUT'
                        })
                        request.env['state.scorm'].sudo().create(vals)
        # except(SyntaxError) as e:
        #     return json.dumps(res = {
        #                             "error": str(e)
        #                         })
    
    @http.route(['/slides/slide/activities/state'], type='http', auth='public',website=True,
                methods=['GET'], csrf=False, cors='*')
    def get_state_scorm(self, **params):
        try:
            if params:
                activityId = params.get('activityId')
                stateId = params.get('stateId')
                agent = params.get('agent')
                agent = json.loads(agent)
                user_name = request.env.user.name
                user_email = request.env.user.login
                objectType=agent.get('objectType')
                channel_rec = request.env['state.scorm'].sudo().search([('activityId', '=', int(activityId)),('user_id','=',request.uid)])
                scorm_datas =request.env['statement.scorm'].sudo().search([('activityId', '=', int(activityId)),('user_id','=',request.env.user.id),('completion','=','True')])
                if not scorm_datas :
                    if channel_rec:
                        vals = ({
                                'activityId':activityId,
                                'state':stateId,
                                # 'state_id':activityId,
                                'user_id':request.uid,
                                'agent_name':user_name,
                                'agent_email':user_email,
                                'object_type':objectType,
                                'request_type':'GET'
                            })
                        request.env['state.scorm'].sudo().create(vals)
                        channel_payload = request.env['state.scorm'].sudo().search([('activityId', '=', int(activityId)),('user_id','=',request.uid),('request_type','=','PUT')])
                        return channel_payload[-1].request_payload
                if scorm_datas:
                    channel_payload = request.env['state.scorm'].sudo().search([('activityId', '=', int(activityId)),('user_id','=',request.uid),('request_type','=','PUT')])
                    return channel_payload[-1].request_payload
            else:
                return {
                        'error': {
                            'status_code': '400',
                            'message': 'Data Not found'
                        }
                    }
        except(SyntaxError) as e:
            return json.dumps(res = {
                                    "error": str(e)
                                })

    @http.route(['/slides/slide/statements'], type='json', auth='public',website=True, methods=['PUT'], csrf=False, cors='*')
    def set_statement_scorm(self, **params):
        # try:
            data = json.loads(request.httprequest.data)
            verb_type = data['verb']['display'].get('en-US')
            user_name = request.env.user.name
            user_email = request.env.user.login
            options = []
            correct_option_pattern = ''
            correct_option_patterns = []
            chosen_choices = []
            response = ''
            match_source_options = []
            scaled_score = ''
            min_score = ''
            max_score = ''
            score = ''
            check_success = ''
            if verb_type == 'answered':
                activityId = data['object'].get('id').partition('/')[0]
                object_name = data['object']['definition']['name'].get('und') if data['object']['definition']['name'].get('und') else ''
                interaction_type = data['object']['definition'].get('interactionType') if data['object']['definition'].get('interactionType') else ''
                # if interaction_type == 'numeric':
                # if interaction_type == 'likert':
                if interaction_type == 'choice':
                    if  'choices' in data['object']['definition']:
                        option = data['object']['definition']['choices']
                        option_dict = {sub['id'] : sub['description']['und'] for sub in option}
                        for k, vals in option_dict.items():
                            options.append(vals)
                    if 'correctResponsesPattern' in data['object']['definition']:
                        if '[,]' in data['object']['definition']['correctResponsesPattern'][0]:
                            correct_option_pattern_rec = list(data['object']['definition']['correctResponsesPattern'][0].split('[,]'))
                            for k in correct_option_pattern_rec:
                                if k in option_dict:
                                    correct_option_patterns.append(option_dict[k])
                        if '[,]' not in data['object']['definition']['correctResponsesPattern'][0]:
                            correct_option_pattern_id = data['object']['definition']['correctResponsesPattern'][0]
                            if correct_option_pattern_id in option_dict:
                                correct_option_pattern = option_dict[correct_option_pattern_id]
                    if '[,]' in data['result']['response']:
                        chosen_choices_id = list(data['result']['response'].split('[,]'))
                        for k in chosen_choices_id:
                            if k in option_dict:
                                chosen_choices.append(option_dict[k])
                    if '[,]' not in data['result']['response']:
                        response_id = data['result']['response']
                        if response_id in option_dict:
                                response = option_dict[response_id]
                if interaction_type == 'fill-in':
                    response = data['result']['response']  if 'result' in data else ''
                if interaction_type == 'matching':
                    if 'source' in data['object']['definition']:
                        sources = data['object']['definition']['source']
                        sources_dict = {sub['id'] : sub['description']['und'] for sub in sources}
                        for k, vals in sources_dict.items():
                            match_source_options.append(vals)
                    if 'target' in data['object']['definition']:
                        option = data['object']['definition']['target']
                        option_dict = {sub['id'] : sub['description']['und'] for sub in option}
                        for k, vals in option_dict.items():
                            options.append(vals)
                    if 'correctResponsesPattern' in data['object']['definition']:
                        if '[,]' in data['object']['definition']['correctResponsesPattern'][0]:
                            correct_option_pattern_rec = list(data['object']['definition']['correctResponsesPattern'][0].split('[,]'))
                            for i, j in enumerate(correct_option_pattern_rec):
                                correct_option_pattern_rec[i] = j.rsplit('[.]', 1)[1]
                            for k in correct_option_pattern_rec:
                                if k in option_dict:
                                    correct_option_patterns.append(option_dict[k])
                        if '[,]' not in data['object']['definition']['correctResponsesPattern'][0]:
                            correct_option_pattern_id = data['object']['definition']['correctResponsesPattern'][0]
                            if correct_option_pattern_id in option_dict:
                                correct_option_pattern = option_dict[correct_option_pattern_id]
                    if '[,]' in data['result']['response']:
                        chosen_choices_id = list(data['result']['response'].split('[,]'))
                        for i, j in enumerate(chosen_choices_id):
                            chosen_choices_id[i] = j.rsplit('[.]', 1)[1]
                        for k in chosen_choices_id:
                            if k in option_dict:
                                chosen_choices.append(option_dict[k])
                    if '[,]' not in data['result']['response']:
                        response_id = data['result']['response']
                        if response_id in option_dict:
                                response = option_dict[response_id]
                if interaction_type == 'sequencing':
                    if 'choices' in data['object']['definition']:
                        option = data['object']['definition']['choices']
                        option_dict = {sub['id'] : sub['description']['und'] for sub in option}
                        for k, vals in option_dict.items():
                            options.append(vals)
                    if 'correctResponsesPattern' in data['object']['definition']:
                        if '[,]' in data['object']['definition']['correctResponsesPattern'][0]:
                            correct_option_pattern_rec = list(data['object']['definition']['correctResponsesPattern'][0].split('[,]'))
                            for k in correct_option_pattern_rec:
                                if k in option_dict:
                                    correct_option_patterns.append(option_dict[k])
                        if '[,]' not in data['object']['definition']['correctResponsesPattern'][0]:
                            correct_option_pattern_id = data['object']['definition']['correctResponsesPattern'][0]
                            if correct_option_pattern_id in option_dict:
                                correct_option_pattern = option_dict[correct_option_pattern_id]
                    if '[,]' in data['result']['response']:
                        chosen_choices_id = list(data['result']['response'].split('[,]'))
                        for k in chosen_choices_id:
                            if k in option_dict:
                                chosen_choices.append(option_dict[k])
                    if '[,]' not in data['result']['response']:
                        response_id = data['result']['response']
                        if response_id in option_dict:
                                response = option_dict[response_id]
                if 'success' in data['result']:
                    check_success = data['result'].get('success')
                if 'score' in data['result']:
                    if 'raw' in data['result']['score']:
                        score = int(data['result']['score'].get('raw'))
                channel_rec = request.env['slide.slide'].sudo().search([('id', '=', int(activityId))], limit=1)
                if channel_rec:
                    channel_id = request.env['slide.slide.partner'].sudo().search([('slide_id','=',int(channel_rec.id))], limit=1)
                    vals = ({
                        'name' : channel_rec.name,
                        # 'statement_id':activityId,
                        'activityId' : activityId,
                        'verb_type' : verb_type,
                        'user_name' : user_name,
                        'user_email' : user_email,
                        'object_name' : object_name,
                        'interaction_type' : interaction_type,
                        'correct_option_pattern_ids' : [(0, 0, {
                                                        'name': correct_option_patterns[index]
                                                        }) for index in range(len(correct_option_patterns))] if correct_option_patterns else [(0, 0, {'correct_option_pattern' : correct_option_pattern})] if correct_option_pattern else '',
                        'options_ids' : [(0, 0, {
                                        'name': options[index]
                                        })for index in range(len(options))],
                        'check_success' : check_success,
                        'score' : score,
                        'chosen_choice_ids' : [(0, 0, {
                                                'response': chosen_choices[index],
                                            }) for index in range(len(chosen_choices))] if chosen_choices else [(0, 0, {'response' : response})] if response else '',
                        'user_id' : request.env.user.id
                    })
                    request.env['statement.scorm'].sudo().create(vals)
                if data['object']['definition'].get('interactionType') and 'success' in data['result'] and channel_rec:
                    #To store latest attempt and attempt counts on a question by user for scorm slide
                    record = request.env['user.tincan.response'].sudo().search([('user_id','=',request.uid),('activityId','=',int(activityId)),('question_name','=',str(object_name))])
                    if not record:
                        vals = ({
                            'channel_name' : channel_rec.channel_id.name,
                            'user_id' : request.env.user.id,
                            'activityId' : activityId,
                            'content_name' : channel_rec.name,
                            'user_name' : user_name,
                            'question_name' : object_name,
                            'response_type' : interaction_type,
                            'chosen_choice' : (",".join(chosen_choices)).replace(",",", ") if chosen_choices else response,
                            'marks_allotted' : score,
                            'attempts_count' : 1,
                            'check_answer' : str(check_success),
                            'update_date' : datetime.now() 
                            })
                        request.env['user.tincan.response'].sudo().create(vals)
                    if record:
                        vals = {
                            'question_name' : object_name,
                            'response_type' : interaction_type,
                            'chosen_choice' : (",".join(chosen_choices)).replace(",",", ") if chosen_choices else response,
                            'marks_allotted' : score,
                            'attempts_count' : int(record.attempts_count) + int(1),
                            'check_answer' : str(check_success),
                            'update_date' : datetime.now()
                            }
                        record.write(vals)
                    user_data = request.env['user.question.choice'].sudo().search([('user_id','=',request.env.user.id),('question_user','=',str(object_name))])
                    record = request.env['statement.scorm'].sudo().search([('user_id','=',request.uid),('verb_type','=','answered'),('activityId','=',int(activityId)),('object_name','=',str(object_name))])
                    if len(record)<2 and not user_data:
                        if chosen_choices:
                            for index in range(len(options)):
                                request.env['user.question.choice'].sudo().create({
                                    'user_id' : request.env.user.id,
                                    'activity_id' : activityId,
                                    'question_user' : object_name,
                                    'choice_user' : options[index],
                                    'user_attempts_count_user': int(1) if options[index] in chosen_choices else 0,
                                    })
                        if response:
                            for index in range(len(options)):
                                request.env['user.question.choice'].sudo().create({
                                    'user_id' : request.env.user.id,
                                    'activity_id' : activityId,
                                    'question_user' : object_name,
                                    'choice_user' : options[index],
                                    'user_attempts_count_user': int(1) if options[index] == response else int(0),
                                    })
                    elif (len(record)>=2 and user_data):
                        prev_choices =[]
                        if chosen_choices:
                            if (len(record[-2].chosen_choice_ids)) > 1:
                                for index in record[-2].chosen_choice_ids:
                                    prev_choices.append(index.response)
                                perv_chose_rec = request.env['user.question.choice'].sudo().search([('user_id','=',request.env.user.id),('question_user','=',str(object_name)),('choice_user','in',prev_choices)])
                                for rec in perv_chose_rec:
                                    rec.user_attempts_count_user -= 1
                            elif (len(record[-2].chosen_choice_ids)) < 2:
                                perv_chose_rec = request.env['user.question.choice'].sudo().search([('user_id','=',request.env.user.id),('question_user','=',str(object_name)),('choice_user','=',(record[-2].chosen_choice_ids.response))])
                                perv_chose_rec.user_attempts_count_user -= 1
                            chose_rec = request.env['user.question.choice'].sudo().search([('user_id','=',request.env.user.id),('question_user','=',str(object_name)),('choice_user','in',chosen_choices)])
                            for rec in chose_rec:
                                rec.user_attempts_count_user += 1
                        if response:
                            if (len(record[-2].chosen_choice_ids)) > 1:
                                for index in record[-2].chosen_choice_ids:
                                    prev_choices.append(index.response)
                                perv_chose_rec = request.env['user.question.choice'].sudo().search([('user_id','=',request.env.user.id),('question_user','=',str(object_name)),('choice_user','in',prev_choices)])
                                for rec in perv_chose_rec:
                                    rec.user_attempts_count_user -= 1
                            elif (len(record[-2].chosen_choice_ids)) < 2:
                                perv_chose_rec = request.env['user.question.choice'].sudo().search([('user_id','=',request.env.user.id),('question_user','=',str(object_name)),('choice_user','=',(record[-2].chosen_choice_ids.response))])
                                perv_chose_rec.user_attempts_count_user -= 1
                            resp_rec = request.env['user.question.choice'].sudo().search([('user_id','=',request.env.user.id),('question_user','=',str(object_name)),('choice_user','=',response)])
                            if resp_rec:
                                resp_rec.user_attempts_count_user += 1
                    #To create record for Tincan Choice Menu
                    request.cr.execute('''SELECT question_user as question, choice_user as choice, SUM(user_attempts_count_user) AS user_attempts_count
                    FROM user_question_choice
                    GROUP BY question_user, choice_user
                    ORDER BY question_user, choice_user''')
                    result =  request.cr.fetchall()
                    if result:
                        record = request.env['question.choice'].sudo().search([])
                        if record:
                            record.unlink()
                        for rec in result:
                            request.env['question.choice'].sudo().create({'question':rec[0],'choice':rec[1],'user_attempts_count':rec[2]})     

                #To create record for users for multiple attempts on question
                user_data = request.env['question.attempt'].sudo().search([('user_id','=',request.env.user.id),('question','=',str(object_name)),('activity_id','=',int(activityId))])
                record = request.env['statement.scorm'].sudo().search([('user_id','=',request.uid),('verb_type','=','answered'),('activityId','=',int(activityId)),('object_name','=',str(object_name))])
                if not user_data :
                    if check_success == True:
                        vals = {
                            'user_id': request.env.user.id,
                            'activity_id': activityId,
                            'question': object_name,
                            'check_success': check_success,
                            'first_attempt_count' : int(1),
                            'second_attempt_count' : int(0),
                            'third_attempt_count' : int(0),
                            'wrong_answer_count' : int(0)
                        }
                    else:
                         vals = {
                            'user_id': request.env.user.id,
                            'activity_id': activityId,
                            'question': object_name,
                            'check_success': check_success,
                            'first_attempt_count' : int(0),
                            'second_attempt_count' : int(0),
                            'third_attempt_count' : int(0),
                            'wrong_answer_count' : int(1)
                        }
                    request.env['question.attempt'].sudo().create(vals)
                if user_data and record:
                    if len(record) == 2 :
                        if record[-1].check_success == True:
                            vals = {
                            'check_success': check_success,
                            'first_attempt_count' : int(0),
                            'second_attempt_count' : int(1),
                            'third_attempt_count' : int(0),
                            'more_attempt_count' : int(0),
                            'wrong_answer_count' : int(0)
                            }
                            user_data.write(vals)
                        elif record[-1].check_success == False:
                            vals = {
                            'check_success': check_success,
                            'first_attempt_count' : int(0),
                            'second_attempt_count' : int(0),
                            'third_attempt_count' : int(0),
                            'more_attempt_count' : int(0),
                            'wrong_answer_count' : int(1)
                            }
                            user_data.write(vals)
                    elif len(record) == 3 :
                        if record[-1].check_success == True:
                            vals = {
                            'check_success': check_success,
                            'first_attempt_count' : int(0),
                            'second_attempt_count' : int(0),
                            'third_attempt_count' : int(1),
                            'more_attempt_count' : int(0),
                            'wrong_answer_count' : int(0)
                            }
                        elif record[-1].check_success == False:
                             vals = {
                            'check_success': check_success,
                            'first_attempt_count' : int(0),
                            'second_attempt_count' : int(0),
                            'third_attempt_count' : int(0),
                            'more_attempt_count' : int(0),
                            'wrong_answer_count' : int(1)
                            }
                        user_data.write(vals)
                    elif len(record) >= 4 :
                        if record[-1].check_success == True:
                            vals = {
                            'check_success': check_success,
                            'first_attempt_count' : int(0),
                            'second_attempt_count' : int(0),
                            'third_attempt_count' : int(0),
                            'more_attempt_count' : int(1),
                            'wrong_answer_count' : int(0)
                            }
                        elif record[-1].check_success == False:
                             vals = {
                            'check_success': check_success,
                            'first_attempt_count' : int(0),
                            'second_attempt_count' : int(0),
                            'third_attempt_count' : int(0),
                            'more_attempt_count' : int(0),
                            'wrong_answer_count' : int(1)
                            }
                        user_data.write(vals)
                    # elif len(record) >= 4 and record[-1].check_success == False:
                    #     vals = {
                    #     'check_success': check_success,
                    #     'first_attempt_count' : int(0),
                    #     'second_attempt_count' : int(0),
                    #     'third_attempt_count' : int(0),
                    #     'more_attempt_count' : int(0),
                    #     'wrong_answer_count' : int(1)
                    #     }
                    #     user_data.write(vals)

                request.cr.execute('''SELECT question as question, SUM(first_attempt_count) AS first_attempt_count,
                SUM(second_attempt_count) AS second_attempt_count,
                SUM(third_attempt_count) AS third_attempt_count,
                SUM(more_attempt_count) AS more_attempt_count,
                SUM(wrong_answer_count) AS wrong_answer_count
                FROM question_attempt
                GROUP BY question
                ORDER BY question''')
                result =  request.cr.fetchall()
                if result:
                    record = request.env['question.attempt.view'].sudo().search([])
                    if record:
                        record.unlink()
                    for rec in result:
                        request.env['question.attempt.view'].sudo().create({'question':rec[0],
                                                                            'first_attempt_count':rec[1],
                                                                            'second_attempt_count':rec[2],
                                                                            'third_attempt_count':rec[3],
                                                                            'more_attempt_count':rec[4],
                                                                            'wrong_answer_count':rec[5]})
            if (verb_type == 'attempted'):
                activityId = data['object'].get('id')
                object_name = data['object']['definition']['name'].get('und')
                interaction_type = data['object'].get('objectType')
                channel_rec = request.env['slide.slide'].sudo().search([('id', '=', int(activityId))], limit=1)
                if channel_rec:
                    vals = ({
                            'name':channel_rec.name,
                            # 'statement_id':activityId,
                            'activityId':activityId,
                            'verb_type': verb_type,
                            'user_name': user_name,
                            'user_email': user_email,
                            'object_name':object_name,
                            'interaction_type':interaction_type,
                            'user_id' : request.env.user.id
                        })
                    request.env['statement.scorm'].sudo().create(vals)

            if (verb_type == 'experienced'):
                activityId = data['object'].get('id').partition('/')[0]
                object_name = data['object']['definition']['name'].get('und')
                interaction_type = data['object'].get('objectType')
                channel_rec = request.env['slide.slide'].sudo().search([('id', '=', int(activityId))], limit=1)
                if channel_rec:
                    vals = ({
                        'name':channel_rec.name,
                        # 'statement_id':activityId,
                        'activityId':activityId,
                        'verb_type': verb_type,
                        'user_name': user_name,
                        'user_email': user_email,
                        'object_name':object_name,
                        'interaction_type':interaction_type,
                        'user_id' : request.env.user.id
                    })
                    request.env['statement.scorm'].sudo().create(vals)

            if (verb_type == 'completed'):
                activityId = data['object'].get('id').partition('/')[0]
            if (verb_type == 'passed'):
                if '/' in data['object']['id']:
                    activityId = data['object'].get('id').partition('/')[0]
                else:
                    activityId = data['object'].get('id')
                object_name = data['object']['definition']['name'].get('und')
                interaction_type = data['object'].get('objectType')
                completion = data['result']['completion'] if 'completion' in data['result'] else ''
                duration = data['result']['duration'] if 'duration' in data['result'] else ''
                check_success = data['result']['success'] if 'success' in ['result'] else ''
                if 'score' in data['result']:
                    scaled_score = float(data['result']['score'].get('scaled')) if 'scaled' in data['result']['score'] else None
                    min_score = int(data['result']['score'].get('min')) if 'min' in data['result']['score'] else None
                    max_score = int(data['result']['score'].get('max')) if 'max' in data['result']['score'] else None
                    score = int(data['result']['score'].get('raw')) if 'raw' in data['result']['score'] else None
                channel_rec = request.env['slide.slide'].sudo().search([('id', '=', int(activityId))], limit=1)
                check_passed = request.env['statement.scorm'].sudo().search([('activityId','=',int(activityId)),('user_id','=',request.env.user.id),('verb_type','=','passed'),('completion','=','True')])
                if not check_passed and channel_rec:
                    vals = ({
                        'name':channel_rec.name,
                        # 'statement_id':activityId,
                        'activityId':activityId,
                        'verb_type': verb_type,
                        'user_name': user_name,
                        'user_email': user_email,
                        'object_name':object_name,
                        'interaction_type':interaction_type,
                        'total_duration':duration,
                        'completion':completion if completion else None,
                        'scaled_score': scaled_score,
                        'min_score':min_score,
                        'max_score':max_score,
                        'score':score,
                        'user_id' : request.env.user.id,
                    })
                    request.env['statement.scorm'].sudo().create(vals)

            if (verb_type == 'failed'):
                if '/' in data['object']['id']:
                    activityId = data['object'].get('id').partition('/')[0]
                else:
                    activityId = data['object'].get('id')
                object_name = data['object']['definition']['name'].get('und')
                interaction_type = data['object'].get('objectType')
                completion = data['result']['completion'] if 'completion' in data['result'] else ''
                duration = data['result']['duration'] if 'duration' in data['result'] else ''
                check_success = data['result']['success'] if 'success' in ['result'] else ''
                if 'score' in data['result']:
                    scaled_score = float(data['result']['score'].get('scaled')) if 'scaled' in data['result']['score'] else None
                    min_score = int(data['result']['score'].get('min')) if 'min' in data['result']['score'] else None
                    max_score = int(data['result']['score'].get('max')) if 'max' in data['result']['score'] else None
                    score = int(data['result']['score'].get('raw')) if 'raw' in data['result']['score'] else None
                channel_rec = request.env['slide.slide'].sudo().search([('id', '=', int(activityId))], limit=1)
                check_failed = request.env['statement.scorm'].sudo().search([('activityId','=',int(activityId)),('user_id','=',request.env.user.id),('verb_type','=','failed'),('completion','=','True')])
                if not check_failed and channel_rec:
                    vals = ({
                        'name':channel_rec.name,
                        # 'statement_id':activityId,
                        'activityId':activityId,
                        'verb_type': verb_type,
                        'user_name': user_name,
                        'user_email': user_email,
                        'object_name':object_name,
                        'interaction_type':interaction_type,
                        'total_duration':duration,
                        'completion':completion if completion else None,
                        'scaled_score': scaled_score,
                        'min_score':min_score,
                        'max_score':max_score,
                        'score':score,
                        'user_id' : request.env.user.id
                    })
                    request.env['statement.scorm'].sudo().create(vals)
        # except(SyntaxError) as e:
        #     return json.dumps(res = {
        #                             "error": str(e)
        #                         })

    