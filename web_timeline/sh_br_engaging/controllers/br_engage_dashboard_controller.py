from odoo.http import request
from odoo import http
from datetime import datetime

#----------------------------------------------------------
# Odoo Web Controllers
#----------------------------------------------------------
class BRDashboard(http.Controller):

    @http.route(['/get/br_engage_dashboard/data'], type='json', auth='public', methods=['POST'])
    def br_dashboard_setup_controller(self):
        response_data = {}
        login_user_id = request.env.user.id

        current_user_partner_id=request.env.user.partner_id.id

        login_user_name = request.env.user.name
        todays_date = datetime.now()
        today_date_in_string_format = todays_date.strftime("%d %B, %Y")

        # Perform Query To Find Latest Record Of Check-In :- 
        check_in_query = f"""SELECT ARRAY(select id from sh_check_in where sh_user_id = {login_user_id} ORDER BY ID DESC)"""
        request.env.cr.execute(check_in_query)
        check_in_records = request._cr.fetchall()[0][0]
        check_in_list = []
        if check_in_records :
            latest_chek_in_record = check_in_records[0]
            browse_latest_record = request.env['sh.check.in'].browse(latest_chek_in_record)
            # === GET THE CREATE DATE AND FORMAT THAT INTO DIFFERENT FORMAT ===
            check_in_create_date = browse_latest_record.create_date

            # Format the date as "15 February, 2024"
            check_in_create_format_date = check_in_create_date.strftime("%d %B, %Y")

            check_in_details_dict = {
                'count_of_records' : len(check_in_records),
                'id_of_latest_record' : browse_latest_record.id,
                'latest_record_name' : browse_latest_record.name,
                'check_in_date' : check_in_create_format_date
            } 
            
            check_in_list.append(check_in_details_dict)

        meeting_list = []

        if current_user_partner_id:

            current_partner_id = request.env.user.partner_id


            # meeting_records = f"""SELECT ARRAY(select id from calendar_event ORDER BY ID DESC)"""
            # request.env.cr.execute(meeting_records)
            # meeting_records = request._cr.fetchall()[0][0]
            meeting_records = request.env['calendar.event'].sudo().search([('partner_ids','in', current_partner_id.ids)],order='id desc')
            if meeting_records :
                latest_meeting_record = meeting_records[0]
                # browse_latest_record = request.env['calendar.event'].sudo().browse(latest_meeting_record)

                 # === GET THE CREATE DATE AND FORMAT THAT INTO DIFFERENT FORMAT ===
                meeting_create_date = latest_meeting_record.create_date

                # Format the date as "15 February, 2024"
                meeting_create_format_date = meeting_create_date.strftime("%d %B, %Y")

                meeting_details_dict = {
                    'count_of_records' : len(meeting_records),
                    'id_of_latest_record' : latest_meeting_record.id,
                    'latest_record_name' : latest_meeting_record.name,
                    'meeting_create_date' : meeting_create_format_date,
                } 
                
                meeting_list.append(meeting_details_dict)
        
        # === Code Of 1on1's Records ===
        current_partner_id = request.env.user.partner_id
        employee_id = request.env.user.employee_id.id if request.env.user.employee_id else 0
        # Perform Query To Find The Count Of 1on1s Records :- 
        # find_1on1s_query = f""" SELECT ARRAY(select id from calendar_event where partner_ids = {current_partner_id} ORDER BY ID DESC) """
        # request.env.cr.execute(find_1on1s_query)
        # record_1on1 = request._cr.fetchall()[0][0]

        # find_1on1s_query = request.env["calendar.event"].sudo().search([('partner_ids', 'in', current_partner_id.ids),('sh_talking_point_id', '!=', False)])
        find_1on1s_query = request.env["sh.talking.points"].sudo().search(['|',('sh_user_id', '=', request.env.user.id),('sh_employee_id','=',employee_id)],order='id desc')
        multiple_ids_list_for_tree = [] 
        multiple_ids_list_for_tree = find_1on1s_query.ids
        list_of_1on1_records = []
        if find_1on1s_query :
            latest_1on1s_record = find_1on1s_query[0]
             # === GET THE CREATE DATE AND FORMAT THAT INTO DIFFERENT FORMAT ===
            OneonOnes_create_date = latest_1on1s_record.create_date

            # Format the date as "15 February, 2024"
            OneonOnes_create_format_date = OneonOnes_create_date.strftime("%d %B, %Y")


            detail_dict_of_1on1s = {
                'count_of_records' : len(find_1on1s_query),
                'multiple_ids_list_for_tree' : multiple_ids_list_for_tree,
                'latest_record_name' : latest_1on1s_record.name,
                'record_create_date' : OneonOnes_create_format_date,
            } 
        
            list_of_1on1_records.append(detail_dict_of_1on1s)
        
        # ** Code Of Realtime Feedback Data **
        # sh_pending_requests = f"""SELECT ARRAY(select id from sh_realtime_feedback where sh_parent_id is null and sh_feedback_type='request_feedback' and sh_realtime_feedback_person={login_user_id})"""
        sh_feedback_dashboard_query = f"""SELECT ARRAY(select id from sh_realtime_feedback where sh_parent_id is null and (sh_realtime_feedback_person={login_user_id} or sh_created_by_id={login_user_id}))"""
        request.env.cr.execute(sh_feedback_dashboard_query)
        sh_feedback_dashboard_records = request._cr.fetchall()[0][0]
        

        all_feedbacks = []
        for feedback_record in sh_feedback_dashboard_records:
            browse_particular_record = request.env['sh.realtime.feedback'].browse(feedback_record)
            feedback_user_details = request.env['res.users'].browse(browse_particular_record.sh_created_by_id.id)
            received_feedback_user_details =  request.env['res.users'].browse(browse_particular_record.sh_realtime_feedback_person.id)

            feedback_item = {
                'feedback_text' : browse_particular_record.name,
                'feedback_type' : browse_particular_record.sh_feedback_type,
                'receieved_feedback_user_name' : received_feedback_user_details.name,
                'feedback_user_id' : feedback_user_details.id,
                'feedback_user_name' : feedback_user_details.name,
                'feedback_create_date' : browse_particular_record.sh_create_date,
                'backend_record_id': browse_particular_record.id,
            }
            
            # Get Child Records 
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

        
        # ** Code Of High Five Data **
        # Perform Query To Find Records Of High Five Model :- 
        sh_high_five = f"""SELECT ARRAY(select id from sh_high_five where sh_parent_id is null and (sh_from_user_id={login_user_id} or sh_to_user_id={login_user_id}))"""
        request.env.cr.execute(sh_high_five)
        sh_high_five_records = request._cr.fetchall()[0][0]
        sh_high_five_records_list = []
        for sh_high_five_record in sh_high_five_records :
            show_like_btn = True
            browse_high_five_record = request.env['sh.high.five'].browse(sh_high_five_record)
            like_count = len(browse_high_five_record.sh_liked_by_ids)
            if login_user_id in browse_high_five_record.sh_liked_by_ids.ids:
                show_like_btn = False
            
            high_five_item = {
                'id' : browse_high_five_record.id,
                'high_five_text' : browse_high_five_record.name,
                'sh_from_user_id': browse_high_five_record.sh_from_user_id.id,
                'sh_to_user_name': browse_high_five_record.sh_to_user_id.name,
                'sh_from_user_name': browse_high_five_record.sh_from_user_id.name,
                'show_like_btn': show_like_btn,
                'like_count': like_count,
                'record_creation_date' : browse_high_five_record.sh_high_five_creation_date,
            }
            sh_high_five_records_list.append(high_five_item)
        
    # =================================================================================================================
    #    ***** WALL OF FAME RECORDS ***** 
    # =================================================================================================================
    
        # # === First assign Blank Value If We Don't Find Any High Five Records ===
        first_top_high_fiver_employee_id = 0
        first_top_high_fiver_employee_name = 'Pending'
        sh_name_of_highest_badge = ''
        top_first_high_fiver_received_counts = 0
        first_post_record_update_date = ''

        second_top_high_fiver_employee_id = 0
        second_top_high_fiver_employee_name = 'Pending'
        top_second_high_fiver_given_count = 0
        top_second_high_fiver_received_count = 0
        second_post_record_update_date = ''

        third_top_high_fiver_employee_id = 0
        third_top_high_fiver_employee_name = 'Pending'
        top_third_high_fiver_given_count = 0
        top_third_high_fiver_received_count = 0
        third_post_record_update_date = ''

        # ==========================================================================================================================================
        #                                                  *==* GET THE DATA OF FIRST POST EMPLOYEE *==* 
        # ==========================================================================================================================================
        first_post_employee_record = request.env["sh.update.wall.of.fame.data"].sudo().search([('sh_employee_post_selection', '=', 'sh_first_post')])
        if first_post_employee_record :
            find_user = first_post_employee_record.sh_wall_of_fame_user_id
            find_badge = first_post_employee_record.sh_first_post_employee_badge
            find_upate_date = first_post_employee_record.sh_date_of_update
            if find_user : 
                first_top_high_fiver_employee_id = find_user.id
                first_top_high_fiver_employee_name = find_user.name
            if find_badge : 
                sh_name_of_highest_badge = find_badge.name
            if find_upate_date : 
                first_post_record_update_date = find_upate_date

        # ==========================================================================================================================================
        #                                                  *==* GET THE DATA OF SECOND POST EMPLOYEE *==* 
        # ==========================================================================================================================================
        second_post_employee_record = request.env["sh.update.wall.of.fame.data"].sudo().search([('sh_employee_post_selection', '=', 'sh_second_post')])
        if second_post_employee_record :
            find_second_user = second_post_employee_record.sh_wall_of_fame_user_id
            find_record_update_date = second_post_employee_record.sh_date_of_update
            if find_second_user : 
                second_top_high_fiver_employee_id = find_second_user.id
                second_top_high_fiver_employee_name = find_second_user.name
            if find_record_update_date : 
                second_post_record_update_date = find_record_update_date

        # ==========================================================================================================================================
        #                                                  *==* GET THE DATA OF THIRD POST EMPLOYEE *==* 
        # ==========================================================================================================================================
        third_post_employee_record = request.env["sh.update.wall.of.fame.data"].sudo().search([('sh_employee_post_selection', '=', 'sh_third_post')])
        if third_post_employee_record :
            find_third_user = third_post_employee_record.sh_wall_of_fame_user_id
            find_third_record_update_date = third_post_employee_record.sh_date_of_update
            if find_third_user : 
                third_top_high_fiver_employee_id = find_third_user.id
                third_top_high_fiver_employee_name = find_third_user.name
            if find_third_record_update_date : 
                third_post_record_update_date = find_third_record_update_date



        # Solve Sequence Issue By Sorting Dictionary With id In High Five And backend_record_id In Feedback
        sh_sorted_high_five_dashboard_records = sorted(sh_high_five_records_list, key=lambda x: x['id'], reverse=True)
        sh_sorted_feedback_dashboard_records = sorted(all_feedbacks, key=lambda x: x['backend_record_id'], reverse=True)
        # ==================================================================
        response_data['1on1s_all_details'] = list_of_1on1_records
        response_data['check_in_all_details'] = check_in_list
        response_data['meeting_all_details'] = meeting_list
        response_data['login_user_name'] = login_user_name
        response_data['login_user_id'] = login_user_id
        response_data['todays_date'] = today_date_in_string_format
        response_data['all_feedbacks'] = sh_sorted_feedback_dashboard_records
        response_data['sh_high_five_records_list'] = sh_sorted_high_five_dashboard_records
        # ** WALL OF FAME DETAILS **
        response_data['first_top_high_fiver_employee_id'] = first_top_high_fiver_employee_id
        response_data['first_top_high_fiver_employee_name'] = first_top_high_fiver_employee_name
        response_data['sh_name_of_highest_badge'] = sh_name_of_highest_badge
        response_data['top_first_high_fiver_received_counts'] = top_first_high_fiver_received_counts
        response_data['first_post_record_update_date'] = first_post_record_update_date

        response_data['second_top_high_fiver_employee_id'] = second_top_high_fiver_employee_id
        response_data['second_top_high_fiver_employee_name'] = second_top_high_fiver_employee_name
        response_data['top_second_high_fiver_given_count'] = top_second_high_fiver_given_count
        response_data['top_second_high_fiver_received_count'] = top_second_high_fiver_received_count
        response_data['second_post_record_update_date'] = second_post_record_update_date

        response_data['third_top_high_fiver_employee_id'] = third_top_high_fiver_employee_id
        response_data['third_top_high_fiver_employee_name'] = third_top_high_fiver_employee_name
        response_data['top_third_high_fiver_given_count'] = top_third_high_fiver_given_count
        response_data['top_third_high_fiver_received_count'] = top_third_high_fiver_received_count
        response_data['third_post_record_update_date'] = third_post_record_update_date

        return response_data
    





    # =========================================
    # *** COPY CONTROLLERS FROM HIGH FIVE ***  
    # =========================================
    @http.route(['/post/dashboard/like_btn/data'], type='json', auth='public', methods=['POST'])
    def update_like_button(self,record_id):
        responce_data = []
        like_record = request.env['sh.high.five'].sudo().search([('id', '=', record_id)])
        like_record.write({
        'sh_liked_by_ids': [(4, request.env.user.id)]  # Add the employee to the Many2many field
    })
        return responce_data
    

    @http.route(['/post/dashboard/unlike_btn/data'], type='json', auth='public', methods=['POST'])
    def update_unlike_button(self,record_id):
        responce_data = []
        like_record = request.env['sh.high.five'].sudo().search([('id', '=', record_id)])
        like_record.write({
        'sh_liked_by_ids': [(3, request.env.user.id)]  # Add the employee to the Many2many field
    })
        return responce_data
    
    @http.route(['/post/dashboard/delete_btn/data'], type='json', auth='public', methods=['POST'])
    def delete_button_method(self,record_id):
        responce_data = []
        delete_record = request.env['sh.high.five'].sudo().search([('id', '=', record_id)])
        browse_delete_record = request.env['sh.high.five'].sudo().browse(record_id)
        if browse_delete_record.sh_child_ids:
            for child_record in browse_delete_record.sh_child_ids :
                child_record.unlink()
        delete_record.unlink()
        return responce_data
    

