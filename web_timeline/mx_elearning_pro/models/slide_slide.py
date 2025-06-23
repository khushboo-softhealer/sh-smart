# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
import urllib.parse
import logging
import re
import requests
from werkzeug import urls
from odoo import models, fields, api
from odoo.exceptions import ValidationError, RedirectWarning, UserError, AccessError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
# from odoo.tools.translate import translate
from odoo import http, _, exceptions
from markupsafe import Markup
from datetime import datetime
from odoo.http import request
from odoo.addons import website_slides
from odoo.addons.http_routing.models.ir_http import slug

_logger = logging.getLogger(__name__)

class SlideTincan(models.Model):
    _inherit = 'slide.slide'

    min_duration = fields.Float('Min. Duration',digits=(10, 4), help="The minimum estimated completion time for this slide")
    is_tincan = fields.Boolean(string="Is Tincan")
    tincan_xp = fields.Boolean("Calculate Xp based on score")
    check_timer_complete = fields.Boolean(string="Check Timer Complete",default=False)
    state_scorm_ids = fields.One2many('state.scorm','state_id',"Scorm State Data")
    statement_scorm_ids = fields.One2many('statement.scorm','statement_id',"Scorm Statement Data")
    sequence = fields.Integer("Sequence")
    completed_user_count = fields.Integer("Completed", store=True, compute='_compute_completions_count')
    completion_duration = fields.Char("Completion Time", store=True) #To store average duration for same slides completed by multiple users 
    embed_code = fields.Html(compute='_compute_embed_code', store=True,compute_sudo=True)
    
    def get_scorm_finish(self):
        if self._fields.get('scorm_completion_on_finish'):
            return self.scorm_completion_on_finish
        return False


    def action_publish(self):
        if not self.id:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'type': 'warning',
                    'message': _("Please save the course to publish it.")
                }
            }
        else:
            self.is_published = True

    def action_unpublish(self):
        self.is_published = False


    def action_mark_completed(self):
        for slide in self:
            if slide.slide_type == 'scorm' and slide.is_tincan and slide.channel_id.is_member:
                datas = self.env['statement.scorm'].sudo()
                scorm_datas = datas.search([('activityId', '=', int(slide.id)),('user_id','=',request.env.user.id)])
                state_rec =  self.env['state.scorm'].sudo().search([('activityId', '=', int(slide.id)),('user_id','=',request.env.user.id)])
                if any(rec.verb_type in ['passed','failed'] and rec.completion for rec in scorm_datas):
                    completion_time = (datetime.strptime("0:00:00", "%H:%M:%S")-datetime.strptime("0:00:00", "%H:%M:%S")).total_seconds()
                    for index in range(0,len(state_rec)-1):
                        if (state_rec[index].request_type == state_rec[index+1].request_type == 'PUT'):
                            if (state_rec[index+1].write_date.date() == state_rec[index].write_date.date()):
                                completion_time += (datetime.strptime(state_rec[index+1].write_date.strftime("%H:%M:%S"), "%H:%M:%S") - datetime.strptime(state_rec[index].write_date.strftime("%H:%M:%S"), "%H:%M:%S")).total_seconds()
                            else:
                                dur1 = (datetime.strptime("23:59:59", "%H:%M:%S") - datetime.strptime(state_rec[index].write_date.strftime("%H:%M:%S"), "%H:%M:%S")).total_seconds()
                                dur2 = (datetime.strptime(state_rec[index+1].write_date.strftime("%H:%M:%S"), "%H:%M:%S")- datetime.strptime("0:00:00", "%H:%M:%S")).total_seconds()
                                completion_time += dur1 + dur2
                        elif (state_rec[index].request_type == 'GET' and state_rec[index+1].request_type == 'PUT'):
                            if (state_rec[index+1].write_date.date() == state_rec[index].write_date.date()):
                                completion_time += (datetime.strptime(state_rec[index+1].write_date.strftime("%H:%M:%S"), "%H:%M:%S") - datetime.strptime(state_rec[index].write_date.strftime("%H:%M:%S"), "%H:%M:%S")).total_seconds()
                            else:
                                dur1 = (datetime.strptime("23:59:59", "%H:%M:%S") - datetime.strptime(state_rec[index].write_date.strftime("%H:%M:%S"), "%H:%M:%S")).total_seconds()
                                dur2 = (datetime.strptime(state_rec[index+1].write_date.strftime("%H:%M:%S"), "%H:%M:%S")- datetime.strptime("0:00:00", "%H:%M:%S")).total_seconds()
                                completion_time += dur1 + dur2
                        else:
                            index = index + 1
                    record = datas.search([('completion','=','True'),('activityId', '=', int(slide.id)),('user_id','=',request.env.user.id)])
                    record.calculated_duration =  completion_time
                if scorm_datas:
                    if any('passed' in rec.verb_type for rec in scorm_datas):
                        slide._action_mark_completed()
                    for rec in scorm_datas:
                        if rec.completion == 'True' and rec.verb_type == 'passed':
                            slide_partner_sudo = request.env['slide.slide.partner'].sudo()
                            slide_partner_id = slide_partner_sudo.search([('slide_id', '=', slide.id),('partner_id', '=', request.env.user.partner_id.id)], limit=1)
                            if slide_partner_id:
                                user_sudo = request.env['res.users'].sudo()
                                user_id = user_sudo.search([('partner_id', '=', slide_partner_id.partner_id.id)], limit=1)
                                if slide.tincan_xp:
                                    score = datas.search([('completion','=','True'),('activityId', '=', int(slide.id)),('user_id','=',request.env.user.id)])
                                    user_id.karma += int(score.scaled_score)*100
                                else:
                                    if slide.scorm_passed_xp:
                                        user_id.karma += slide.scorm_passed_xp
                    if any('failed' in rec.verb_type for rec in scorm_datas):
                        slide._action_mark_completed()
                    else:
                        return {'error': 'scorm_incomplete'}
                else:
                    return request.redirect('/slides/slide/%s' % slug(slide))
            else:
                res = super(SlideTincan, self).action_mark_completed()
                return res

    @api.depends('slide_partner_ids.slide_id', 'slide_partner_ids.completed')
    def _compute_completions_count(self):
        read_group_res = self.env['slide.slide.partner'].read_group(
            [('completed','=',True)],
            ['slide_id'], groupby=['slide_id'])
        mapped_data = dict((rec['slide_id'][0], rec['slide_id_count']) for rec in read_group_res)
        for slide in self:
            slide.completed_user_count = mapped_data.get(slide.id, 0)
        for slide in self: 
            if slide.slide_category == 'scorm' and slide.is_tincan:
                duration = 0
                duration_rec = self.env['statement.scorm'].sudo().search([('completion','=','True'),('activityId','=',slide.id)])
                for rec in duration_rec:
                    duration += rec.calculated_duration
                    if duration != 0 and slide.completed_user_count >= 1:
                        seconds = (duration/slide.completed_user_count) % (24 * 3600)
                        hour = seconds // 3600
                        seconds %= 3600
                        minutes = seconds // 60
                        seconds %= 60
                        slide.completion_duration = "%02d:%02d:%02d" % (hour, minutes, seconds)
                    elif duration == 0 and slide.completed_user_count >= 1:
                        slide.completion_duration = '00:00:01'
                    else:
                        slide.completion_duration = ''
                        # slide.completion_duration = timedelta(seconds=(duration/slide.completed_user_count))
            else:
                record = self.env['slide.slide.partner'].sudo().search([('completed','=',True),('slide_id','=',slide.id)])
                duration = 0
                for rec in record:
                    duration += (datetime.strptime(rec.write_date.strftime("%H:%M:%S"), "%H:%M:%S") - datetime.strptime(rec.create_date.strftime("%H:%M:%S"), "%H:%M:%S")).total_seconds()
                    if duration != 0 and slide.completed_user_count >= 1:
                        seconds = (duration/slide.completed_user_count) % (24 * 3600)
                        hour = seconds // 3600
                        seconds %= 3600
                        minutes = seconds // 60
                        seconds %= 60
                        slide.completion_duration = "%02d:%02d:%02d" % (hour, minutes, seconds)
                    elif duration == 0 and slide.completed_user_count >= 1:
                        slide.completion_duration = '00:00:01'
                    else:
                        slide.completion_duration = ''

    @api.depends('slide_category', 'google_drive_id', 'video_source_type', 'youtube_id')
    def _compute_embed_code(self):
        try:
            for rec in self:
                if rec.slide_category == 'scorm' and rec.scorm_data and not rec.is_tincan:
                    rec.embed_code = Markup('<iframe src="%s" allowFullScreen="true" frameborder="0"></iframe>') % (rec.filename)
                    rec.embed_code_external = Markup('<iframe src="%s" allowFullScreen="true" frameborder="0"></iframe>') % (rec.filename)
                elif rec.slide_category == 'scorm' and rec.scorm_data and rec.is_tincan:
                    user_name = self.env.user.name
                    user_mail = self.env.user.login
                    end_point = self.env['ir.config_parameter'].get_param('web.base.url') + '/slides/slide'
                    end_point = urllib.parse.quote(end_point, safe=" ")
                    actor = "{'name': [%s], mbox: ['mailto':%s]}" % (user_name,user_mail)
                    actor = json.dumps(actor)
                    actor = urllib.parse.quote(actor)
                    rec.embed_code = Markup('<iframe src="%s?endpoint=%s&actor=%s&activity_id=%s" allowFullScreen="true" frameborder="0"></iframe>') % (rec.filename,end_point,actor,rec.id)
                    rec.embed_code_external = Markup('<iframe src="%s?endpoint=%s&actor=%s&activity_id=%s" allowFullScreen="true" frameborder="0"></iframe>') % (rec.filename,end_point,actor,rec.id)
                else:
                    res = super(SlideTincan, rec)._compute_embed_code()
                    return res
        except:
            for rec in self:
                if rec.slide_category  == 'scorm' and rec.scorm_data:
                    rec.embed_code = Markup('<iframe src="%s" allowFullScreen="true" frameborder="0"></iframe>') % (rec.filename)
                    rec.embed_code_external = Markup('<iframe src="%s" allowFullScreen="true" frameborder="0"></iframe>') % (rec.filename)
                else:
                    res = super(SlideTincan, rec)._compute_embed_code()
                    return res


class StateScorm(models.Model):
    _name = 'state.scorm'

    state = fields.Char("State")
    user_id = fields.Integer("User ID")
    state_id = fields.Many2one('slide.slide', ondelete = "cascade")
    activityId = fields.Char("Activity ID")
    agent_name = fields.Char("User Name")
    agent_email = fields.Char("User Email")
    request_payload = fields.Char("Request Payload")
    request_type = fields.Char("Request Type")
    object_type = fields.Char("Object Type")


class StatementScorm(models.Model):
    _name = 'statement.scorm'

    name = fields.Char("Name")
    statement_id = fields.Many2one('slide.slide', ondelete = "cascade")
    activityId = fields.Char("Scorm ID")
    user_name = fields.Char("User Name")
    user_email = fields.Char("User Email")
    verb_type = fields.Char("Verb")
    object_name = fields.Char("Object Name")
    interaction_type = fields.Char("Interaction Type")
    check_success = fields.Boolean("Success")
    score = fields.Integer("Score")
    chosen_choice_ids = fields.One2many('response.choice','chosen_option_id')
    correct_option_pattern_ids = fields.One2many('option.pattern','correct_option_id')
    options_ids = fields.One2many('assesment.option','assesment_option_id',"Options")
    completion = fields.Char("Completion")
    min_score = fields.Integer("Min Score")
    max_score = fields.Integer("Max Score")
    scaled_score = fields.Float("Scaled Score")
    total_duration = fields.Char("Completion Time")
    user_id = fields.Integer("User ID")
    calculated_duration = fields.Float("Duration") #To store duration taken by an user to complete the single slide
    error_scorm = fields.Char("Error Scorm")

class chosenOptions(models.Model):
    _name = 'response.choice'

    response = fields.Char("Chosen Choice")
    chosen_option_id = fields.Many2one('statement.scorm', ondelete = "cascade")

class correctOptionPatterns(models.Model):
    _name = 'option.pattern'

    name = fields.Char("Correct Response")
    correct_option_pattern = fields.Char("Correct Option Pattern")
    correct_option_id = fields.Many2one('statement.scorm', ondelete = "cascade")


class ScormAssesOptions(models.Model):
    _name = 'assesment.option'

    name = fields.Char("Option Name")
    assesment_option_id = fields.Many2one('statement.scorm', ondelete = "cascade")

class UserTincanResponse(models.Model):
    _name = "user.tincan.response"

    channel_name = fields.Char("Course")
    activityId = fields.Integer("Scorm ID")
    user_id = fields.Integer("User ID")
    user_name = fields.Char('User Name')
    content_name = fields.Text("Content")
    question_name = fields.Text("Question Name")
    response_type = fields.Text("Response Type")
    chosen_choice =  fields.Char("Response")
    option = fields.Char("Options")
    marks_allotted = fields.Integer("Points")
    attempts_count = fields.Integer("Attempts Count", default=1)
    check_answer = fields.Char("Result")
    update_date = fields.Datetime("Create Date")

class QuestionChoice(models.Model):
    _name = "question.choice"

    question = fields.Text("Question Name")
    choice =  fields.Char("Option")
    user_attempts_count = fields.Integer("Attempts Count", default=0)

class AttemptQuestion(models.Model):
    _name = "question.attempt"

    question = fields.Text("Question Name")
    user_id = fields.Integer("User ID")
    activity_id = fields.Integer("Slide ID")
    check_success = fields.Boolean("Result")
    first_attempt_count =  fields.Integer("First Attempt", default=0)
    second_attempt_count = fields.Integer("Second Attempt", default=0)
    third_attempt_count = fields.Integer("Third Attempt", default=0)
    more_attempt_count = fields.Integer("More than 3 Attempts", default=0)
    wrong_answer_count = fields.Integer("Wrong Answer", default=0)

class AttemptQuestionView(models.Model):
    _name = "question.attempt.view"

    question = fields.Text("Question Name")
    first_attempt_count =  fields.Integer("First Attempt", default=0)
    second_attempt_count = fields.Integer("Second Attempt", default=0)
    third_attempt_count = fields.Integer("Third Attempt", default=0)
    more_attempt_count = fields.Integer("More than 3 Attempts", default=0)
    wrong_answer_count = fields.Integer("Wrong Answer", default=0)


class UserQuestionChoice(models.Model):
    _name = "user.question.choice"

    question_user = fields.Text("Question Name")
    user_id = fields.Integer("User ID")
    activity_id = fields.Integer("Activity ID")
    choice_user =  fields.Char("Option")
    user_attempts_count_user = fields.Integer("Attempts Count", default=0)


class Channel(models.Model):
    _inherit = 'slide.channel'

    mx_slide_channel_ids = fields.One2many('slide.channel.depend', 'mx_channel_id')
    channel_type = fields.Selection(selection_add=[
        ('learning_path', 'Learning Path')
    ], ondelete={'learning_path': 'cascade'})
    channel_ids = fields.Many2many('slide.channel', 'channel_slide_channel_rel', 'channel_id', 'path_id')
    learning_path_ids = fields.Many2many('slide.channel', 'learning_path_channel_rel', 'path_id', 'channel_id',
        compute='_get_learning_paths')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    description_short = fields.Html('Short Description', help="The description that is displayed on the course card")
    description = fields.Html('Description', help="The description that is displayed on top of the course page, just below the title")
    enrollment_start_date = fields.Date('Enrollment Start Date')
    enrollment_end_date = fields.Date('Enrollment End Date')
    is_timer = fields.Boolean('Timer')
    is_sequential = fields.Boolean('Sequential')

    YOUTUBE_VIDEO_ID_REGEX_PRO = r'^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*'
    GOOGLE_DRIVE_DOCUMENT_ID_REGEX_PRO = r'(^https:\/\/docs.google.com|^https:\/\/drive.google.com).*\/d\/([^\/]*)'
    VIMEO_VIDEO_ID_REGEX_PRO = r'\/\/(player.)?vimeo.com\/(?:[a-z]*\/)*([0-9]{6,11})\/?([0-9a-z]{6,11})?[?]?.*'
    intro_video_type = fields.Selection([
        ('youtube_video', 'YouTube Video'),
        ('google_drive_video', 'Google Drive Video'),
        ('vimeo_video', 'Vimeo Video')],
        string="Slide Type", compute='_compute_intro_video_type', store=True, readonly=False,
        help="Subtype of the video category, allows more precision on the actual file type / source type.")
    intro_url = fields.Char('External URL', help="URL of the Google Drive file or URL of the YouTube video")
    intro_video_url = fields.Char('Introduction Video Link', related='intro_url', readonly=False,
        help="Link of the video (we support YouTube, Google Drive and Vimeo as sources)")
    intro_video_source_type = fields.Selection([
        ('youtube', 'YouTube'),
        ('google_drive', 'Google Drive'),
        ('vimeo', 'Vimeo')],
        string='Video Source', compute="_compute_intro_video_source_type")
    video_image_1920 = fields.Image(store=True, readonly=False)
    intro_youtube_id = fields.Char('Video YouTube ID', compute='_compute_intro_youtube_id')
    intro_vimeo_id = fields.Char('Video Vimeo ID', compute='_compute_intro_vimeo_id')
    intro_google_drive_id = fields.Char('Google Drive ID of the external URL', compute='_compute_intro_google_drive_id')
    video_embed_code = fields.Html('Embed Code', readonly=True, compute='_compute_video_embed_code', sanitize=False)
    
    @api.depends('intro_video_url', 'intro_google_drive_id', 'intro_video_source_type', 'intro_youtube_id')
    def _compute_video_embed_code(self):
        for course in self:
            video_embed_code = False
            # embed_code_external = False
            if course.intro_video_url :
                if course.intro_video_source_type == 'youtube':
                    query_params = urls.url_parse(course.intro_video_url).query
                    query_params = query_params + '&theme=light' if query_params else 'theme=light'
                    video_embed_code = Markup('<iframe src="//www.youtube-nocookie.com/embed/%s?%s" allowFullScreen="true" frameborder="0" style="height:-webkit-fill-available; width:-webkit-fill-available;"></iframe>') % (course.intro_youtube_id, query_params)
                elif course.intro_video_source_type == 'google_drive':
                    video_embed_code = Markup('<iframe src="//drive.google.com/file/d/%s/preview" allowFullScreen="true" frameborder="0" style="height:-webkit-fill-available; width:-webkit-fill-available;"></iframe>') % (course.intro_google_drive_id)
                elif course.intro_video_source_type == 'vimeo':
                    if '/' in course.intro_vimeo_id:
                        # in case of privacy 'with URL only', vimeo adds a token after the video ID
                        # the embed url needs to receive that token as a "h" parameter
                        [vimeo_id, vimeo_token] = course.intro_vimeo_id.split('/')
                        video_embed_code = Markup("""
                            <iframe src="https://player.vimeo.com/video/%s?h=%s&badge=0&amp;autopause=0&amp;player_id=0"
                                frameborder="0" style="height:-webkit-fill-available; width:-webkit-fill-available;" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe>""") % (
                                vimeo_id, vimeo_token)
                    else:
                        video_embed_code = Markup("""
                            <iframe src="https://player.vimeo.com/video/%s?badge=0&amp;autopause=0&amp;player_id=0"
                                frameborder="0" style="height:-webkit-fill-available; width:-webkit-fill-available;" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe>""") % (course.intro_vimeo_id)
            course.video_embed_code = video_embed_code

    
    @api.depends('intro_video_type', 'intro_video_source_type')
    def _compute_intro_video_type(self):
        """ For 'local content' or specific slide categories, the slide type is directly derived
        from the slide category.

        For external content, the slide type is determined from the metadata and the mime_type.
        (See #_fetch_google_drive_metadata() for more details)."""
        for course in self:
            if course.intro_video_url and course.intro_video_source_type == 'youtube':
                course.intro_video_type = 'youtube_video'
            elif course.intro_video_url and course.intro_video_source_type == 'google_drive':
                course.intro_video_type = 'google_drive_video'
            elif course.intro_video_url and course.intro_video_source_type == 'vimeo':
                course.intro_video_type = 'vimeo_video'
            else:
                course.intro_video_type = False
    
    @api.depends('intro_video_url')
    def _compute_intro_video_source_type(self):
        for course in self:
            intro_video_source_type = False
            youtube_match = re.match(self.YOUTUBE_VIDEO_ID_REGEX_PRO, course.intro_video_url) if course.intro_video_url else False
            if youtube_match and len(youtube_match.groups()) == 2 and len(youtube_match.group(2)) == 11:
                intro_video_source_type = 'youtube'
            if course.intro_video_url and not intro_video_source_type and re.match(self.GOOGLE_DRIVE_DOCUMENT_ID_REGEX_PRO, course.intro_video_url):
                intro_video_source_type = 'google_drive'
            vimeo_match = re.search(self.VIMEO_VIDEO_ID_REGEX_PRO, course.intro_video_url) if course.intro_video_url else False
            if not intro_video_source_type and vimeo_match and len(vimeo_match.groups()) == 3:
                intro_video_source_type = 'vimeo'

            course.intro_video_source_type = intro_video_source_type

    @api.depends('intro_video_url', 'intro_video_source_type')
    def _compute_intro_youtube_id(self):
        for course in self: 
            if course.intro_video_url and course.intro_video_source_type == 'youtube':
                match = re.match(self.YOUTUBE_VIDEO_ID_REGEX_PRO, course.intro_video_url)
                if match and len(match.groups()) == 2 and len(match.group(2)) == 11:
                    course.intro_youtube_id = match.group(2)
                else:
                    course.intro_youtube_id = False
            else:
                course.intro_youtube_id = False

    @api.depends('intro_video_url', 'intro_video_source_type')
    def _compute_intro_vimeo_id(self):
        for course in self:
            if course.intro_video_url and course.intro_video_source_type == 'vimeo':
                match = re.search(self.VIMEO_VIDEO_ID_REGEX_PRO, course.intro_video_url)
                if match and len(match.groups()) == 3:
                    if match.group(3):
                        # in case of privacy 'with URL only', vimeo adds a token after the video ID
                        # the share url is then 'vimeo_id/token'
                        # the token will be captured in the third group of the regex (if any)
                        course.intro_vimeo_id = '%s/%s' % (match.group(2), match.group(3))
                    else:
                        # regular video, we just capture the vimeo_id
                        course.intro_vimeo_id = match.group(2)
            else:
                course.intro_vimeo_id = False

    @api.depends('intro_video_url')
    def _compute_intro_google_drive_id(self):
        """ Extracts the Google Drive ID from the url based on the slide category. """
        for course in self:
            url = course.intro_video_url
            intro_google_drive_id = False
            if url:
                match = re.match(self.GOOGLE_DRIVE_DOCUMENT_ID_REGEX_PRO, url)
                if match and len(match.groups()) == 2:
                    intro_google_drive_id = match.group(2)

            course.intro_google_drive_id = intro_google_drive_id

    @api.onchange('start_date')
    def onchange_start_date(self):
        if self.end_date:
            if datetime.strptime(str(self.start_date), DEFAULT_SERVER_DATE_FORMAT).date() > self.end_date:
                raise ValidationError("Please select a date smaller than the End date!")
            else:
                pass
        else:
            pass

    @api.onchange('enrollment_end_date')
    def onchange_enrollment_end_date(self):
        if self.end_date:
            if datetime.strptime(str(self.enrollment_end_date), DEFAULT_SERVER_DATE_FORMAT).date() > self.end_date:
                raise ValidationError("Please select Enrollment end date smaller than the End date!")
            else:
                pass
        if self.enrollment_start_date:
            if datetime.strptime(str(self.enrollment_end_date), DEFAULT_SERVER_DATE_FORMAT).date() < self.enrollment_start_date:
                raise ValidationError("Please select Enrollment end date greater than the Enrollment start date!")
            else:
                pass
    @api.onchange('enrollment_start_date')
    def onchange_enrollment_start_date(self):
        if self.end_date:
            if datetime.strptime(str(self.enrollment_start_date), DEFAULT_SERVER_DATE_FORMAT).date() > self.end_date:
                raise ValidationError("Please select Enrollment start date smaller than the End date!")
            else:
                pass
        else:
            pass

    @api.onchange('end_date')
    def onchange_end_date(self):
        if self.start_date:
            if datetime.strptime(str(self.end_date), DEFAULT_SERVER_DATE_FORMAT).date() <= datetime.strptime(str(self.start_date), DEFAULT_SERVER_DATE_FORMAT).date():
                raise ValidationError("Please select a date greater than the start date!")
            if self.end_date < datetime.now().date():
                self.is_published = False
            else:
                self.is_published = True
                
    def _get_learning_paths(self):
        for rec in self:
            learning_path_ids = self.search([('channel_ids', 'in', rec.id)])
            rec.learning_path_ids = [(6, 0, learning_path_ids.ids)]

    @api.depends('slide_partner_ids', 'slide_partner_ids.completed', 'total_slides')
    @api.depends_context('uid')
    def _compute_user_statistics(self):
        current_user_info = self.env['slide.channel.partner'].sudo().search(
            [('channel_id', 'in', self.ids), ('partner_id', '=', self.env.user.partner_id.id)]
        )
        mapped_data = dict((info.channel_id.id, (info.completed, info.completed_slides_count)) for info in current_user_info)
        for record in self:
            completed, completed_slides_count = mapped_data.get(record.id, (False, 0))
            record.completed = completed
            record.completion = 100.0 if completed else round(100.0 * completed_slides_count / (record.total_slides or 1))
            if record.channel_type == 'learning_path':
                completion = 0
                for channel in record.channel_ids:
                    completion += channel.completion
                record.completion = completion / len(record.channel_ids.ids)

    @api.depends('slide_ids.slide_category', 'slide_ids.is_published', 'slide_ids.completion_time',
                 'slide_ids.likes', 'slide_ids.dislikes', 'slide_ids.total_views', 'slide_ids.is_category', 'slide_ids.active')
    def _compute_slides_statistics(self):
        default_vals = dict(total_views=0, total_votes=0, total_time=0, total_slides=0)
        keys = ['nbr_%s' % slide_category for slide_category in self.env['slide.slide']._fields['slide_category'].get_values(self.env)]
        default_vals.update(dict((key, 0) for key in keys))

        result = dict((cid, dict(default_vals)) for cid in self.ids)
        read_group_res = self.env['slide.slide']._read_group(
            [('active', '=', True), ('is_published', '=', True), ('channel_id', 'in', self.ids), ('is_category', '=', False)],
            ['channel_id', 'slide_category', 'likes', 'dislikes', 'total_views', 'completion_time'],
            groupby=['channel_id', 'slide_category'],
            lazy=False)
        for res_group in read_group_res:
            cid = res_group['channel_id'][0]
            result[cid]['total_views'] += res_group.get('total_views', 0)
            result[cid]['total_votes'] += res_group.get('likes', 0)
            result[cid]['total_votes'] -= res_group.get('dislikes', 0)
            result[cid]['total_time'] += res_group.get('completion_time', 0)

        type_stats = self._compute_slides_statistics_category(read_group_res)
        for cid, cdata in type_stats.items():
            result[cid].update(cdata)

        for record in self:
            record.update(result.get(record.id, default_vals))
            if record.channel_type == 'learning_path':
                total_time = 0
                for course in record.channel_ids:
                    total_time += course.total_time
                record.total_time = total_time


class SlideChannelDepend(models.Model):
    _name = 'slide.channel.depend'

    mx_channel_id = fields.Many2one('slide.channel', 'Course', required=1)
    mx_course_id = fields.Many2one('slide.channel', 'Dependent Course', required=1)
    mx_completion_percent = fields.Integer(default=100, required=1)

class ChannelUsersRelation(models.Model):
    _inherit = 'slide.channel.partner'

    mx_resume_slide_id = fields.Many2one('slide.slide', 'Resume Slide')