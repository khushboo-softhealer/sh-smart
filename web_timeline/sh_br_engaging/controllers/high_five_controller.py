from odoo.http import request
from odoo import http
from datetime import datetime, date

#----------------------------------------------------------
# Odoo Web web Controllers
#----------------------------------------------------------
class HighFiveController(http.Controller):

    @http.route(['/get/high_five/data'], type='json', auth='public', methods=['POST'])
    def get_high_fives_data(self, domain=None, groupBy=None):
        response_data = {}
        todays_date = datetime.now()
        login_user_id = request.env.user.id
        login_user_name = request.env.user.name
        today_date_in_string_format = todays_date.strftime("%d %B, %Y")

        # ** Find The Top High Fiver ** 
        query_to_find_top_high_fiver = f""" SELECT sh_to_user_id, COUNT(id) AS received_count FROM sh_high_five 
                                            WHERE sh_parent_id IS NULL GROUP BY sh_to_user_id
                                            ORDER BY received_count DESC LIMIT 5 """ 
        request.env.cr.execute(query_to_find_top_high_fiver)
        redord_of_top_high_fiver = request._cr.fetchall()
        

        # # === First assign Blank Value If We Don't Find Any High Five Records ===
        # First 
        first_top_high_fiver_id = 0
        first_top_high_fiver_name = 'Pending'
        top_first_high_fiver_count = 0
        # Second
        second_top_high_fiver_id = 0
        second_top_high_fiver_name = 'Pending'
        top_second_high_fiver_count = 0
        # Third
        third_top_high_fiver_id = 0
        third_top_high_fiver_name = 'Pending'
        top_third_high_fiver_count = 0
        # Fourth
        fourth_top_high_fiver_id = 0
        fourth_top_high_fiver_name = 'Pending'
        top_fourth_high_fiver_count = 0
        # Fifth
        fifth_top_high_fiver_id = 0
        fifth_top_high_fiver_name = 'Pending'
        top_fifth_high_fiver_count = 0

        # Check if there are results
        if redord_of_top_high_fiver:
            # ** Find the First Top High Fiver User Name And Count From Query Result 
            top_first_high_fiver_user_id = redord_of_top_high_fiver[0][0]
            # # ** Browse The User Model To Get The Name Of First Top High Fiver User **
            browse_first_user_model = request.env['res.users'].browse(top_first_high_fiver_user_id)
            first_top_high_fiver_id = browse_first_user_model.id
            first_top_high_fiver_name = browse_first_user_model.name
            top_first_high_fiver_count = redord_of_top_high_fiver[0][1]

            # ** Find the Second Top High Fiver User Name And Count From Query Result 
            if len(redord_of_top_high_fiver) > 1:
                top_second_high_fiver_user_id = redord_of_top_high_fiver[1][0]
                # ** Browse The User Model To Get The Name Of Second Top High Fiver User **
                browse_second_user_model = request.env['res.users'].browse(top_second_high_fiver_user_id)
                second_top_high_fiver_id = browse_second_user_model.id
                second_top_high_fiver_name = browse_second_user_model.name
                top_second_high_fiver_count = redord_of_top_high_fiver[1][1]
            
            # ** Find the Third Top High Fiver User Name And Count From Query Result 
            if len(redord_of_top_high_fiver) > 2:
                top_third_high_fiver_user_id = redord_of_top_high_fiver[2][0]
                # ** Browse The User Model To Get The Name Of Third Top High Fiver User **
                browse_third_user_model = request.env['res.users'].browse(top_third_high_fiver_user_id)
                third_top_high_fiver_id = browse_third_user_model.id
                third_top_high_fiver_name = browse_third_user_model.name
                top_third_high_fiver_count = redord_of_top_high_fiver[2][1]
            
            # ** Find the Fourth Top High Fiver User Name And Count From Query Result 
            if len(redord_of_top_high_fiver) > 3:
                top_fourth_high_fiver_user_id = redord_of_top_high_fiver[3][0]
                # ** Browse The User Model To Get The Name Of Third Top High Fiver User **
                browse_fourth_user_model = request.env['res.users'].browse(top_fourth_high_fiver_user_id)
                fourth_top_high_fiver_id = browse_fourth_user_model.id
                fourth_top_high_fiver_name = browse_fourth_user_model.name
                top_fourth_high_fiver_count = redord_of_top_high_fiver[3][1]
            
            # ** Find the Fifth Top High Fiver User Name And Count From Query Result 
            if len(redord_of_top_high_fiver) > 4:
                top_fifth_high_fiver_user_id = redord_of_top_high_fiver[4][0]
                # ** Browse The User Model To Get The Name Of Third Top High Fiver User **
                browse_fifth_user_model = request.env['res.users'].browse(top_fifth_high_fiver_user_id)
                fifth_top_high_fiver_id = browse_fifth_user_model.id
                fifth_top_high_fiver_name = browse_fifth_user_model.name
                top_fifth_high_fiver_count = redord_of_top_high_fiver[4][1]



        # ================================================
        # # ** Find the First Top High Fiver User Name And Count From Query Result 
        # top_first_high_fiver_user_id = redord_of_top_high_fiver[0][0]
        # # # ** Browse The User Model To Get The Name Of First Top High Fiver User **
        # browse_first_user_model = request.env['res.users'].browse(top_first_high_fiver_user_id)
        # first_top_high_fiver_id = browse_first_user_model.id
        # first_top_high_fiver_name = browse_first_user_model.name
        # top_first_high_fiver_count = redord_of_top_high_fiver[0][1]
    

        #  # ** Find the Second Top High Fiver User Name And Count From Query Result 
        # second_top_high_fiver_id=0
        # second_top_high_fiver_name=False
        # top_second_high_fiver_count=0
        # if  len(redord_of_top_high_fiver) > 1:
        #     top_second_high_fiver_user_id = redord_of_top_high_fiver[1][0]
        #     # ** Browse The User Model To Get The Name Of Second Top High Fiver User **
        #     browse_second_user_model = request.env['res.users'].browse(top_second_high_fiver_user_id)
        #     second_top_high_fiver_id = browse_second_user_model.id
        #     second_top_high_fiver_name = browse_second_user_model.name
        #     top_second_high_fiver_count = redord_of_top_high_fiver[1][1]





        # ** Get The Points Of Given And Received From Setting ** 
        points_of_given_high_five = request.env.company.sh_points_for_each_given_high_five
        points_of_received_high_five = request.env.company.sh_points_for_each_received_high_five


        # ** Find The Count Of Given And Received High Five **
        # Given Counts 
        sh_given_query = f"""select count(id) from sh_high_five where sh_from_user_id = {login_user_id} and sh_parent_id is null"""
        request.env.cr.execute(sh_given_query)
        sh_high_five_given_records_count = request._cr.fetchall()[0][0]

         # Received Counts 
        sh_received_query = f"""select count(id) from sh_high_five where sh_to_user_id = {login_user_id} and sh_parent_id is null"""
        request.env.cr.execute(sh_received_query)
        sh_high_five_received_records_count = request._cr.fetchall()[0][0]
        
        # ** Calculate The Total High Five Points **
        # Calculate The Given High Five Points :- 
        total_points_of_given_high_five =  sh_high_five_given_records_count * points_of_given_high_five

        # Calculate The Received High Five Points :- 
        total_points_of_received_high_five =  sh_high_five_received_records_count * points_of_received_high_five


        # CUSTOM CODE GROUPBY
        # =====================================================
        high_five = request.env['sh.high.five']
        group_by_dict={}
        final_group_by_dict={}

        if groupBy:
            if domain:
                query = high_five._where_calc(domain)
                tables, where_clause, where_params = query.get_sql()

                first_group_by = f"""
                        SELECT {groupBy[0]}, STRING_AGG(id::TEXT, ',') as high_five_ids
                        FROM {tables}
                        WHERE sh_parent_id IS NULL AND {where_clause} 
                        GROUP BY {groupBy[0]};
                        """
                request.env.cr.execute(first_group_by,where_params)
                first_group_by_records = request._cr.fetchall()
            else:
                first_group_by = f"""
                        SELECT {groupBy[0]}, STRING_AGG(id::TEXT, ',') as high_five_ids
                        FROM sh_high_five
                        WHERE sh_parent_id IS NULL 
                        GROUP BY {groupBy[0]};
                        """
                request.env.cr.execute(first_group_by)
                first_group_by_records = request._cr.fetchall()

            
            # FIND MODEL OF GROUP BY FIELD
            model_field = request.env['ir.model.fields'].sudo().search([
                    ('model', '=', 'sh.high.five'),
                    ('name', '=', groupBy[0])
                ])

            group_by_model=model_field.relation

            for item in first_group_by_records:
                key = str(item[0])
                values = list(map(int, item[1].split(',')))
                group_by_dict[key] = values

            for groupby_field,high_five_ids_values in group_by_dict.items() :

                record_set_group_by_field=request.env[group_by_model].sudo().browse(int(groupby_field))
                group_by_key=record_set_group_by_field.name

                sh_high_five_records_group_by_list = []

                for sh_high_five_record in high_five_ids_values :
                    show_like_btn = True
                    browse_high_five_record = request.env['sh.high.five'].browse(sh_high_five_record)
                    like_count = len(browse_high_five_record.sh_liked_by_ids)
                    if login_user_id in browse_high_five_record.sh_liked_by_ids.ids:
                        show_like_btn = False
                    # ** Delete Button Restriction Code ** 
                    show_delete_button = False
                    if login_user_id == browse_high_five_record.sh_from_user_id.id:
                        show_delete_button = True 
                    high_five_item = {
                        'id' : browse_high_five_record.id,
                        'high_five_text' : browse_high_five_record.name,
                        'sh_from_user_id': browse_high_five_record.sh_from_user_id.id,
                        'sh_to_user_name': browse_high_five_record.sh_to_user_id.name,
                        'sh_from_user_name': browse_high_five_record.sh_from_user_id.name,
                        'show_like_btn': show_like_btn,
                        'show_delete_button': show_delete_button,
                        'like_count': like_count,
                        'record_creation_date' : browse_high_five_record.sh_high_five_creation_date,
                    }

                    if browse_high_five_record.sh_child_ids:
                        child_record_list=[]
                        for child in  browse_high_five_record.sh_child_ids:
                            sh_show_edit_delete_btn = False
                            sh_is_login_user_have_acs = False
                            show_child_like_btn = True
                            child_like_count = len(child.sh_liked_by_ids)
                            if login_user_id in child.sh_liked_by_ids.ids :
                                show_child_like_btn = False
                            # Make Boolean True If Login User Is Created User 
                            if login_user_id == child.sh_from_user_id.id :
                                sh_show_edit_delete_btn = True
                            # Make boolean true if private comment 
                            if child.sh_is_private_comment :
                                if login_user_id == browse_high_five_record.sh_to_user_id.id or login_user_id == child.sh_from_user_id.id:
                                    sh_is_login_user_have_acs = True
                            child_vals={
                                'id' : child.id,
                                'high_five_text' : child.name,
                                'sh_from_user_id': child.sh_from_user_id.id,
                                'sh_from_user_name': child.sh_from_user_id.name,
                                'show_child_like_btn': show_child_like_btn,
                                'child_like_count': child_like_count,
                                'child_creation_date' :  child.sh_high_five_creation_date,
                                'sh_show_edit_delete_btn' : sh_show_edit_delete_btn,
                                'sh_is_private_cmt_record' : child.sh_is_private_comment,
                                'sh_is_login_user_have_acs' : sh_is_login_user_have_acs,
                                'sh_third_mention_name' : child.sh_third_mention_id.name,
                            }
                            child_record_list.append(child_vals)

                        high_five_item.update({
                            'child_ids':child_record_list
                        })
                    sh_high_five_records_group_by_list.append(high_five_item)

                final_group_by_dict[group_by_key]=sh_high_five_records_group_by_list

        # ======================================================

        # CUSTOM CODE DOMAIN
        # =======================================================
        if domain and not groupBy:
            high_five = request.env['sh.high.five']
            query = high_five._where_calc(domain)
            tables, where_clause, where_params = query.get_sql()
            sh_high_five = f"""
                            SELECT ARRAY(select id 
                                        from {tables} where sh_parent_id is null AND
                                        {where_clause}
                            )
                            """
            request.env.cr.execute(sh_high_five,where_params)
            sh_high_five_records = request._cr.fetchall()[0][0]
        else:
            sh_high_five = f"""SELECT ARRAY(select id from sh_high_five where sh_parent_id is null)"""
            request.env.cr.execute(sh_high_five)
            sh_high_five_records = request._cr.fetchall()[0][0]

        # ========================================================

        sh_high_five_records_list = []
        for sh_high_five_record in sh_high_five_records :
            show_like_btn = True
            browse_high_five_record = request.env['sh.high.five'].browse(sh_high_five_record)
            like_count = len(browse_high_five_record.sh_liked_by_ids)
            if login_user_id in browse_high_five_record.sh_liked_by_ids.ids:
                show_like_btn = False
            # ** Delete Button Restriction Code ** 
            show_delete_button = False
            if login_user_id == browse_high_five_record.sh_from_user_id.id:
                show_delete_button = True 
            high_five_item = {
                'id' : browse_high_five_record.id,
                'high_five_text' : browse_high_five_record.name,
                'sh_from_user_id': browse_high_five_record.sh_from_user_id.id,
                'sh_to_user_name': browse_high_five_record.sh_to_user_id.name,
                'sh_from_user_name': browse_high_five_record.sh_from_user_id.name,
                'show_like_btn': show_like_btn,
                'show_delete_button': show_delete_button,
                'like_count': like_count,
                'record_creation_date' : browse_high_five_record.sh_high_five_creation_date,
            }

            if browse_high_five_record.sh_child_ids:
                child_record_list=[]
                for child in  browse_high_five_record.sh_child_ids:
                    sh_show_edit_delete_btn = False
                    sh_is_login_user_have_acs = False
                    show_child_like_btn = True
                    child_like_count = len(child.sh_liked_by_ids)
                    if login_user_id in child.sh_liked_by_ids.ids :
                        show_child_like_btn = False
                    # Make Boolean True If Login User Is Created User 
                    if login_user_id == child.sh_from_user_id.id :
                        sh_show_edit_delete_btn = True
                    # Make boolean true if private comment 
                    if child.sh_is_private_comment :
                        if login_user_id == browse_high_five_record.sh_to_user_id.id or login_user_id == child.sh_from_user_id.id:
                            sh_is_login_user_have_acs = True
                    child_vals={
                        'id' : child.id,
                        'high_five_text' : child.name,
                        'sh_from_user_id': child.sh_from_user_id.id,
                        'sh_from_user_name': child.sh_from_user_id.name,
                        'show_child_like_btn': show_child_like_btn,
                        'child_like_count': child_like_count,
                        'child_creation_date' :  child.sh_high_five_creation_date,
                        'sh_show_edit_delete_btn' : sh_show_edit_delete_btn,
                        'sh_is_private_cmt_record' : child.sh_is_private_comment,
                        'sh_is_login_user_have_acs' : sh_is_login_user_have_acs,
                        'sh_third_mention_name' : child.sh_third_mention_id.name,
                    }
                    child_record_list.append(child_vals)

                high_five_item.update({
                    'child_ids':child_record_list
                })
            sh_high_five_records_list.append(high_five_item)
        
        sum_of_given_received_high_five_points = total_points_of_given_high_five + total_points_of_received_high_five

        # ** Code For Groupby Functionality **
        # find_groupby_high_five = f"""SELECT ARRAY(select sh_high_five_creation_date from sh_high_five where sh_parent_id is null group by sh_high_five_creation_date order by sh_high_five_creation_date desc)"""

        if domain:
            high_five = request.env['sh.high.five']
            query = high_five._where_calc(domain)
            tables, where_clause, where_params = query.get_sql()

            find_groupby_high_five = f"""SELECT ARRAY(select sh_high_five_creation_date from sh_high_five where sh_parent_id is null AND {where_clause} group by sh_high_five_creation_date order by MAX(id) DESC)"""
            request.env.cr.execute(find_groupby_high_five,where_params)

        else:
            find_groupby_high_five = f"""SELECT ARRAY(select sh_high_five_creation_date from sh_high_five where sh_parent_id is null group by sh_high_five_creation_date order by MAX(id) DESC)"""
            request.env.cr.execute(find_groupby_high_five)
        group_by_high_five_list = request._cr.fetchall()[0][0]


        # Solve Sequence Issue By Sorting Dictionary With id Same As Feedback
        sorted_high_five_records = sorted(sh_high_five_records_list, key=lambda x: x['id'], reverse=True)

        # FOR GET ALL BADGES RECORD IF SEARCH MORE CLICK FROM BADGE SELECTION
        # ===================================================================
        badges=request.env['sh.manage.badge'].sudo().search([])
        badge_dict={}
        for badge in badges:
            badge_dict[badge.id]=badge.name


        response_data['all_high_five_records'] = sorted_high_five_records
        response_data['login_user_id'] = login_user_id
        response_data['login_user_name'] = login_user_name
        response_data['today_date_in_string_format'] = today_date_in_string_format
        response_data['given_high_five_count'] = sh_high_five_given_records_count
        response_data['received_high_five_count'] = sh_high_five_received_records_count
        response_data['total_points_of_given_high_five'] = total_points_of_given_high_five
        response_data['total_points_of_received_high_five'] = total_points_of_received_high_five
        response_data['sum_of_given_received_high_five_points'] = sum_of_given_received_high_five_points
        response_data['badge_all_list'] = badge_dict
        # ** Top Users Details **
        # ** First **  
        response_data['first_top_high_fiver_id'] = first_top_high_fiver_id
        response_data['first_top_high_fiver_name'] = first_top_high_fiver_name
        response_data['top_first_high_fiver_count'] = top_first_high_fiver_count
        # ** Second **  
        response_data['second_top_high_fiver_id'] = second_top_high_fiver_id
        response_data['second_top_high_fiver_name'] = second_top_high_fiver_name
        response_data['top_second_high_fiver_count'] = top_second_high_fiver_count
         # ** Third **  
        response_data['third_top_high_fiver_id'] = third_top_high_fiver_id
        response_data['third_top_high_fiver_name'] = third_top_high_fiver_name
        response_data['top_third_high_fiver_count'] = top_third_high_fiver_count
         # ** Fourth **  
        response_data['fourth_top_high_fiver_id'] = fourth_top_high_fiver_id
        response_data['fourth_top_high_fiver_name'] = fourth_top_high_fiver_name
        response_data['top_fourth_high_fiver_count'] = top_fourth_high_fiver_count
         # ** Fifth **  
        response_data['fifth_top_high_fiver_id'] = fifth_top_high_fiver_id
        response_data['fifth_top_high_fiver_name'] = fifth_top_high_fiver_name
        response_data['top_fifth_high_fiver_count'] = top_fifth_high_fiver_count
        # Group By Date Functionality 
        response_data['group_by_high_five_list'] = group_by_high_five_list

        #GROUP BY LATEST
        response_data['is_group_by_enable'] = True if groupBy else False
        response_data['final_group_by_dict'] = final_group_by_dict if final_group_by_dict else False

        return response_data
    
    @http.route(['/post/high_five/data'], type='json', auth='public', methods=['POST'])
    def postButtonController(self, high_five_text, to_user_id,sh_manage_badge_id):
        response_data = {}
        todays_date = datetime.now()

        today_date_in_string_format = todays_date.strftime("%d %B, %Y")

        high_five_vals={
                        # 'sh_from_user_id':self.sh_give_feedback_person.id,
                        'name':high_five_text,
                        'sh_from_user_id' : request.env.user.id,
                        'sh_high_five_creation_date' : today_date_in_string_format,
                        'sh_to_user_id' : int(to_user_id),
                        'sh_manage_badges_id' : int(sh_manage_badge_id),
                        'sh_high_five_create_date_search' : date.today(),
                    }
        new_test = request.env['sh.high.five'].sudo().create(high_five_vals)
        request.env['user.push.notification'].push_notification([new_test.sh_to_user_id],title="New High Five",message="You received High Five from %s"%(request.env.user.name),link="",res_model="sh.high.five",res_id=0,type='hr')
        return response_data


    @http.route(['/get/user/list'], type='json', auth='public', methods=['POST'])
    def get_users_name_list(self,search,limit):
        if search:
            users=request.env['res.users'].sudo().search([('name', 'ilike', search)],limit=limit)
        else:
            users=request.env['res.users'].sudo().search([('share', '=', False)],limit=limit)
        users_name_list=[]

        for user in users:

            user_info={
                'id':user.id,
                'name':user.name,
            }
            users_name_list.append(user_info)
        return users_name_list

    @http.route(['/get/badge/list'], type='json', auth='public', methods=['POST'])
    def get_default_badge_list(self,search,limit):
        if search:
            badges=request.env['sh.manage.badge'].sudo().search([('name', 'ilike', search),('sh_is_active','=',True)],limit=limit)
        else:
            badges=request.env['sh.manage.badge'].sudo().search([('sh_is_active','=',True)],limit=limit)
        badge_list={}
        for badge in badges:
            badge_list[badge.id]=badge.name
        return badge_list


    @http.route(['/post/high_five/comments'], type='json', auth='public', methods=['POST'])
    def post_comments(self,high_five_reply_id,high_five_reply, private_cmt_boolean_value,third_person_id):
        todays_date = datetime.now()
        today_date_in_string_format = todays_date.strftime("%d %B, %Y")
        high_five_vals={
                        'name':high_five_reply,
                        'sh_from_user_id' : request.env.user.id,
                        'sh_parent_id' : high_five_reply_id,
                        'sh_high_five_creation_date' : today_date_in_string_format,
                        'sh_is_private_comment':private_cmt_boolean_value,
                        'sh_third_mention_id':third_person_id if third_person_id else False,
                    }
        request.env['sh.high.five'].sudo().create(high_five_vals)

        # notification on comment highfive
        # ================================
        main_high_five_reply_id=request.env['sh.high.five'].sudo().browse(high_five_reply_id)

        if main_high_five_reply_id.sh_from_user_id:
            request.env['user.push.notification'].push_notification([main_high_five_reply_id.sh_from_user_id],title="Comment High Five",message="%s commented on your High Five"%(request.env.user.name),link="",res_model="sh.high.five",res_id=0,type='hr')
        if main_high_five_reply_id.sh_to_user_id:
            request.env['user.push.notification'].push_notification([main_high_five_reply_id.sh_to_user_id],title="Comment High Five",message="%s commented on your High Five"%(request.env.user.name),link="",res_model="sh.high.five",res_id=0,type='hr')
        if third_person_id:
            mentioned_user=request.env['res.users'].sudo().browse(int(third_person_id))
            if mentioned_user:
                request.env['user.push.notification'].push_notification([mentioned_user],title="Mention High Five",message="%s mentioned you in High Five"%(request.env.user.name),link="",res_model="sh.high.five",res_id=0,type="hr")

    # ==============================
    # *** PARENT CONTROLLERS ***  
    # ==============================
    @http.route(['/post/like_btn/data'], type='json', auth='public', methods=['POST'])
    def update_like_button(self,record_id):
        responce_data = []
        like_record = request.env['sh.high.five'].sudo().search([('id', '=', record_id)])
        like_record.write({
        'sh_liked_by_ids': [(4, request.env.user.id)]  # Add the employee to the Many2many field
        })

        # notification on like highfive
        # =============================
        if like_record and like_record.sh_from_user_id:
            request.env['user.push.notification'].push_notification([like_record.sh_from_user_id],title="Like High Five",message="%s liked your High Five"%(request.env.user.name),link="",res_model="sh.high.five",res_id=0,type="hr")
        if like_record and like_record.sh_to_user_id:
            request.env['user.push.notification'].push_notification([like_record.sh_to_user_id],title="Like High Five",message="%s liked your High Five"%(request.env.user.name),link="",res_model="sh.high.five",res_id=0,type="hr")
        return responce_data
    

    @http.route(['/post/unlike_btn/data'], type='json', auth='public', methods=['POST'])
    def update_unlike_button(self,record_id):
        responce_data = []
        like_record = request.env['sh.high.five'].sudo().search([('id', '=', record_id)])
        like_record.write({
        'sh_liked_by_ids': [(3, request.env.user.id)]  # Add the employee to the Many2many field
    })
        return responce_data
    
    @http.route(['/post/delete_btn/data'], type='json', auth='public', methods=['POST'])
    def delete_button_method(self,record_id):
        responce_data = []
        delete_record = request.env['sh.high.five'].sudo().search([('id', '=', record_id)])
        browse_delete_record = request.env['sh.high.five'].sudo().browse(record_id)
        if browse_delete_record.sh_child_ids:
            for child_record in browse_delete_record.sh_child_ids :
                child_record.unlink()
        delete_record.unlink()
        return responce_data
    
    # ==============================
    # *** CHILD CONTROLLERS ***  
    # ==============================
    @http.route(['/post/like/child/data'], type='json', auth='public', methods=['POST'])
    def like_child_record(self,record_id):
        responce_data = []
        like_record = request.env['sh.high.five'].sudo().search([('id', '=', record_id)])
        like_record.write({
        'sh_liked_by_ids': [(4, request.env.user.id)]  # Add the employee to the Many2many field
    })
        
        # notification on like highfive
        # =============================
        if like_record and like_record.sh_from_user_id:
            request.env['sh.br.engage.push.notification'].create_br_engage_push_notification(user=like_record.sh_from_user_id,name="Like High Five",description="%s liked your High Five"%(request.env.user.name),res_model="sh.high.five",res_id=0)
        if like_record and like_record.sh_to_user_id:
            request.env['sh.br.engage.push.notification'].create_br_engage_push_notification(user=like_record.sh_to_user_id,name="Like High Five",description="%s liked your High Five"%(request.env.user.name),res_model="sh.high.five",res_id=0)

        return responce_data
    

    @http.route(['/post/unlike/child/data'], type='json', auth='public', methods=['POST'])
    def unlike_child_record(self,record_id):
        responce_data = []
        like_record = request.env['sh.high.five'].sudo().search([('id', '=', record_id)])
        like_record.write({
        'sh_liked_by_ids': [(3, request.env.user.id)]  # Add the employee to the Many2many field
    })
        return responce_data
    
    @http.route(['/post/delete/child/data'], type='json', auth='public', methods=['POST'])
    def delete_child_record_details(self,record_id):
        responce_data = []
        delete_record = request.env['sh.high.five'].sudo().search([('id', '=', record_id)])       
        delete_record.unlink()
        return responce_data
    

    @http.route(['/edit/child/high_five/post'], type='json', auth='public', methods=['POST'])
    def edit_child_high_five(self,record_id, record_value):
        responce_data = []
        browse_child_record = request.env['sh.high.five'].browse(record_id)
        browse_child_record.write({'name': record_value})
        return responce_data