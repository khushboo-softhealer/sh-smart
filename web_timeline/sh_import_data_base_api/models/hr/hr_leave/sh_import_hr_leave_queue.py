# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields
import requests


class HeLeaveToQueue(models.Model):
    _inherit = "sh.import.base"

    sh_hr_leave_ids_list = fields.Char("Leave ids")
    sh_is_import_hr_leave_in_queue = fields.Boolean("Import Hr Leave to Queue")
    sh_from_date_hr_leave = fields.Datetime("From Date(Time Off)")
    sh_to_date_hr_leave = fields.Datetime("To Date(Time Off)")

    def import_hr_leave_to_queue(self):
        ''' ========== Import He Leave between from date and end date ==================  '''
        base_obj = self.env['sh.import.base'].search([], limit=1)
        if base_obj.sh_is_import_hr_leave_in_queue:
            response = requests.get('''%s/api/public/hr.leave?query={id,write_date}&filter=[["write_date",">=","%s"],["write_date","<=","%s"]]''' % (
                base_obj.base_url, str(base_obj.sh_from_date_hr_leave), str(base_obj.sh_to_date_hr_leave)))
            if response.status_code == 200:
                response_json = response.json()
                if response_json.get('result'):
                    base_obj.sh_hr_leave_ids_list = [
                        r['id'] for r in response_json.get('result')]

    def import_hr_leave_from_queue(self):
        ''' ========== Import Hr Leave From Queue ==================  '''
        base_obj = self.env['sh.import.base'].search([], limit=1)

        if base_obj.sh_is_import_hr_leave_in_queue and base_obj.sh_hr_leave_ids_list:
            hr_leaves_list = base_obj.sh_hr_leave_ids_list.strip('][').split(', ')

            if not hr_leaves_list[0]:
                base_obj.sh_is_import_hr_leave_in_queue = False
                base_obj.sh_hr_leave_ids_list = False
                return False

            count = 0
            failed = 0
            for leave_id in hr_leaves_list[0:20]:
                response = requests.get('''%s/api/public/hr.leave/%s?query={%s}''' % (
                    base_obj.base_url, leave_id, self.query['hr_leave']))
                response_json = response.json()
                for leave in response_json['result']:
                    if leave.get('id') in [3740,3791,3789,3717,3714,3713,3709,3422]:
                        continue
                    # try:
                    if not leave.get('id'):
                        continue
                    if not base_obj.is_leave_can_be_create(leave):
                        failed += 1
                        continue
                    domain = [('remote_leave_id', '=', leave['id'])]
                    find_leave = self.env['hr.leave'].search(domain)
                    leave_vals = self.process_hr_leave_vals(leave)
                    if not leave_vals:
                        failed += 1
                        continue
                    if find_leave:
                        count +=1
                        find_leave.write(leave_vals)
                        # if find_leave.state in ('confirm', 'validate'):
                        #     find_leave.action_refuse()
                        # if leave_vals.get('employee_id'):
                        #     # To prevent error from
                        #     # employee_ids += vals['employee_id']
                        #     if leave_vals.get('employee_id') in find_leave.employee_id.ids:
                        #         del leave_vals['employee_id']
                        # find_leave.write(leave_vals)
                    else:
                        try:
                            find_leave = self.env['hr.leave'].create(
                                leave_vals)
                        except ValueError:
                            if 'request_hour_from' in leave_vals:
                                del leave_vals['request_hour_from']
                            if 'request_hour_to' in leave_vals:
                                del leave_vals['request_hour_to']
                            find_leave = self.env['hr.leave'].create(
                                leave_vals)
                            
                        except Exception as e:
                            failed += 1
                            self.create_fail_log(
                                name=leave.get('id'),
                                field_type='hr_leave',
                                error=e,
                                import_json=leave,
                            )
                                 
                        
                    find_leave.write(
                        {'state': leave['state']['sh_api_current_state']})
                    count += 1

                    # except Exception as e:
                    #     failed += 1
                    #     self.create_fail_log(
                    #         name=leave.get('id'),
                    #         field_type='hr_leave',
                    #         error=e,
                    #         import_json=leave,
                    #     )

            if count > 0:
                self.create_log(field_type='hr_leave', error="%s Hr Leave Imported Successfully" % (
                    count), state='success')
            if failed > 0:
                # self.create_fail_log(
                #     name=leave.get('id'),
                #     field_type='hr_leave',
                #     error=e,
                #     import_json=leave,
                # )
                self.create_log(field_type='hr_leave',
                                error='%s Hr Leave Failed to import.' % (failed))

            base_obj.sh_hr_leave_ids_list = '['+', '.join(
                [str(elem) for elem in hr_leaves_list[20:]])+']'
