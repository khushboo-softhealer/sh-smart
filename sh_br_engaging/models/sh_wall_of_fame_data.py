# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models,api
from datetime import datetime, timedelta


class WallOfFameDataUpdate(models.Model):
    _name = "sh.update.wall.of.fame.data"
    _description = "Model Usage To Store The Wall Of Fame Data"


    sh_wall_of_fame_user_id = fields.Many2one('res.users', "Wall Of Fame User")
    sh_employee_post_selection = fields.Selection([
            ('sh_first_post', 'At First Position'),
            ('sh_second_post', 'At Second Position'),
            ('sh_third_post', 'At Third Position'),
        ],string='Post Of Employee')
    sh_first_post_employee_badge = fields.Many2one("sh.manage.badge", string="Manage Badges")
    sh_date_of_update = fields.Char("Date Of Record Update")

    # =============================================================================
    # CRONE JOB METHOD
    # =============================================================================
    


    def update_wall_of_fame_data(self):
        # =================================================================================================================================
        # ========================================================
        # LOGIC TO UPDATE THE WALL OF FAME DATA AT MONTHLY BASIS 
        # ========================================================
        current_date = datetime.now()
    
        # Set the day to 1 for the current date to get the first date of the current month
        first_date_of_current_month = current_date.replace(day=1)

        # Subtract one day from the first date of the current month to get the last date of the previous month
        last_date_of_last_month = first_date_of_current_month - timedelta(days=1)

        # Format last_date_of_last_month as string for SQL query
        last_date_str = last_date_of_last_month.strftime("%Y-%m-%d 00:00:00")

        # Calculate the first day of the previous month
        first_date_of_last_month = last_date_of_last_month.replace(day=1)

        # Format first_date_of_last_month as string for SQL query
        first_date_str = first_date_of_last_month.strftime("%Y-%m-%d 00:00:00")


        # ========================================================
        # LOGIC TO UPDATE THE WALL OF FAME DATA AT MONTHLY BASIS 
        # ========================================================
        # =================================================================================================================================

        # GET THE DATA UPDATE DATE FROM RES SETTINGS 
        company = self.env.company
        sh_wall_of_fame_record_update_date = company.sh_wall_of_fame_record_update_date
        # GET THE TODAY'S DATE
        todays_date = datetime.now().date()
        today_date_in_string_format = todays_date.strftime("%d %B, %Y")
        # Calculate the first date of the next month
        first_day_next_month = (todays_date.replace(day=1) + timedelta(days=32)).replace(day=1)

        # ==============================================================================================================================
        # ** FIRST WALL OF FAME EMPLOYEE **
        # ==============================================================================================================================

        current_model_first_post_record = self.env['sh.update.wall.of.fame.data'].sudo().search([('sh_employee_post_selection','=','sh_first_post')])
        if current_model_first_post_record :
            # ** CHECK IF TODAY'S DATE IS MATCHED WITH RES SETTINGS DATE ** 
            if todays_date == sh_wall_of_fame_record_update_date :
                # =============================================================================================
                # WE FOUND THE RECORD OF FIRST POST SELECTION SO WE PERFORM WRITE METHOD AND UPDATE THAT RECORD
                # === Custom Query To Find Top Given And Received Both High Five Records ===  
                # =============================================================================================
                # top_given_received_counts = f""" SELECT sh_to_user_id, sh_manage_badges_id,
                #                                 COUNT(sh_manage_badges_id) AS received_count FROM 
                #                                 sh_high_five GROUP BY sh_to_user_id, sh_manage_badges_id
                #                                 ORDER BY received_count DESC LIMIT 1 """ 
                
                top_given_received_counts = f"""SELECT sh_to_user_id, sh_manage_badges_id,
                                                COUNT(sh_manage_badges_id) AS received_count FROM 
                                                sh_high_five where create_date >= '{first_date_str}' 
                                                AND create_date <= '{last_date_str}' GROUP BY sh_to_user_id, sh_manage_badges_id
                                                ORDER BY received_count DESC LIMIT 1 """ 
                self.env.cr.execute(top_given_received_counts)
                wall_of_fame_first_emp_records = self._cr.fetchall()
                # === IF WE GET RESULT IN OUR QUERY SO THEN EITHER WE ADD VALUE IN VALS OR WE CAN NOT ADD VALUE IN EMPLOYEE FIELD FOR PENDING ===
                if wall_of_fame_first_emp_records :
                    current_model_vals={
                        'sh_wall_of_fame_user_id': wall_of_fame_first_emp_records[0][0],
                        'sh_employee_post_selection' : 'sh_first_post',
                        'sh_first_post_employee_badge' : wall_of_fame_first_emp_records[0][1],
                        'sh_date_of_update' : today_date_in_string_format,
                    }
                else :
                    current_model_vals={
                        'sh_employee_post_selection' : 'sh_first_post',
                        'sh_date_of_update' : today_date_in_string_format,
                    }
                current_model_first_post_record.write(current_model_vals)
                # UPDATE THE DATE IN RES SETTING FIELD
                # =================================================================
                company.sh_wall_of_fame_record_update_date = first_day_next_month 
                # =================================================================
        else :
            # ================================================================================
            # WE CAN NOT FIND ANY RECORD SO WE CREATE NEW RECORD WITH FIRST POST SELECTION
            # === Custom Query To Find Top Given And Received Both High Five Records ===  
            # ================================================================================

            # top_given_received_counts = f""" SELECT sh_to_user_id, sh_manage_badges_id,
            #                                 COUNT(sh_manage_badges_id) AS received_count FROM 
            #                                 sh_high_five GROUP BY sh_to_user_id, sh_manage_badges_id
            #                                 ORDER BY received_count DESC LIMIT 1 """ 
                
            top_given_received_counts = f"""SELECT sh_to_user_id, sh_manage_badges_id,
                                            COUNT(sh_manage_badges_id) AS received_count FROM 
                                            sh_high_five where create_date >= '{first_date_str}' 
                                            AND create_date <= '{last_date_str}' GROUP BY sh_to_user_id, sh_manage_badges_id
                                            ORDER BY received_count DESC LIMIT 1 """ 
            self.env.cr.execute(top_given_received_counts)
            wall_of_fame_first_emp_records = self._cr.fetchall()
            # === IF WE GET RESULT IN OUR QUERY SO THEN EITHER WE ADD VALUE IN VALS OR WE CAN NOT ADD VALUE IN EMPLOYEE FIELD FOR PENDING ===
            if wall_of_fame_first_emp_records : 
                current_model_vals={
                    'sh_wall_of_fame_user_id': wall_of_fame_first_emp_records[0][0],
                    'sh_employee_post_selection' : 'sh_first_post',
                    'sh_first_post_employee_badge' : wall_of_fame_first_emp_records[0][1],
                    'sh_date_of_update' : today_date_in_string_format,
                }
            else :
                current_model_vals={
                    'sh_employee_post_selection' : 'sh_first_post',
                    'sh_date_of_update' : today_date_in_string_format,
                }
            self.env['sh.update.wall.of.fame.data'].create(current_model_vals)
            # UPDATE THE DATE IN RES SETTING FIELD
            # =================================================================
            company.sh_wall_of_fame_record_update_date = first_day_next_month 
            # =================================================================
        
        # ==============================================================================================================================
        # ** SECOND WALL OF FAME EMPLOYEE **
        # ==============================================================================================================================

        current_model_second_post_record = self.env['sh.update.wall.of.fame.data'].sudo().search([('sh_employee_post_selection','=','sh_second_post')])
        if current_model_second_post_record : 
            # ** CHECK IF TODAY'S DATE IS MATCHED WITH RES SETTINGS DATE ** 
            if todays_date == sh_wall_of_fame_record_update_date :
                # =============================================================================================
                # WE FOUND THE RECORD OF SECOND POST SELECTION SO WE PERFORM WRITE METHOD AND UPDATE THAT RECORD
                # === Custom Query To Find Top Received FEEDBACK Records ===  
                # =============================================================================================
                # === QUERY TO FIND THE FEEDBACK TOP EMPLOYEE === 
                # top_second_wall_of_fame_query = f""" SELECT sh_realtime_feedback_person, COUNT(id) 
                #                                     AS received_count FROM sh_realtime_feedback where 
                #                                     sh_feedback_type='give_feedback' GROUP BY  
                #                                     sh_realtime_feedback_person ORDER BY received_count DESC LIMIT 1 """ 
                

                top_second_wall_of_fame_query = f"""SELECT sh_realtime_feedback_person, COUNT(id) AS received_count FROM sh_realtime_feedback 
                                                    WHERE sh_feedback_type = 'give_feedback' 
                                                    AND create_date >= '{first_date_str}' 
                                                    AND create_date <= '{last_date_str}'
                                                    GROUP BY sh_realtime_feedback_person 
                                                    ORDER BY received_count DESC 
                                                    LIMIT 1
                                                """
                
                self.env.cr.execute(top_second_wall_of_fame_query)
                second_wall_of_fame_employee_query_result = self._cr.fetchall() 


                # === IF WE GET RESULT IN OUR QUERY SO THEN EITHER WE ADD VALUE IN VALS OR WE CAN NOT ADD VALUE IN EMPLOYEE FIELD FOR PENDING ===
                if second_wall_of_fame_employee_query_result : 
                    current_model_second_post_vals={
                        'sh_wall_of_fame_user_id': second_wall_of_fame_employee_query_result[0][0],
                        'sh_employee_post_selection' : 'sh_second_post',
                        'sh_date_of_update' : today_date_in_string_format,
                    }
                else :
                    current_model_second_post_vals={
                        'sh_employee_post_selection' : 'sh_second_post',
                        'sh_date_of_update' : today_date_in_string_format,
                    }
                current_model_second_post_record.write(current_model_second_post_vals)
                # UPDATE THE DATE IN RES SETTING FIELD
                # =================================================================
                company.sh_wall_of_fame_record_update_date = first_day_next_month 
                # =================================================================
        else :
            # ================================================================================
            # WE CAN NOT FIND ANY RECORD SO WE CREATE NEW RECORD WITH SECOND POST SELECTION
            # === Custom Query To Find Top Received FEEDBACK Records ===  
            # ================================================================================

            # top_second_wall_of_fame_query = f""" SELECT sh_realtime_feedback_person, COUNT(id) 
            #                                     AS received_count FROM sh_realtime_feedback where 
            #                                     sh_feedback_type='give_feedback' GROUP BY  
            #                                     sh_realtime_feedback_person ORDER BY received_count DESC LIMIT 1 """ 

            top_second_wall_of_fame_query = f"""SELECT sh_realtime_feedback_person, COUNT(id) AS received_count FROM sh_realtime_feedback 
                                                    WHERE sh_feedback_type = 'give_feedback' 
                                                    AND create_date >= '{first_date_str}' 
                                                    AND create_date <= '{last_date_str}'
                                                    GROUP BY sh_realtime_feedback_person 
                                                    ORDER BY received_count DESC 
                                                    LIMIT 1
                                                """
            
            self.env.cr.execute(top_second_wall_of_fame_query)
            second_wall_of_fame_employee_query_result = self._cr.fetchall() 
            # === IF WE GET RESULT IN OUR QUERY SO THEN EITHER WE ADD VALUE IN VALS OR WE CAN NOT ADD VALUE IN EMPLOYEE FIELD FOR PENDING ===
            if second_wall_of_fame_employee_query_result : 
                current_model_second_post_vals={
                    'sh_wall_of_fame_user_id': second_wall_of_fame_employee_query_result[0][0],
                    'sh_employee_post_selection' : 'sh_second_post',
                    'sh_date_of_update' : today_date_in_string_format,
                }
            else :
                current_model_second_post_vals={
                    'sh_employee_post_selection' : 'sh_second_post',
                    'sh_date_of_update' : today_date_in_string_format,
                }
            self.env['sh.update.wall.of.fame.data'].create(current_model_second_post_vals)
            # UPDATE THE DATE IN RES SETTING FIELD
            # =================================================================
            company.sh_wall_of_fame_record_update_date = first_day_next_month 
            # =================================================================
        # ==============================================================================================================================
        # ** THIRD WALL OF FAME EMPLOYEE **
        # ==============================================================================================================================
        current_model_third_post_record = self.env['sh.update.wall.of.fame.data'].sudo().search([('sh_employee_post_selection','=','sh_third_post')])
        hr_selected_employee = self.env.company.sh_wall_of_fame_employee
        if current_model_third_post_record :
            # ** CHECK IF TODAY'S DATE IS MATCHED WITH RES SETTINGS DATE ** 
            if todays_date == sh_wall_of_fame_record_update_date :
                if hr_selected_employee :
                    current_model_third_post_vals = {
                        'sh_wall_of_fame_user_id' : hr_selected_employee.id,
                        'sh_employee_post_selection' : 'sh_third_post',
                        'sh_date_of_update' : today_date_in_string_format,
                    }
                else :
                    current_model_third_post_vals = {
                        'sh_employee_post_selection' : 'sh_third_post',
                        'sh_date_of_update' : today_date_in_string_format,
                    }
                
                current_model_third_post_record.write(current_model_third_post_vals)
                # UPDATE THE DATE IN RES SETTING FIELD
                # =================================================================
                company.sh_wall_of_fame_record_update_date = first_day_next_month 
                # =================================================================
        else :
            if hr_selected_employee :
                current_model_third_post_vals = {
                    'sh_wall_of_fame_user_id' : hr_selected_employee.id,
                    'sh_employee_post_selection' : 'sh_third_post',
                    'sh_date_of_update' : today_date_in_string_format,
                }
            else :
                current_model_third_post_vals = {
                    'sh_employee_post_selection' : 'sh_third_post',
                    'sh_date_of_update' : today_date_in_string_format,
                }
            
            self.env['sh.update.wall.of.fame.data'].create(current_model_third_post_vals)
            # UPDATE THE DATE IN RES SETTING FIELD
            # =================================================================
            company.sh_wall_of_fame_record_update_date = first_day_next_month 
            # =================================================================
        