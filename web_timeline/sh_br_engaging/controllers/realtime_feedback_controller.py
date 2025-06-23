from odoo.http import request
from odoo import http
from datetime import datetime

#----------------------------------------------------------
# Odoo Web Controllers
#----------------------------------------------------------
class RealtimeFeedbackController(http.Controller):

    @http.route(['/get/realtime_feedback/data'], type='json', auth='public', methods=['POST'])
    def get_realtime_feedback_data(self):
        response_data = {}
        todays_date = datetime.now()
        login_user_id = request.env.user.id

        # Perform Query To Find Pending Request Records :- 
        sh_pending_requests = f"""SELECT ARRAY(select id from sh_realtime_feedback where sh_parent_id is null and sh_feedback_type='request_feedback' and sh_realtime_feedback_person={login_user_id})"""
        request.env.cr.execute(sh_pending_requests)
        pending_requests_records = request._cr.fetchall()[0][0]
        non_parent_pending_requests_records = []
        for pending_requests_record in pending_requests_records :
            find_non_parent_records = f"""SELECT ARRAY(SELECT id FROM sh_realtime_feedback WHERE sh_parent_id = {pending_requests_record})"""
            request.env.cr.execute(find_non_parent_records)
            fetch_non_parent_records = request._cr.fetchall()[0][0]
            if not fetch_non_parent_records :
                non_parent_pending_requests_records.append(pending_requests_record)
        
        length_of_non_parent_pending_requests_records_list = len(non_parent_pending_requests_records)



        # Format the current date into character.
        today_date_in_string_format = todays_date.strftime("%d %B, %Y")

        # Get Data From Realtime Feedback Model 
        sh_realtime_feedback_model = f"""SELECT ARRAY(SELECT id FROM sh_realtime_feedback WHERE sh_parent_id IS NULL)"""
        request.env.cr.execute(sh_realtime_feedback_model)
        all_records = request._cr.fetchall()[0][0]
        all_feedbacks = []
        for record in all_records:
            browse_particular_record = request.env['sh.realtime.feedback'].browse(record)
            feedback_user_details = request.env['res.users'].browse(browse_particular_record.sh_created_by_id.id)
            received_feedback_user_details =  request.env['res.users'].browse(browse_particular_record.sh_realtime_feedback_person.id)

            if browse_particular_record.sh_feedback_review_selection == "public" :
                show_reply_button = False
                show_awaiting_responce_text = False
                if browse_particular_record.sh_realtime_feedback_person.id == request.env.user.id and browse_particular_record.sh_feedback_type == 'request_feedback':
                    show_reply_button = True
                
                if browse_particular_record.sh_created_by_id.id == request.env.user.id and browse_particular_record.sh_feedback_type == 'request_feedback':
                    show_awaiting_responce_text = True

                feedback_item = {
                    'feedback_text' : browse_particular_record.name,
                    'feedback_user_id' : feedback_user_details.id,
                    'feedback_user_name' : feedback_user_details.name,
                    'receieved_feedback_user_name' : received_feedback_user_details.name,
                    'feedback_type' : browse_particular_record.sh_feedback_type,
                    'feedback_create_date' : browse_particular_record.sh_create_date,
                    'show_reply_button' : show_reply_button,
                    'show_awaiting_responce_text' : show_awaiting_responce_text,
                    'backend_record_id': browse_particular_record.id,
                }

                child_record=request.env['sh.realtime.feedback'].sudo().search([('sh_parent_id','=',browse_particular_record.id)],limit=1)
                if child_record:
                    child_dict={
                        'feedback_text' : child_record.name,
                        'feedback_user_id' : child_record.sh_created_by_id.id,
                        'feedback_user_name' : child_record.sh_created_by_id.name,
                        'feedback_create_date' : child_record.sh_create_date,
                        'show_reply_button' : False,
                        'backend_record_id': child_record.id,
                    }
                    feedback_item.update({
                        'child_id_details':child_dict,
                        'show_reply_button' : False,
                        'show_awaiting_responce_text' : False,
                    })

                all_feedbacks.append(feedback_item)
                # Solve Sequence Issue By Sorting Dictionary With backend_record_id
                sorted_feedbacks = sorted(all_feedbacks, key=lambda x: x['backend_record_id'], reverse=True)

                # ** Code For Groupby Functionality **
                # find_groupby_feedback_records = f"""SELECT ARRAY(select sh_create_date from sh_realtime_feedback where sh_parent_id is null group by sh_create_date order by sh_create_date desc)"""
                find_groupby_feedback_records = f"""SELECT ARRAY(select sh_create_date from sh_realtime_feedback where sh_parent_id is null group by sh_create_date order by MAX(id) DESC)"""
                request.env.cr.execute(find_groupby_feedback_records)
                groupby_date_feedback = request._cr.fetchall()[0][0]

                login_user_name = request.env.user.name
                response_data['all_feedbacks'] = sorted_feedbacks
                response_data['login_user_name'] = login_user_name
                response_data['today_date_in_string_format'] = today_date_in_string_format
                response_data['pending_request_records_length'] = length_of_non_parent_pending_requests_records_list
                # Group By Date Functionality 
                response_data['group_by_feedback_list'] = groupby_date_feedback
        
            elif browse_particular_record.sh_feedback_review_selection == "manager" :
                # == Find Given Feedback User's Manager  ==
                given_feedback_user_coach = browse_particular_record.sh_created_by_id.sudo().employee_id.parent_id
                given_coach_user = 0
                if given_feedback_user_coach :
                    given_coach_user = given_feedback_user_coach.user_id.id

                # == Find Received Feedback User's Manager  ==
                received_feedback_user_coach = browse_particular_record.sh_realtime_feedback_person.sudo().employee_id.parent_id
                received_coach_user = 0
                if received_feedback_user_coach :
                    received_coach_user  = received_feedback_user_coach.user_id.id

                # if request.env.user.has_group('sh_br_engaging.group_br_engage_manager') or request.env.user.id == browse_particular_record.sh_created_by_id.id or request.env.user.id == browse_particular_record.sh_realtime_feedback_person.id :
                if request.env.user.id == given_coach_user or request.env.user.id == received_coach_user or request.env.user.id == browse_particular_record.sh_created_by_id.id or request.env.user.id == browse_particular_record.sh_realtime_feedback_person.id :
                    show_reply_button = False
                    show_awaiting_responce_text = False
                    if browse_particular_record.sh_realtime_feedback_person.id == request.env.user.id and browse_particular_record.sh_feedback_type == 'request_feedback':
                        show_reply_button = True
                    
                    if browse_particular_record.sh_created_by_id.id == request.env.user.id and browse_particular_record.sh_feedback_type == 'request_feedback':
                        show_awaiting_responce_text = True

                    feedback_item = {
                        'feedback_text' : browse_particular_record.name,
                        'feedback_user_id' : feedback_user_details.id,
                        'feedback_user_name' : feedback_user_details.name,
                        'receieved_feedback_user_name' : received_feedback_user_details.name,
                        'feedback_type' : browse_particular_record.sh_feedback_type,
                        'feedback_create_date' : browse_particular_record.sh_create_date,
                        'show_reply_button' : show_reply_button,
                        'show_awaiting_responce_text' : show_awaiting_responce_text,
                        'backend_record_id': browse_particular_record.id,
                    }

                    child_record=request.env['sh.realtime.feedback'].sudo().search([('sh_parent_id','=',browse_particular_record.id)],limit=1)
                    if child_record:
                        child_dict={
                            'feedback_text' : child_record.name,
                            'feedback_user_id' : child_record.sh_created_by_id.id,
                            'feedback_user_name' : child_record.sh_created_by_id.name,
                            'feedback_create_date' : child_record.sh_create_date,
                            'show_reply_button' : False,
                            'backend_record_id': child_record.id,
                        }
                        feedback_item.update({
                            'child_id_details':child_dict,
                            'show_reply_button' : False,
                            'show_awaiting_responce_text' : False,
                        })

                    all_feedbacks.append(feedback_item)

                    # Solve Sequence Issue By Sorting Dictionary With backend_record_id
                    sorted_feedbacks = sorted(all_feedbacks, key=lambda x: x['backend_record_id'], reverse=True)

                    # ** Code For Groupby Functionality **
                    # find_groupby_feedback_records = f"""SELECT ARRAY(select sh_create_date from sh_realtime_feedback where sh_parent_id is null group by sh_create_date order by sh_create_date desc)"""
                    find_groupby_feedback_records = f"""SELECT ARRAY(select sh_create_date from sh_realtime_feedback where sh_parent_id is null group by sh_create_date order by MAX(id) DESC)"""
                    request.env.cr.execute(find_groupby_feedback_records)
                    groupby_date_feedback = request._cr.fetchall()[0][0]

                    login_user_name = request.env.user.name
                    response_data['all_feedbacks'] = sorted_feedbacks
                    response_data['login_user_name'] = login_user_name
                    response_data['today_date_in_string_format'] = today_date_in_string_format
                    response_data['pending_request_records_length'] = length_of_non_parent_pending_requests_records_list
                    # Group By Date Functionality 
                    response_data['group_by_feedback_list'] = groupby_date_feedback
            
            elif browse_particular_record.sh_feedback_review_selection == "recepient_only" :
                if request.env.user.id == browse_particular_record.sh_created_by_id.id or request.env.user.id == browse_particular_record.sh_realtime_feedback_person.id :
                    show_reply_button = False
                    show_awaiting_responce_text = False
                    if browse_particular_record.sh_realtime_feedback_person.id == request.env.user.id and browse_particular_record.sh_feedback_type == 'request_feedback':
                        show_reply_button = True
                    
                    if browse_particular_record.sh_created_by_id.id == request.env.user.id and browse_particular_record.sh_feedback_type == 'request_feedback':
                        show_awaiting_responce_text = True

                    feedback_item = {
                        'feedback_text' : browse_particular_record.name,
                        'feedback_user_id' : feedback_user_details.id,
                        'feedback_user_name' : feedback_user_details.name,
                        'receieved_feedback_user_name' : received_feedback_user_details.name,
                        'feedback_type' : browse_particular_record.sh_feedback_type,
                        'feedback_create_date' : browse_particular_record.sh_create_date,
                        'show_reply_button' : show_reply_button,
                        'show_awaiting_responce_text' : show_awaiting_responce_text,
                        'backend_record_id': browse_particular_record.id,
                    }

                    child_record=request.env['sh.realtime.feedback'].sudo().search([('sh_parent_id','=',browse_particular_record.id)],limit=1)
                    if child_record:
                        child_dict={
                            'feedback_text' : child_record.name,
                            'feedback_user_id' : child_record.sh_created_by_id.id,
                            'feedback_user_name' : child_record.sh_created_by_id.name,
                            'feedback_create_date' : child_record.sh_create_date,
                            'show_reply_button' : False,
                            'backend_record_id': child_record.id,
                        }
                        feedback_item.update({
                            'child_id_details':child_dict,
                            'show_reply_button' : False,
                            'show_awaiting_responce_text' : False,
                        })

                    all_feedbacks.append(feedback_item)

                    # Solve Sequence Issue By Sorting Dictionary With backend_record_id
                    sorted_feedbacks = sorted(all_feedbacks, key=lambda x: x['backend_record_id'], reverse=True)

                    # ** Code For Groupby Functionality **
                    # find_groupby_feedback_records = f"""SELECT ARRAY(select sh_create_date from sh_realtime_feedback where sh_parent_id is null group by sh_create_date order by sh_create_date desc)"""
                    find_groupby_feedback_records = f"""SELECT ARRAY(select sh_create_date from sh_realtime_feedback where sh_parent_id is null group by sh_create_date order by MAX(id) DESC)"""
                    request.env.cr.execute(find_groupby_feedback_records)
                    groupby_date_feedback = request._cr.fetchall()[0][0]

                    login_user_name = request.env.user.name
                    response_data['all_feedbacks'] = sorted_feedbacks
                    response_data['login_user_name'] = login_user_name
                    response_data['today_date_in_string_format'] = today_date_in_string_format
                    response_data['pending_request_records_length'] = length_of_non_parent_pending_requests_records_list
                    # Group By Date Functionality 
                    response_data['group_by_feedback_list'] = groupby_date_feedback

            
        return response_data
    

    @http.route(['/post/realtime_feedback/data'], type='json', auth='public', methods=['POST'])
    def postButtonController(self, feedback_text, date_of_feedback_record, parent_record_id):
        response_data = {}

        realtime_feedback_vals={
                        # 'sh_realtime_feedback_person':self.sh_give_feedback_person.id,
                        'name':feedback_text,
                        'sh_feedback_review_selection': 'public',
                        'sh_feedback_type' : 'give_feedback',
                        'sh_created_by_id' : request.env.user.id,
                        'sh_create_date' : date_of_feedback_record,
                        'sh_parent_id' : parent_record_id,
                    }
        request.env['sh.realtime.feedback'].sudo().create(realtime_feedback_vals)

        return response_data

