from odoo.http import request
from odoo import http

#----------------------------------------------------------
# Odoo Web Controllers
#----------------------------------------------------------
class TalkingPoints(http.Controller):

    @http.route(['/get/talking_point/data'], type='json', auth='public', methods=['POST'])
    def get_talking_points_data(self, res_id):
        browse_active_talking_point = request.env['sh.talking.points'].sudo().browse(res_id)
        response_data = {}
        
        list_of_agenda_dict=[]
        for record in browse_active_talking_point.sh_manage_agenda_line:
            listed_agenda_dict = {
                'id' : record.id,
                'name' : record.sh_agenda_id.name,
                'checked' : record.sh_checked,
                'description' : record.sh_talking_point_description,
                }
            list_of_agenda_dict.append(listed_agenda_dict)

        takling_point_employee_name=False
        if browse_active_talking_point.sudo().sh_employee_id:

            related_partners=[]
            if request.env.user.partner_id:
                if request.env.user.partner_id not in related_partners:
                    related_partners.append(request.env.user.partner_id.id) 

            if browse_active_talking_point.sudo().sh_employee_id.user_id:
                if browse_active_talking_point.sudo().sh_employee_id.user_id.partner_id not in related_partners:
                    related_partners.append(browse_active_talking_point.sudo().sh_employee_id.user_id.partner_id.id) 
            
            if browse_active_talking_point.sudo().sh_user_id:
                if browse_active_talking_point.sudo().sh_user_id.partner_id not in related_partners:
                    related_partners.append(browse_active_talking_point.sudo().sh_user_id.partner_id.id) 


            takling_point_employee_name={
                'employee_name':browse_active_talking_point.sudo().sh_employee_id.name,
                'related_partner_ids':related_partners,
                'employee_user_id' : browse_active_talking_point.sudo().sh_employee_id.sudo().user_id.id,
                'one_on_one_user_name' : browse_active_talking_point.sudo().sh_user_id.name if browse_active_talking_point.sudo().sh_user_id else '',
            }

        # for checking is there any schedule meeeting of this talking point or not
        even_id=False
        if res_id:
            event_check = f"""SELECT ARRAY(SELECT id FROM calendar_event WHERE sh_talking_point_id={res_id})"""
            request.env.cr.execute(event_check)
            responce = request._cr.fetchall()[0][0]
            if responce:
                even_id=True


        # for taking data of answers of shared notes and private notes
        answers_value_dict={}
        if browse_active_talking_point:

            is_employee_user=False
            is_created_user=False
            if browse_active_talking_point.sudo().sh_employee_id and browse_active_talking_point.sudo().sh_employee_id.sudo().user_id.id==request.env.user.id:
                is_employee_user=True

            if browse_active_talking_point.sudo().sh_user_id.id==request.env.user.id:
                is_created_user=True

            answers_value_dict={
                'your_notes':browse_active_talking_point.sh_your_notes,
                'employee_notes':browse_active_talking_point.sh_employee_notes,
                'private_notes':browse_active_talking_point.sh_your_private_notes,
                'user_notes':browse_active_talking_point.sh_user_private_notes,
                'is_employee_user':is_employee_user,
                'is_created_user':is_created_user,
            }


        # NEW
        previous_talking_points_value_list=[]
        if browse_active_talking_point and browse_active_talking_point.sudo().child_ids:
            for child in browse_active_talking_point.sudo().child_ids:
                previous_record_dict={
                            'id':child.id,
                            'sh_your_notes':child.sh_your_notes,
                            'sh_employee_notes':child.sh_employee_notes,
                            'sh_your_private_notes':child.sh_your_private_notes,
                            'sh_user_private_notes':child.sh_user_private_notes,
                            'sh_calender_event_id':child.sh_calender_event_id.name,
                        }
                previous_talking_points_value_list.append(previous_record_dict)


        # for taking data of scheduled event and previos event
        current_scheduled_event={}
        if browse_active_talking_point and browse_active_talking_point.sh_calender_event_id:
            current_scheduled_event['id']= browse_active_talking_point.sh_calender_event_id.id
            current_scheduled_event['name']= browse_active_talking_point.sh_calender_event_id.name
            current_scheduled_event['meeting_date']= browse_active_talking_point.sh_calender_event_id.start.strftime("%d %B, %Y")

        previous_scheduled_event_list=[]

        if res_id:
            previous_events = f"""SELECT ARRAY(SELECT id FROM calendar_event WHERE sh_talking_point_id={res_id})"""
            request.env.cr.execute(previous_events)
            responce = request._cr.fetchall()[0][0]

            if responce and browse_active_talking_point and browse_active_talking_point.sh_calender_event_id and browse_active_talking_point.sh_calender_event_id.id in responce:
                if browse_active_talking_point.sh_calender_event_id.id in responce:
                    responce.remove(browse_active_talking_point.sh_calender_event_id.id)

            if responce:
                browse_previous_events = request.env['calendar.event'].sudo().browse(responce)
                for event in browse_previous_events:
                    previous_events_dict={
                        'id':event.id,
                        'name':event.name,
                        'meeting_date_previous':event.start.strftime("%d %B, %Y")
                    }
                    previous_scheduled_event_list.append(previous_events_dict)

        # for previour meetings order in id desc
        if previous_scheduled_event_list:
            previous_scheduled_event_list = sorted(previous_scheduled_event_list, key=lambda x: x['id'], reverse=True)


        is_submitted=False
        if browse_active_talking_point.sh_stage=='completed':
            is_submitted=True

        # IF AUTO CREATE 1ON1 AND USER IS MANAGER THEN SHOW END 1ON1 BUTTON ONLY
        # ======================================================================
        allow_to_end_one_on_one = False
        if not browse_active_talking_point.is_auto_create and browse_active_talking_point.sh_user_id and browse_active_talking_point.sh_user_id.id==request.env.user.id:
            allow_to_end_one_on_one=True
        if browse_active_talking_point.is_auto_create and request.env.user.has_group('sh_br_engaging.group_br_engage_manager'):
            allow_to_end_one_on_one=True

        date_information={
            'start_date': browse_active_talking_point.sh_create_date.strftime("%d %b, %Y"),
            'due_date': browse_active_talking_point.sh_create_date.strftime("%A, %B %d")
        }

        is_allow_delete_meeting_agenda=False
        if browse_active_talking_point.sh_user_id and browse_active_talking_point.sh_user_id.id==request.env.user.id:
            is_allow_delete_meeting_agenda=True


        response_data['even_id']=even_id
        response_data['list_of_agenda_dict']=list_of_agenda_dict
        response_data['takling_point_employee_name']=takling_point_employee_name
        response_data['answers_value_dict']=answers_value_dict
        response_data['previous_talking_points_value_dict']=previous_talking_points_value_list if previous_talking_points_value_list else False
        response_data['current_scheduled_event']=current_scheduled_event if current_scheduled_event else False
        response_data['previous_scheduled_event_list']=previous_scheduled_event_list if previous_scheduled_event_list else False
        response_data['is_submitted']=is_submitted
        response_data['allow_to_end_one_on_one']=allow_to_end_one_on_one
        response_data['date_information']=date_information
        response_data['is_allow_delete_meeting_agenda']=is_allow_delete_meeting_agenda

        return response_data


    @http.route(['/end/1-on-1s',], type='json', auth='public', methods=['POST'])
    def end_one_on_ones(self, res_id, checked_agenda_records,talking_point_answers,is_submitted):

        talking_point_id = request.env['sh.talking.points'].browse(res_id)

        # for update checked values of agenda

        # checked_agenda_records = [int(element) for element in checked_agenda_records]
        # talking_point_lines = request.env['sh.talking.agenda.line'].browse(checked_agenda_records)
        # for agenda_line in talking_point_lines:
        #     agenda_line.sh_checked=True

        for agenda_record in checked_agenda_records:
            agenda_id = int(agenda_record['id'])
            checked_value = agenda_record['checked']
            description_value = agenda_record['description']
            agenda_line = request.env['sh.talking.agenda.line'].browse(agenda_id)
            agenda_line.sh_checked = checked_value
            agenda_line.sh_talking_point_description = description_value


        # for update answers of talking points

        if talking_point_answers:
            if talking_point_id:

                if 'your_notes' in talking_point_answers:
                    talking_point_id.sh_your_notes=talking_point_answers.get('your_notes')

                # if talking_point_answers[0]:
                #     talking_point_id.sh_your_notes=talking_point_answers[0]
                    
                if 'employee_notes' in talking_point_answers:
                    talking_point_id.sh_employee_notes=talking_point_answers.get('employee_notes')
                    
                # if talking_point_answers[1]:
                #     talking_point_id.sh_employee_notes=talking_point_answers[1]

                if 'private_note' in talking_point_answers:
                    talking_point_id.sh_your_private_notes=talking_point_answers.get('private_note')


                if 'user_note' in talking_point_answers:
                    talking_point_id.sh_user_private_notes=talking_point_answers.get('user_note')


                # if len(talking_point_answers)==3 and talking_point_answers[2]:
                #     talking_point_id.sh_your_private_notes=talking_point_answers[2]
                    
                # if len(talking_point_answers)>2 and talking_point_answers[2]:
                #     talking_point_id.sh_your_private_notes=talking_point_answers[2]

                # if len(talking_point_answers)>3 and talking_point_answers[3]:
                #     talking_point_id.sh_user_private_notes=talking_point_answers[3]

        # for update talking point stage
        if is_submitted:
            talking_point_id.write({
                'sh_stage':'completed'
            })


        # for rec in checked_agenda_records:

        # question_data = f"""SELECT ARRAY(SELECT id FROM sh_talking_points WHERE id in {checked_agenda_record_tuple})"""
        # request.env.cr.execute(question_data)
        # responce = request._cr.fetchall()[0][0]

    @http.route(['/post/delete_agenda/record',], type='json', auth='public', methods=['POST'])
    def delete_agenda_lines(self, res_id):
        responce_list = []
        browse_agenda_record = request.env['sh.talking.agenda.line'].sudo().search([('id', '=', res_id)])
        browse_agenda_record.unlink()
        return responce_list
