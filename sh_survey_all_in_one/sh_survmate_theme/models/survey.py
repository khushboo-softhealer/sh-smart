# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, _


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    sh_survmate_theme_grid_type = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
    ], string="Grid", required=True, default='12')

    
    sh_is_rating_question = fields.Boolean(
        string='Is Rating?',
    )
    
class survey_survey(models.Model):
    _inherit = "survey.survey"

    sh_survmate_settings_id = fields.Many2one(
        comodel_name="sh.survmate.settings", string="Survmate Theme")

    # timer position fixed
    sh_is_time_fixed = fields.Boolean(string="Is Fixed Timer Position?")


class sh_survmate_settings(models.Model):
    _name = "sh.survmate.settings"
    _description = 'Survmate Settings'
    _order = "id desc"

    name = fields.Char(string="Name", required=True)
    sh_survmate_show_bg_color = fields.Boolean(string="Show Background Color")
    sh_survmate_bg_color = fields.Char(string="Background Color")
    sh_survmate_question_color = fields.Char(string="Question Color")
    sh_survmate_answer_color = fields.Char(string="Answer Color")
    sh_survmate_section_title_color = fields.Char(
        string="Section Background Color")
    sh_survmate_section_title_font_color = fields.Char(
        string="Section Font Color")
    sh_survmate_section_answer_text_color = fields.Char(
        string="Answer Text Color")

    sh_survmate_theme_primary_color = fields.Char(string="Primary Color")
    sh_survmate_theme_secondary_color = fields.Char(string="Secondary Color")

    sh_survmate_button_style = fields.Selection([
        ('style_1', 'Style 1'),
        ('style_2', 'Style 2'),
        ('style_3', 'Style 3'),
        ('style_4', 'Style 4'),
        ('style_5', 'Style 5'),
    ], string="Button Style")

    sh_survmate_input_style = fields.Selection([
        ('style_1', 'Style 1'),
        ('style_2', 'Style 2'),
        ('style_3', 'Style 3'),
        ('style_4', 'Style 4'),
        ('style_5', 'Style 5'),
    ], string="Input Style")

    sh_survmate_section_style = fields.Selection([
        ('style_1', 'Style 1'),
        ('style_2', 'Style 2'),
        ('style_3', 'Style 3'),
        ('style_4', 'Style 4'),
        ('style_5', 'Style 5'),
    ], string="Section Style")

    sh_survmate_checkbox_style = fields.Selection([
        ('style_1', 'Style 1'),
        ('style_2', 'Style 2'),
        ('style_3', 'Style 3'),
        ('style_4', 'Style 4'),
        ('style_5', 'Style 5'),
    ], string="Checkbox Style")

    sh_survmate_radio_button_style = fields.Selection([
        ('style_1', 'Style 1'),
        ('style_2', 'Style 2'),
        ('style_3', 'Style 3'),
        ('style_4', 'Style 4'),
        ('style_5', 'Style 5'),
    ], string="Radio Button Style")

    def action_preview_theme_style(self):
        if self:

            context = dict(self.env.context or {})
            img_src = ""
            if context and context.get('which_style', '') == 'button':
                img_src = "/sh_survey_all_in_one/static/src/img/extra_addons/sh_survmate_theme/button-style---2.gif"

            if context and context.get('which_style', '') == 'input':
                img_src = "/sh_survey_all_in_one/static/src/img/extra_addons/sh_survmate_theme/input_style.png"

            if context and context.get('which_style', '') == 'section':
                img_src = "/sh_survey_all_in_one/static/src/img/extra_addons/sh_survmate_theme/section_style.png"

            if context and context.get('which_style', '') == 'checkbox':
                img_src = "/sh_survey_all_in_one/static/src/img/extra_addons/sh_survmate_theme/checkbox_style.png"

            if context and context.get('which_style', '') == 'radio':
                img_src = "/sh_survey_all_in_one/static/src/img/extra_addons/sh_survmate_theme/radio_button_style.png"

            context['default_img_src'] = img_src

            return {
                'name': _('Preview Style'),
                'view_mode': 'form',
                'res_model': 'sh.survmate.theme.button.design.wizard',
                'view_id': self.env.ref('sh_survey_all_in_one.sh_survmate_theme_button_style_wizard_view').id,
                'type': 'ir.actions.act_window',
                'context': context,
                'target': 'new',
                'flags': {'form': {'action_buttons': False}}
            }
