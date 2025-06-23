# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import _, api, fields, models, SUPERUSER_ID
import logging
import time
from datetime import datetime, timedelta
import odoo
from pytz import timezone,UTC,utc

_logger = logging.getLogger(__name__)


class ShIrCrone(models.Model):
    _inherit = 'ir.cron'

    def _callback(self, cron_name, server_action_id, job_id):
        # override the _callback method of standard
        cron_success = False
        start_time = False
        end_time = False
        failure_reason = False

        try:
            if self.pool != self.pool.check_signaling():
                self.env.reset()
                self = self.env()[self._name]

            log_depth = (None if _logger.isEnabledFor(logging.DEBUG) else 1)
            odoo.netsvc.log(_logger, logging.DEBUG, 'cron.object.execute', (self._cr.dbname, self._uid, '*', cron_name, server_action_id), depth=log_depth)
            _logger.info('Starting job `%s`.', cron_name)
            if _logger.isEnabledFor(logging.DEBUG):
                start_time = time.time()
            self.env['ir.actions.server'].browse(server_action_id).run()
            self.env.flush_all()
            _logger.info('Job `%s` done.', cron_name)
            if start_time and _logger.isEnabledFor(logging.DEBUG):
                end_time = time.time()
                _logger.debug('%.3fs (cron %s, server action %d with uid %d)', end_time - start_time, cron_name, server_action_id, self.env.uid)
            self.pool.signal_changes()
            cron_success = True
        except Exception as e:
            self.pool.reset_changes()
            _logger.exception("Call from cron %s for server action #%s failed in Job #%s",
                              cron_name, server_action_id, job_id)
            self._handle_callback_exception(cron_name, server_action_id, job_id, e)
            cron_success = False
            failure_reason = e
        
        finally:
            try:
                time = fields.Datetime.now()

                admin = self.env.ref("base.user_admin")
                local_tz = timezone(admin.tz)
                time = time.astimezone(local_tz)

                time = time.strftime('%d-%m-%Y %I:%M:%S')
          
                job_id = self.env['ir.cron'].sudo().browse(job_id)

                if cron_success:
                    message= f'The scheduled cron job "{cron_name}" was successfully executed at {time}.'
                    job_id.message_post(body=message)
                else:
                    message = f'The scheduled cron job "{cron_name}" failed during execution at {time}.Failure Reason : {failure_reason}.'
                    # job_id.sudo().activity_schedule(
                    #     'mail.mail_activity_data_email',
                    #     note = message,
                    #     user_id = admin.id)
                    
                    self.env['sh.cron.failure'].sudo().create({'name':cron_name,
                                                                'failure_time':time,
                                                                'failure_reason':failure_reason,
                                                                'cron':job_id.id})

            except Exception as e:
                job_id = self.env['ir.cron'].sudo().browse(job_id)
                message = f'The scheduled cron job "{cron_name}" failed due to Custom Code during execution at {time}. Failure Reason : {e}.'
                # job_id.sudo().activity_schedule(
                #         'mail.mail_activity_data_email',
                #         note = message,
                #         user_id = self.env.ref("base.user_admin").id)
                self.env['sh.cron.failure'].sudo().create({'name':cron_name,
                                                                'failure_time':time,
                                                                'failure_reason':message,
                                                                'cron':job_id.id})