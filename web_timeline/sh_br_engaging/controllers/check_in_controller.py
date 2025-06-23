from odoo.http import request
from odoo import http
from datetime import datetime


#----------------------------------------------------------
# Odoo Web Controllers
#----------------------------------------------------------
class CheckInController(http.Controller):

    @http.route(['/get/check_in/data'], type='json', auth='public', methods=['POST'])
    def get_check_in_data(self, res_id):
        browse_current_model = request.env['sh.check.in'].browse(res_id)
        response_data = {}
        
        if browse_current_model.sh_stage == 'draft':
            sh_question_answer_id = f"""SELECT ARRAY(SELECT id FROM sh_question_answers WHERE sh_check_in_id={res_id})"""
            request.env.cr.execute(sh_question_answer_id)
            responce = request._cr.fetchall()[0][0]
            sh_question_answer_model_browse = request.env['sh.question.answers'].browse(responce)
            non_rating_questions = []
            rating_questions = []
            sh_how_feel_question_id = 0
            for questions in sh_question_answer_model_browse:
                if not questions.sh_question_id.sh_is_rating_question:
                    if questions.sh_answer :
                        non_rating_question_dict = {
                            'question_id' : questions.sh_question_id.id,
                            'question_text' : questions.sh_question_id.name,
                            'answer_text' : questions.sh_answer,
                        }
                    else:
                        non_rating_question_dict = {
                            'question_id' : questions.sh_question_id.id,
                            'question_text' : questions.sh_question_id.name,
                        }
                    non_rating_questions.append(non_rating_question_dict)
                else:
                    if questions.sh_answer :
                        rating_question_dict = {
                            'question_id' : questions.sh_question_id.id,
                            'question_text' : questions.sh_question_id.name,
                            'answer_text' : questions.sh_answer,
                            'low_rating_reason' : questions.sh_low_rating_reason
                        }
                    else:
                        rating_question_dict = {
                            'question_id' : questions.sh_question_id.id,
                            'question_text' : questions.sh_question_id.name,
                        }
                    
                    is_how_feel_question = questions.sh_question_id.sh_how_did_you_feel_question
                    if is_how_feel_question :
                        rating_question_dict.update({
                            'sh_how_feel_question' : True
                        })
                        sh_how_feel_question_id = questions.sh_question_id.id
                    rating_questions.append(rating_question_dict)
            
            # login_user_name = request.env.user.name
            login_user_name = browse_current_model.sh_user_id.name if browse_current_model.sh_user_id else ''
            ans_records_for_submited_model = False
            sh_is_record_submited = False
            rating_ans_for_submited_model = False
            get_current_record_name = browse_current_model.name

            # Code to get Dynamic Name For Each Check-In Record
            login_user_id = request.env.user.id
            sh_check_in_model_ids = f"""SELECT ARRAY(SELECT id FROM sh_check_in WHERE sh_user_id={browse_current_model.sh_user_id.id} AND id!={res_id})"""
            request.env.cr.execute(sh_check_in_model_ids)
            responce = request._cr.fetchall()[0][0]
            sh_browse_check_in_model = request.env['sh.check.in'].browse(responce)

            # Create Custom Dictionary To Store Name And Id As Key And Pair Form
            check_in_model_id_name_dict = {}
            for record in sh_browse_check_in_model:
                id = record.id
                name = record.name
                check_in_model_id_name_dict[id] = name
            
            # Solve Sequence Issue By Sorting Dictionary With Question Id
            non_rating_questions = sorted(non_rating_questions, key=lambda x: x['question_id'])
            rating_questions = sorted(rating_questions, key=lambda x: x['question_id'])

            # Add data to the response_data for draft
            response_data['stage'] = 'draft'
            response_data['non_rating_questions'] = non_rating_questions
            response_data['rating_questions'] = rating_questions
            response_data['login_user_name'] = login_user_name
            response_data['ans_records_for_submited_model'] = ans_records_for_submited_model
            response_data['sh_is_record_submited'] = sh_is_record_submited
            response_data['rating_ans_for_submited_model'] = rating_ans_for_submited_model
            response_data['name'] = get_current_record_name
            response_data['check_in_model_id_name_dict'] = check_in_model_id_name_dict
            response_data['sh_how_feel_question_id'] = sh_how_feel_question_id

        elif browse_current_model.sh_stage == 'submitted':
            sh_question_answer_id = f"""SELECT ARRAY(SELECT id FROM sh_question_answers WHERE sh_check_in_id={res_id})"""
            request.env.cr.execute(sh_question_answer_id)
            responce = request._cr.fetchall()[0][0]
            sh_question_answer_model_browse = request.env['sh.question.answers'].browse(responce)
            non_rating_questions = []
            rating_questions = []
            ans_records_for_submited_model = []
            rating_ans_for_submited_model = []
            for questions in sh_question_answer_model_browse:
                if not questions.sh_question_id.sh_is_rating_question:
                    if questions.sh_answer :
                        non_rating_question_dict = {
                            'question_id' : questions.sh_question_id.id,
                            'question_text' : questions.sh_question_id.name,
                            'answer_text' : questions.sh_answer,
                        }
                    else:
                        non_rating_question_dict = {
                            'question_id' : questions.sh_question_id.id,
                            'question_text' : questions.sh_question_id.name,
                        }
                    non_rating_questions.append(non_rating_question_dict)
                    ans_records_for_submited_model.append(questions.sh_answer)
                else:
                    if questions.sh_answer :
                        # == Code To Add Low Rating Reason Into Dictionary == 
                        if questions.sh_low_rating_reason :
                            rating_question_dict = {
                                'question_id' : questions.sh_question_id.id,
                                'question_text' : questions.sh_question_id.name,
                                'answer_text' : questions.sh_answer,
                                'sh_low_rating_reason' : questions.sh_low_rating_reason,
                            }
                        else :
                            rating_question_dict = {
                                'question_id' : questions.sh_question_id.id,
                                'question_text' : questions.sh_question_id.name,
                                'answer_text' : questions.sh_answer,
                            }
                    else:
                        rating_question_dict = {
                            'question_id' : questions.sh_question_id.id,
                            'question_text' : questions.sh_question_id.name,
                        }
                    rating_questions.append(rating_question_dict)
                    rating_ans_for_submited_model.append(questions.sh_answer)

            # ans_records_for_submited_model = []
            # rating_ans_for_submited_model = []
            # for questions in sh_question_answer_model_browse:
            #     if not questions.sh_question_id.sh_is_rating_question:
            #         non_rating_questions.append(questions.sh_question_id.name)
            #         ans_records_for_submited_model.append(questions.sh_answer)
            #     else:
            #         rating_questions.append(questions.sh_question_id.name)
            #         rating_ans_for_submited_model.append(questions.sh_answer)
            
            # login_user_name = request.env.user.name
            login_user_name = browse_current_model.sh_user_id.name if browse_current_model.sh_user_id else ''

            sh_is_record_submited = True
            get_current_record_name = browse_current_model.name

           # Code to get Dynamic Name For Each Check-In Record
            login_user_id = request.env.user.id
            sh_check_in_model_ids = f"""SELECT ARRAY(SELECT id FROM sh_check_in WHERE sh_user_id={browse_current_model.sh_user_id.id} AND id!={res_id})"""
            request.env.cr.execute(sh_check_in_model_ids)
            responce = request._cr.fetchall()[0][0]
            sh_browse_check_in_model = request.env['sh.check.in'].browse(responce)

            # Create Custom Dictionary To Store Name And Id As Key And Pair Form
            check_in_model_id_name_dict = {}
            for record in sh_browse_check_in_model:
                id = record.id
                name = record.name
                check_in_model_id_name_dict[id] = name



            # to add data of 1-on-1 in smart button in check-in view

            smart_button_1_on_1s_data=False
            sh_talking_point_id = f"""SELECT ARRAY(SELECT id FROM sh_talking_points WHERE sh_check_in_id={res_id})"""
            request.env.cr.execute(sh_talking_point_id)
            responce = request._cr.fetchall()[0][0]

            if responce:
                sh_1_on_1_ids = f"""SELECT ARRAY(SELECT id FROM calendar_event WHERE sh_talking_point_id = {responce[0]})"""
                request.env.cr.execute(sh_1_on_1_ids)
                responce = request._cr.fetchall()[0][0]

                if responce:
                    smart_button_1_on_1s_data={
                        'count':len(responce),
                        'event_ids':responce,
                    }

            # Add data to the response_data for submitted
            response_data['stage'] = 'submitted'
            response_data['non_rating_questions'] = non_rating_questions
            response_data['rating_questions'] = rating_questions
            response_data['login_user_name'] = login_user_name
            response_data['ans_records_for_submited_model'] = ans_records_for_submited_model
            response_data['sh_is_record_submited'] = True
            response_data['rating_ans_for_submited_model'] = rating_ans_for_submited_model
            response_data['name'] = get_current_record_name
            response_data['check_in_model_id_name_dict'] = check_in_model_id_name_dict
            response_data['smart_button_1_on_1s_data'] = smart_button_1_on_1s_data if smart_button_1_on_1s_data else False

        return response_data

    @http.route(['/submit/data',], type='json', auth='public', methods=['POST'])
    def submit_checkIn(self, res_id, non_rating_answers_records, rating_answers_records, submit_low_rating_questions_reason_list):
        controller_responce = False
        question_data = f"""SELECT ARRAY(SELECT id FROM sh_question_answers WHERE sh_check_in_id=({res_id}))"""
        request.env.cr.execute(question_data)
        responce = request._cr.fetchall()[0][0]
        browse_question_model_for_condition = request.env['sh.question.answers'].browse(responce)

        # === Code To Find The NonRating Questions From One2many Model === 
        non_rating_questions_list = []
        for non_rating in browse_question_model_for_condition :
            if not non_rating.sh_question_id.sh_is_rating_question :
                non_rating_questions_list.append(non_rating.id)
        browse_check_in_model = request.env['sh.check.in'].browse(res_id)
        browse_check_in_model.write({'sh_stage': 'submitted'})

        # === Code to Perform the write method and store the answer of NonRating questions ===
        for record, answer in zip(non_rating_questions_list, non_rating_answers_records):
            non_rating_answers_record = request.env['sh.question.answers'].browse(record)
            non_rating_answers_record.write({'sh_answer': answer})
        
        # === Code To Find The Rating Questions From One2many Model === 
        rating_questions_list = []
        for rating in browse_question_model_for_condition :
            if rating.sh_question_id.sh_is_rating_question :
                rating_questions_list.append(rating.id)

        # === Code to Create new list from the rating questions dictionary ===
        # Sort the input dictionary by 'progressBarId'
        sorted_dict = sorted(rating_answers_records, key=lambda x: x['progressBarId'])
        # Extract 'selectedRating' values into a list
        selected_ratings = [item['selectedRating'] for item in sorted_dict]
        # === Code to Perform the write method and store the answer of rating questions ===
        for record, answer in zip(rating_questions_list, selected_ratings):
            rating_answer_record = request.env['sh.question.answers'].browse(record)
            rating_answer_record.write({'sh_answer': answer})

        selected_ratings = [item['selectedRating'] for item in rating_answers_records]
        need_to_create_meeting = False
        for answer_rating in selected_ratings :
            answer_rating = int(answer_rating)
            if answer_rating <= 3 :
                need_to_create_meeting = True
        if need_to_create_meeting :
            employee_id = browse_check_in_model.sh_employee_id

            talking_point_vals = {
                'name' : browse_check_in_model.name,
                'sh_employee_id' : browse_check_in_model.sh_employee_id.id,
                # 'sh_employee_id' : browse_check_in_model.sh_employee_id.sudo().parent_id.id,
                'sh_check_in_id' : browse_check_in_model.id,
                'sh_create_date' : datetime.now(),
                'is_auto_create' : True,
            }
            if browse_check_in_model.sh_employee_id and browse_check_in_model.sh_employee_id.sudo().user_id:
                talking_point_vals.update({
                    'sh_user_id':browse_check_in_model.sh_employee_id.sudo().parent_id.sudo().user_id.id
                })
            
            manage_agenda = request.env['sh.manage.agenda'].sudo().search([('sh_is_active','=',True)])
            agenda_vals = []
            if manage_agenda:
                for agenda in manage_agenda:
                    vals={
                         'sh_agenda_id':agenda.id,
                         'sh_checked':False,
                    }
                    agenda_vals.append((0,0,vals))
            if agenda_vals:    
                talking_point_vals['sh_manage_agenda_line']=agenda_vals
            talking_point=request.env['sh.talking.points'].sudo().create(talking_point_vals)

            # for br enagage user push notification
            # request.env['sh.br.engage.push.notification'].create_br_engage_push_notification(user=browse_check_in_model.sh_user_id,name="Talking Point Created",description="Talking Point created for user",res_model="sh.talking.points",res_id=talking_point.id)
        
        # === Code to Perform Write Method In Low Reason Field For Rating Question ===
        # Loop through 'low_rating_questions_records' and update 'sh_low_rating_reason'
        for low_rating_record in submit_low_rating_questions_reason_list:
            submit_reason_inputId = low_rating_record['reason_inputId']
            submit_answer_values = low_rating_record['answer_values']

            # Find the corresponding 'sh.question.answers' record and update 'sh_low_rating_reason'
            matching_record = browse_question_model_for_condition.filtered(lambda r: r.sh_question_id.id == submit_reason_inputId)
            if matching_record:
                matching_record.write({'sh_low_rating_reason': submit_answer_values})

        # CHECK OF WE FOUND LESS RATING OR NOT 
        if need_to_create_meeting :
            controller_responce = talking_point.id

        return controller_responce
    



     # === Save Controller === 
    @http.route(['/save/data',], type='json', auth='public', methods=['POST'])
    def save_checkIn(self, res_id, non_rating_answers_records, rating_answers_records, low_rating_questions_records):
        question_data = f"""SELECT ARRAY(SELECT id FROM sh_question_answers WHERE sh_check_in_id=({res_id}))"""
        request.env.cr.execute(question_data)
        response = request._cr.fetchall()[0][0]
        browse_question_model_for_condition = request.env['sh.question.answers'].browse(response)

        # Create mappings for 'InputId' to 'answer_values' and 'progressBarId' to 'selectedRating'
        non_rating_mapping = {record['InputId']: record['answer_values'] for record in non_rating_answers_records}
        rating_mapping = {record['progressBarId']: record['selectedRating'] for record in rating_answers_records}

        # Loop through 'sh.question.answers' records
        for record in browse_question_model_for_condition:
            InputId = record.sh_question_id.id
            progressBarId = record.sh_question_id.id

            if InputId in non_rating_mapping:
                # Update 'sh_answer' with the corresponding 'answer_values' for non-rating questions
                answer_values = non_rating_mapping[InputId]
                record.write({'sh_answer': answer_values})
            elif progressBarId in rating_mapping:
                # Update 'sh_answer' with the corresponding 'selectedRating' for rating questions
                selectedRating = rating_mapping[progressBarId]
                record.write({'sh_answer': selectedRating})

        # Loop through 'low_rating_questions_records' and update 'sh_low_rating_reason'
        for low_rating_record in low_rating_questions_records:
            reason_inputId = low_rating_record['reason_inputId']
            answer_values = low_rating_record['answer_values']

            # Find the corresponding 'sh.question.answers' record and update 'sh_low_rating_reason'
            matching_record = browse_question_model_for_condition.filtered(lambda r: r.sh_question_id.id == reason_inputId)
            if matching_record:
                matching_record.write({'sh_low_rating_reason': answer_values})

        return response




