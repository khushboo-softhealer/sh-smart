# Copyright (C) Softhealer Technologies.

from datetime import datetime, timedelta
from odoo import api, fields, models


class SurveyLabel(models.Model):
    """ A suggested answer for a question """
    _inherit = 'survey.question.answer'

    sh_value_type = fields.Selection(selection_add=[
        ('que_sh_qrcode', 'QR Code'),
        ('que_sh_barcode', 'Barcode'),
    ])


class survey_question(models.Model):
    _inherit = 'survey.question'
    _description = 'Inherit Survey Question for extra fields'

    question_type = fields.Selection(selection_add=[
        ('que_sh_qrcode', 'QR Code'),
        ('que_sh_barcode', 'Barcode'),
        ('que_sh_location', 'Location')
    ])

    # ------------------------------------------------------------
    # VALIDATION
    # ------------------------------------------------------------

    def validate_question(self, answer, comment=None):
        """ Validate question, depending on question type and parameters
         for simple choice, text, date and number, answer is simply the answer of the question.
         For other multiple choices questions, answer is a list of answers (the selected choices
         or a list of selected answers per question -for matrix type-):
            - Simple answer : answer = 'example' or 2 or question_answer_id or 2019/10/10
            - Multiple choice : answer = [question_answer_id1, question_answer_id2, question_answer_id3]
            - Matrix: answer = { 'rowId1' : [colId1, colId2,...], 'rowId2' : [colId1, colId3, ...] }

         return dict {question.id (int): error (str)} -> empty dict if no validation error.
         """
        self.ensure_one()
        if isinstance(answer, str):
            answer = answer.strip()
        # Empty answer to mandatory question
        if self.constr_mandatory and not answer and self.question_type not in ['simple_choice', 'multiple_choice']:
            return {self.id: self.constr_error_msg}

        # because in choices question types, comment can count as answer
        if answer or self.question_type in ['simple_choice', 'multiple_choice']:
            if self.question_type == 'char_box':
                return self._validate_char_box(answer)
            elif self.question_type == 'numerical_box':
                return self._validate_numerical_box(answer)
            elif self.question_type in ['date', 'datetime']:
                return self._validate_date(answer)
            elif self.question_type in ['simple_choice', 'multiple_choice']:
                return self._validate_choice(answer, comment)
            elif self.question_type == 'matrix':
                return self._validate_matrix(answer)
            elif self.question_type == 'que_sh_color':
                return self.validate_que_sh_color(answer)
            elif self.question_type == 'que_sh_email':
                return self.validate_que_sh_email(answer)
            elif self.question_type == 'que_sh_url':
                return self.validate_que_sh_url(answer)
            elif self.question_type == 'que_sh_time':
                return self.validate_que_sh_time(answer)
            elif self.question_type == 'que_sh_range':
                return self.validate_que_sh_range(answer)
            elif self.question_type == 'que_sh_week':
                return self.validate_que_sh_week(answer)
            elif self.question_type == 'que_sh_month':
                return self.validate_que_sh_month(answer)
            elif self.question_type == 'que_sh_password':
                return self.validate_que_sh_password(answer)
            elif self.question_type == 'que_sh_file':
                return self.validate_que_sh_file(answer)
            elif self.question_type == 'que_sh_signature':
                return self.validate_que_sh_signature(answer)
            elif self.question_type == 'que_sh_many2one':
                return self.validate_que_sh_many2one(answer)
            elif self.question_type == 'que_sh_many2many':
                return self.validate_que_sh_many2many(answer)
            elif self.question_type == 'que_sh_address':
                return self.validate_que_sh_address(answer)            
            elif self.question_type == 'que_sh_qrcode':
                return self.validate_que_sh_qrcode(answer)
            elif self.question_type == 'que_sh_barcode':
                return self.validate_que_sh_barcode(answer)
            elif self.question_type == 'que_sh_location':
                return self.validate_que_sh_location(answer)

        return {}

    # ====================================================================
    #for QR field.
    # ====================================================================

    def validate_que_sh_qrcode(self, answer):
        if self.constr_mandatory and not answer:
            return {self.id: self.constr_error_msg}
        return {}

    # ====================================================================
    #for BARCODE field.
    # ====================================================================

    def validate_que_sh_barcode(self, answer):
        if self.constr_mandatory and not answer:
            return {self.id: self.constr_error_msg}
        return {}
    # ====================================================================
    #for Location field.
    # ====================================================================

    def validate_que_sh_location(self, answer):
        if self.constr_mandatory and not answer:
            return {self.id: self.constr_error_msg}
        return {}


    def _validate_matrix(self, answers):
        # Validate that each line has been answered
        if self.constr_mandatory:
            for row in answers:
                if answers[row] == ['']:
                    return {self.id: self.constr_error_msg}
        return {}
    
class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    def _save_line_matrix(self, question, old_answers, answers, comment):
        vals_list = []
        if answers:
            for row_key, row_answer in answers.items():
                if question.matrix_subtype == 'sh_custom_matrix':
                    answer = row_key.split('_')[1]
                    if answer:
                        for data_value in row_answer:
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
                                    if data_value  in ['',"",False,None]:
                                        data_value = False
                                    else:
                                        data_value = datetime.strptime(
                                        data_value, '%m/%d/%Y %H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")
                                    # data_value = datetime.strptime(
                                    # data_value, '%m/%d/%Y %H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")
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
                                elif answer_id.sh_value_type == 'que_sh_qrcode':
                                    
                                    vals = self.sh_get_line_answer_values(
                                    question, answer, data_value, 'ans_sh_qrcode')
                                elif answer_id.sh_value_type == 'que_sh_barcode':
                                    vals = self.sh_get_line_answer_values(
                                    question, answer, data_value, 'ans_sh_barcode')
                                elif answer_id.sh_value_type == 'que_sh_location':
                                    
                                    vals = self.sh_get_line_answer_values(
                                    question, answer, data_value, 'ans_sh_location')
                                vals['matrix_row_id'] = int(
                                row_key.split('_')[0])
                                
                            else:
                                vals = self.sh_get_line_answer_values(
                                question, answer, answer, 'suggestion')
                                vals['matrix_row_id'] = int(answer)
                            vals_list.append(vals.copy())

                else:
                    for answer in row_answer:
                        vals = self.sh_get_line_answer_values(question, answer, answer, 'suggestion')
                        vals['matrix_row_id'] = int(row_key)
                        vals_list.append(vals.copy())

        if comment:
            vals_list.append(self._get_line_comment_values(question, comment))

        old_answers.sudo().unlink()
        return self.env['survey.user_input.line'].create(vals_list)

    def save_lines(self, question, answer, comment=None):
        """ Save answers to questions, depending on question type

            If an answer already exists for question and user_input_id, it will be
            overwritten (or deleted for 'choice' questions) (in order to maintain data consistency).
        """
        old_answers = self.env['survey.user_input.line'].search([
            ('user_input_id', '=', self.id),
            ('question_id', '=', question.id)
        ])
        if question.question_type in ['char_box', 'text_box', 'numerical_box', 'date', 'datetime']:
            self._save_line_simple_answer(question, old_answers, answer)
            if question.save_as_email and answer:
                self.write({'email': answer})
            if question.save_as_nickname and answer:
                self.write({'nickname': answer})
        
        elif question.question_type in ['simple_choice', 'multiple_choice']:
            self._save_line_choice(question, old_answers, answer, comment)
        elif question.question_type == 'matrix':
            self._save_line_matrix(question, old_answers, answer, comment)
        elif question.question_type in ['que_sh_color']:
            self.save_line_que_sh_field(
                question, old_answers, answer, 'ans_sh_color')
        elif question.question_type in ['que_sh_email']:
            self.save_line_que_sh_field(
                question, old_answers, answer, 'ans_sh_email')
        elif question.question_type in ['que_sh_url']:
            self.save_line_que_sh_field(
                question, old_answers, answer, 'ans_sh_url')
        elif question.question_type in ['que_sh_time']:
            self.save_line_que_sh_field(
                question, old_answers, answer, 'ans_sh_time')
        elif question.question_type in ['que_sh_range']:
            self.save_line_que_sh_field(
                question, old_answers, answer, 'ans_sh_range')
        elif question.question_type in ['que_sh_week']:
            self.save_line_que_sh_field(
                question, old_answers, answer, 'ans_sh_week')
        elif question.question_type in ['que_sh_month']:
            self.save_line_que_sh_field(
                question, old_answers, answer, 'ans_sh_month')
        elif question.question_type in ['que_sh_password']:
            self.save_line_que_sh_field(
                question, old_answers, answer, 'ans_sh_password')
        elif question.question_type in ['que_sh_file']:
            self.save_line_que_sh_file(
                question, old_answers, answer, 'ans_sh_file')
        elif question.question_type in ['que_sh_signature']:
            self.save_line_que_sh_signature(
                question, old_answers, answer, 'ans_sh_signature')
        elif question.question_type in ['que_sh_address']:
            self.save_line_que_sh_address(
                question, old_answers, answer, 'ans_sh_address')

        elif question.question_type in ['que_sh_many2one']:
            self.save_line_que_sh_many2one(
                question, old_answers, answer, 'ans_sh_many2one')

        elif question.question_type in ['que_sh_many2many']:
            self.save_line_que_sh_many2many(
                question, old_answers, answer, 'ans_sh_many2many')            
        elif question.question_type in ['que_sh_qrcode']:
            self.save_line_que_sh_field(
                question, old_answers, answer, 'ans_sh_qrcode')
        elif question.question_type in ['que_sh_barcode']:
            self.save_line_que_sh_field(
                question, old_answers, answer, 'ans_sh_barcode')
        elif question.question_type in ['que_sh_location']:
            self.save_line_que_sh_location(
                question, old_answers, answer, 'ans_sh_location')
        else:
            raise AttributeError(question.question_type +
                                 ": This type of question has no saving function")

    # ====================================================================
    #for color field.
    # ====================================================================
    @api.model
    def save_line_que_sh_location(self, question, old_answers, answer, answer_type):
        vals_list = []

        vals = {
            'user_input_id': self.id,
            'question_id': question.id,
            'skipped': False,
            'answer_type': answer_type,
        }
        if not answer or (isinstance(answer, str) and not answer.strip()):
            vals.update(answer_type=None, skipped=True)
            return vals
        vals['value_%s' % answer_type] = answer
        if(answer and len(answer.split('&')) > 0):

            vals['value_sh_location_latitude'] = answer.split('&')[0]
            vals['value_sh_location_longitude'] = answer.split('&')[1]
            vals['value_ans_sh_location'] = answer
    
        vals_list.append(vals)
        old_answers.sudo().unlink()
        return self.env['survey.user_input.line'].create(vals_list)


class survey_user_input_line(models.Model):
    _inherit = 'survey.user_input.line'
    _description = 'Survey User Input Line for extra fields'

    value_ans_sh_qrcode = fields.Char(string="QR Code")
    value_ans_sh_barcode = fields.Char(string="Barcode")

    value_sh_location_latitude = fields.Char(string="Latitude")
    value_sh_location_longitude = fields.Char(string="Longitude")
    value_ans_sh_location = fields.Char(string="Location")

    answer_type = fields.Selection(selection_add=[
        ('ans_sh_qrcode', 'QR Code'),
        ('ans_sh_barcode', 'Barcode'),
        ('ans_sh_location', 'Location')
    ])
