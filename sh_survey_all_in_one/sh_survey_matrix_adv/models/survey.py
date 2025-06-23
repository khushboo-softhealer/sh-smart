# Copyright (C) Softhealer Technologies.

from odoo import models, fields, api, _
import base64
from datetime import datetime
from odoo.exceptions import ValidationError

class survey_question(models.Model):
    _inherit = 'survey.question'

    matrix_subtype = fields.Selection(selection_add=[
        ('sh_custom_matrix', 'Custom Matrix')
    ])


class SurveyLabel(models.Model):
    """ A suggested answer for a question """
    _inherit = 'survey.question.answer'

    sh_value_type = fields.Selection([
        ('textbox', 'Single Line Text Box'),
        ('free_text', 'Multiple Lines Text Box'),
        ('numerical_box', 'Numerical Value'),
        ('date', 'Date'),
        ('datetime', 'Datetime'),
        ('que_sh_color', 'Color'),
        ('que_sh_email', 'E-mail'),
        ('que_sh_url', 'URL'),
        ('que_sh_time', 'Time'),
        ('que_sh_range', 'Range'),
        ('que_sh_week', 'Week'),
        ('que_sh_month', 'Month'),
        ('que_sh_password', 'Password'),
        ('que_sh_file', 'File'),
    ], string='Choices Type')

    ## Matrix Range Config
    sh_matrix_range_min = fields.Integer(string='Minimum')
    sh_matrix_range_max = fields.Integer(string='Maximum')
    sh_matrix_range_step = fields.Integer(string='Step')

class survey_user_input(models.Model):
    _inherit = 'survey.user_input'
    _description = 'Survey User Input for custom matrix'

    def _save_line_matrix(self, question, old_answers, answers, comment):
        vals_list = []

        if answers:
            for row_key, row_answer in answers.items():
                if question.matrix_subtype == 'sh_custom_matrix':
                    answer = row_key.split('_')[1]
                    if answer:
                        for data_value in row_answer:
                            vals = {}
                            if not data_value:
                                data_value = False
                            if question.matrix_subtype == 'sh_custom_matrix':
                                answer_id = self.env['survey.question.answer'].sudo().browse(
                                    int(answer))
                                if answer_id.sh_value_type == 'textbox':
                                    vals = self.sh_get_line_answer_values(
                                        question, answer, data_value, 'text_box')
                                elif answer_id.sh_value_type == 'free_text':
                                    vals = self.sh_get_line_answer_values(
                                        question, answer, data_value, 'char_box')
                                elif answer_id.sh_value_type == 'numerical_box':
                                    vals = self.sh_get_line_answer_values(
                                        question, answer, data_value, 'numerical_box')
                                elif answer_id.sh_value_type == 'date':
                                    vals = self.sh_get_line_answer_values(
                                        question, answer, data_value, 'date')
                                elif answer_id.sh_value_type == 'datetime':
                                    if data_value:
                                        data_value = datetime.strptime(
                                            data_value, '%m/%d/%Y %H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")
                                        vals = self.sh_get_line_answer_values(
                                            question, answer, data_value, 'datetime')
                                elif answer_id.sh_value_type == 'que_sh_color':
                                    vals = self.sh_get_line_answer_values(
                                        question, answer, data_value, 'ans_sh_color')
                                elif answer_id.sh_value_type == 'que_sh_email':
                                    vals = self.sh_get_line_answer_values(
                                        question, answer, data_value, 'ans_sh_email')
                                elif answer_id.sh_value_type == 'que_sh_url':
                                    vals = self.sh_get_line_answer_values(
                                        question, answer, data_value, 'ans_sh_url')
                                elif answer_id.sh_value_type == 'que_sh_time':
                                    vals = self.sh_get_line_answer_values(
                                        question, answer, data_value, 'ans_sh_time')
                                elif answer_id.sh_value_type == 'que_sh_range':
                                    vals = self.sh_get_line_answer_values(
                                        question, answer, data_value, 'ans_sh_range')
                                elif answer_id.sh_value_type == 'que_sh_week':
                                    vals = self.sh_get_line_answer_values(
                                        question, answer, data_value, 'ans_sh_week')
                                elif answer_id.sh_value_type == 'que_sh_month':
                                    vals = self.sh_get_line_answer_values(
                                        question, answer, data_value, 'ans_sh_month')
                                elif answer_id.sh_value_type == 'que_sh_password':
                                    vals = self.sh_get_line_answer_values(
                                        question, answer, data_value, 'ans_sh_password')
                                elif answer_id.sh_value_type == 'que_sh_file':
                                    vals = self.sh_get_line_answer_values(
                                        question, answer, data_value, 'ans_sh_file')
                                vals['matrix_row_id'] = int(
                                    row_key.split('_')[0])
                            else:
                                vals = self.sh_get_line_answer_values(
                                    question, answer, answer, 'suggestion')
                                vals['matrix_row_id'] = int(answer)
                            vals_list.append(vals.copy())

                else:
                    for answer in row_answer:
                        vals = self.sh_get_line_answer_values(
                            question, answer, answer, 'suggestion')
                        vals['matrix_row_id'] = int(row_key)
                        vals_list.append(vals.copy())

        if comment:
            vals_list.append(self._get_line_comment_values(question, comment))

        old_answers.sudo().unlink()
        return self.env['survey.user_input.line'].create(vals_list)

    def sh_get_line_answer_values(self, question, answer, data_value, answer_type):
        vals = {
            'user_input_id': self.id,
            'question_id': question.id,
            'skipped': False,
            'answer_type': answer_type,
        }
        if not answer or (isinstance(answer, str) and not answer.strip()):
            vals.update(answer_type=None, skipped=True)
            return vals

        if answer_type == 'suggestion':
            vals['suggested_answer_id'] = int(answer)
        else:
            vals['value_%s' % answer_type] = data_value
            vals['suggested_answer_id'] = int(answer)
        return vals


class survey_user_input_line(models.Model):
    _inherit = 'survey.user_input.line'
    _description = 'Survey User Input Line for custom matrix'

    @api.constrains('skipped', 'answer_type')
    def _check_answer_type_skipped(self):
        for line in self:
            if (line.skipped == bool(line.answer_type)):
                raise ValidationError(
                    _('A question is either skipped, either answered. Not both.'))
            if line.answer_type == 'suggestion':
                field_name = 'suggested_answer_id'
            elif line.answer_type:
                field_name = 'value_%s' % line.answer_type
            else:  # skipped
                field_name = False
