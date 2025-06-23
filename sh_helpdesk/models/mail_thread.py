# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models,api,_
import sys
import smtplib
import logging
_test_logger = logging.getLogger('odoo.tests')
_logger = logging.getLogger(__name__)
def _print_debug(self, *args):
    _logger.debug(' '.join(str(a) for a in args))
smtplib.SMTP._print_debug = _print_debug
from odoo.tools import ustr


import logging
import psycopg2
import smtplib
import base64
import re
from odoo import tools
from odoo.addons.base.models.ir_mail_server import MailDeliveryException
import ast
import base64

from odoo import _, api, models, tools
from collections import defaultdict


_logger = logging.getLogger(__name__)

class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    def _notify_thread_by_email(self, message, recipients_data, msg_vals=False,
                                mail_auto_delete=True,  # mail.mail
                                model_description=False, force_email_company=False, force_email_lang=False,  # rendering
                                resend_existing=False, force_send=True, send_after_commit=True,  # email send
                                subtitles=None, **kwargs):
        
        # ==================================================================
        # Just Because of we don't want to notify user while fetch emails
        # ==================================================================
        if self.env.context.get('fetchmail_cron_running'):
            return True
        # ==================================================================
        # Just Because of we don't want to notify user while fetch emails
        # ==================================================================

        return super(MailThread,self)._notify_thread_by_email(
            message=message,
            recipients_data=recipients_data,
            msg_vals=msg_vals,
            mail_auto_delete=mail_auto_delete,
            model_description=model_description,
            force_email_company=force_email_company,
            force_email_lang=force_email_lang,
            resend_existing=resend_existing,
            force_send=force_send,
            send_after_commit=send_after_commit,
            subtitles=subtitles,
            kwargs=kwargs
            )

    @api.model
    def _message_route_process(self, message, message_dict, routes):
        self = self.with_context(attachments_mime_plainxml=True) # import XML attachments as text
        # postpone setting message_dict.partner_ids after message_post, to avoid double notifications
        original_partner_ids = message_dict.pop('partner_ids', [])
        thread_id = False
        for model, thread_id, custom_values, user_id, alias in routes or ():
            subtype_id = False
            related_user = self.env['res.users'].browse(user_id)
            Model = self.env[model].with_context(mail_create_nosubscribe=True, mail_create_nolog=True)
            if not (thread_id and hasattr(Model, 'message_update') or hasattr(Model, 'message_new')):
                raise ValueError(
                    "Undeliverable mail with Message-Id %s, model %s does not accept incoming emails" %
                    (message_dict['message_id'], model)
                )

            # disabled subscriptions during message_new/update to avoid having the system user running the
            # email gateway become a follower of all inbound messages
            ModelCtx = Model.with_user(related_user).sudo()
            if thread_id and hasattr(ModelCtx, 'message_update'):
                thread = ModelCtx.browse(thread_id)
                thread.message_update(message_dict)
            else:
                # if a new thread is created, parent is irrelevant
                message_dict.pop('parent_id', None)
                thread = ModelCtx.message_new(message_dict, custom_values)
                thread_id = thread.id
                subtype_id = thread._creation_subtype().id

            # replies to internal message are considered as notes, but parent message
            # author is added in recipients to ensure they are notified of a private answer
            parent_message = False
            if message_dict.get('parent_id'):
                parent_message = self.env['mail.message'].sudo().browse(message_dict['parent_id'])
            partner_ids = []
            if not subtype_id:
                if message_dict.get('is_internal'):
                    subtype_id = self.env['ir.model.data']._xmlid_to_res_id('mail.mt_note')
                    if parent_message and parent_message.author_id:
                        partner_ids = [parent_message.author_id.id]
                else:
                    subtype_id = self.env['ir.model.data']._xmlid_to_res_id('mail.mt_comment')

            post_params = dict(subtype_id=subtype_id, partner_ids=partner_ids, **message_dict)
            # remove computational values not stored on mail.message and avoid warnings when creating it


            # ---------------------------------------------------------------------------------------------------------------------------------------
            # THIS LOOP DEFINE VALUES WHICH ODOO REMOVES WHILE MAIL.MESSAGE computational so for out need we remove 'cc' and 'reply-to' from loop
            # ---------------------------------------------------------------------------------------------------------------------------------------
            for x in ('from', 'recipients', 'references', 'in_reply_to', 'bounced_email', 'bounced_message', 'bounced_msg_id', 'bounced_partner'):
            # ---------------------------------------------------------------------------------------------------------------------------------------
            # THIS LOOP DEFINE VALUES WHICH ODOO REMOVES WHILE MAIL.MESSAGE computational so for out need we remove 'cc' and 'reply-to' from loop
            # ---------------------------------------------------------------------------------------------------------------------------------------                 
            
                post_params.pop(x, None)
                
            new_msg = False
            if thread._name == 'mail.thread':  # message with parent_id not linked to record
                new_msg = thread.message_notify(**post_params)
            else:
                # parsing should find an author independently of user running mail gateway, and ensure it is not odoobot
                partner_from_found = message_dict.get('author_id') and message_dict['author_id'] != self.env['ir.model.data']._xmlid_to_res_id('base.partner_root')
                thread = thread.with_context(mail_create_nosubscribe=not partner_from_found)
                new_msg = thread.message_post(**post_params)

            if new_msg and original_partner_ids:
                # postponed after message_post, because this is an external message and we don't want to create
                # duplicate emails due to notifications
                new_msg.write({'partner_ids': original_partner_ids})
        return thread_id

    def message_update(self, msg_dict, update_vals=None):
        '''Adds cc email to self.email_cc while trying to keep email as raw as possible but unique'''
        res  = super(MailThread, self).message_update(msg_dict, update_vals)
        if self._name and self._name == 'sh.helpdesk.ticket':
            new_recipients = self._mail_cc_sanitized_raw_dict(msg_dict.get('recipients'))
            # --------------------------------------------------------------------------------------------------------------------------------
            # ODOO MANAGE ONLY CC_EMAILS FIELD IN PERTICUALR MODEL BUT WE NEED REPLY TO AS WELL SO REPLY TO EMAILS MERGE WITH CC EMAILS
            # --------------------------------------------------------------------------------------------------------------------------------
            if new_recipients:
                old_cc = self._mail_cc_sanitized_raw_dict(self.email_cc)
                new_recipients.update(old_cc)
                self.email_cc = ", ".join(new_recipients.values())      
            # --------------------------------------------------------------------------------------------------------------------------------
            # ODOO MANAGE ONLY CC_EMAILS FIELD IN PERTICUALR MODEL BUT WE NEED REPLY TO AS WELL SO REPLY TO EMAILS MERGE WITH CC EMAILS
            # --------------------------------------------------------------------------------------------------------------------------------        
        return res
    
    @api.model
    def message_new(self, msg_dict, custom_values=None):

        res = super(MailThread, self).message_new(msg_dict, custom_values)
        # --------------------------------------------------------------------------------------------------------------------------------
        # ODOO MANAGE ONLY CC_EMAILS FIELD IN PERTICUALR MODEL BUT WE NEED REPLY TO AS WELL SO REPLY TO EMAILS MERGE WITH CC EMAILS
        # --------------------------------------------------------------------------------------------------------------------------------
        if self._name and self._name == 'sh.helpdesk.ticket':
            res.sudo().email_cc = ", ".join(self._mail_cc_sanitized_raw_dict(msg_dict.get('recipients')).values())
        # --------------------------------------------------------------------------------------------------------------------------------
        # ODOO MANAGE ONLY CC_EMAILS FIELD IN PERTICUALR MODEL BUT WE NEED REPLY TO AS WELL SO REPLY TO EMAILS MERGE WITH CC EMAILS
        # --------------------------------------------------------------------------------------------------------------------------------

        return res
    


class MailMessage(models.Model):
    _inherit = 'mail.message'

    @api.model_create_multi
    def create(self, vals_list):
        
        results = super(MailMessage,self).create(vals_list)

        for result in results:
            
            # MOVE TICKET TO CUSTOMER REPLIES
            if self.env.context.get('form_portal_chatter') or result.message_type and result.subtype_id and result.message_type == 'email' and result.subtype_id.id == self.env.ref('mail.mt_comment').id and result.model == 'sh.helpdesk.ticket' and result.res_id:
                ticket = self.env['sh.helpdesk.ticket'].sudo().browse(result.res_id)
                if ticket:
                    mail_message_id = self.env['mail.message'].sudo().search([('res_id','=',ticket.id),('model','=','sh.helpdesk.ticket')])
                    if len(mail_message_id.ids) > 1:
                        if ticket.company_id and ticket.company_id.sh_customer_replied_stage_id:
                            if ticket.sh_auto_followup:
                                ticket.sh_auto_followup = False
                            ticket.sudo().stage_id = ticket.company_id.sh_customer_replied_stage_id.id
                            ticket.sudo().sh_ticket_replied_status = 'customer'
                            ticket.sudo().state = 'customer_replied'
                    else:
                        if ticket.company_id and ticket.company_id.new_stage_id:
                            ticket.sudo().stage_id = ticket.company_id.new_stage_id.id
                            ticket.sudo().sh_ticket_replied_status = 'customer'
                            ticket.sudo().state = 'customer_replied'
                    
            
            if not self.env.context.get('form_portal_chatter') and result.message_type and result.subtype_id and result.message_type == 'comment' and result.subtype_id.id == self.env.ref('mail.mt_comment').id and result.model == 'sh.helpdesk.ticket' and result.res_id:
                ticket = self.env['sh.helpdesk.ticket'].sudo().browse(result.res_id)
                if ticket:
                    if ticket.company_id and ticket.sh_auto_followup:
                        if ticket.company_id.sh_auto_followup_stage_id:
                            ticket.sudo().stage_id = ticket.company_id.sh_auto_followup_stage_id.id
                            ticket.sudo().sh_ticket_replied_status = 'staff'
                            ticket.sudo().state = 'staff_replied'
                        else:
                            ticket.sudo().stage_id = ticket.company_id.sh_staff_replied_stage_id.id
                            ticket.sudo().sh_ticket_replied_status = 'staff'
                            ticket.sudo().state = 'staff_replied'
                    elif ticket.company_id and not ticket.sh_auto_followup and ticket.company_id.sh_staff_replied_stage_id:
                        ticket.sudo().stage_id = ticket.company_id.sh_staff_replied_stage_id.id
                        ticket.sudo().sh_ticket_replied_status = 'staff'
                        ticket.sudo().state = 'staff_replied'        
        return results

class Mail(models.Model):
    _inherit = "mail.mail"

    def _send(self, auto_commit=False, raise_exception=False, smtp_session=None):
        IrMailServer = self.env['ir.mail_server']
        IrAttachment = self.env['ir.attachment']
        for mail_id in self.ids:
            success_pids = []
            failure_type = None
            processing_pid = None
            mail = None
            try:
                mail = self.browse(mail_id)
                print("\n\n\nmail",mail)
                if mail.state != 'outgoing':
                    continue

                # remove attachments if user send the link with the access_token
                body = mail.body_html or ''
                attachments = mail.attachment_ids
                for link in re.findall(r'/web/(?:content|image)/([0-9]+)', body):
                    attachments = attachments - IrAttachment.browse(int(link))

                # load attachment binary data with a separate read(), as prefetching all
                # `datas` (binary field) could bloat the browse cache, triggerring
                # soft/hard mem limits with temporary data.
                attachments = [(a['name'], base64.b64decode(a['datas']), a['mimetype'])
                               for a in attachments.sudo().read(['name', 'datas', 'mimetype']) if a['datas'] is not False]

                # specific behavior to customize the send email for notified partners
                email_list = []
                if mail.email_to:
                    email_list.append(mail._send_prepare_values())
                for partner in mail.recipient_ids:
                    values = mail._send_prepare_values(partner=partner)
                    values['partner_id'] = partner
                    email_list.append(values)

                # headers
                headers = {}
                ICP = self.env['ir.config_parameter'].sudo()
                bounce_alias = ICP.get_param("mail.bounce.alias")
                catchall_domain = ICP.get_param("mail.catchall.domain")
                if bounce_alias and catchall_domain:
                    headers['Return-Path'] = '%s@%s' % (bounce_alias, catchall_domain)
                if mail.headers:
                    try:
                        headers.update(ast.literal_eval(mail.headers))
                    except Exception:
                        pass

                # Writing on the mail object may fail (e.g. lock on user) which
                # would trigger a rollback *after* actually sending the email.
                # To avoid sending twice the same email, provoke the failure earlier
                mail.write({
                    'state': 'exception',
                    'failure_reason': _('Error without exception. Probably due to sending an email without computed recipients.'),
                })
                # Update notification in a transient exception state to avoid concurrent
                # update in case an email bounces while sending all emails related to current
                # mail record.
                notifs = self.env['mail.notification'].search([
                    ('notification_type', '=', 'email'),
                    ('mail_mail_id', 'in', mail.ids),
                    ('notification_status', 'not in', ('sent', 'canceled'))
                ])
                if notifs:
                    notif_msg = _('Error without exception. Probably due to concurrent access update of notification records. Please see with an administrator.')
                    notifs.sudo().write({
                        'notification_status': 'exception',
                        'failure_type': 'unknown',
                        'failure_reason': notif_msg,
                    })
                    # `test_mail_bounce_during_send`, force immediate update to obtain the lock.
                    # see rev. 56596e5240ef920df14d99087451ce6f06ac6d36
                    notifs.flush_recordset(['notification_status', 'failure_type', 'failure_reason'])

                # build an RFC2822 email.message.Message object and send it without queuing
                res = None
                # TDE note: could be great to pre-detect missing to/cc and skip sending it
                # to go directly to failed state update
                reply_to = mail.reply_to
                if mail.model in ['sale.order','account.move','crm.lead']:
                    reply_to = 'sales@softhealer.com'
                elif mail.model in ['sh.helpdesk.ticket','project.task']:
                    reply_to = 'angeltest7890@gmail.com'
                for email in email_list:
                    msg = IrMailServer.build_email(
                        email_from=mail.email_from,
                        email_to=email.get('email_to'),
                        subject=mail.subject,
                        body=email.get('body'),
                        body_alternative=email.get('body_alternative'),
                        email_cc=tools.email_split(mail.email_cc),
                        reply_to=reply_to,
                        attachments=attachments,
                        message_id=mail.message_id,
                        references=mail.references,
                        object_id=mail.res_id and ('%s-%s' % (mail.res_id, mail.model)),
                        subtype='html',
                        subtype_alternative='plain',
                        headers=headers)
                    processing_pid = email.pop("partner_id", None)
                    try:
                        res = IrMailServer.send_email(
                            msg, mail_server_id=mail.mail_server_id.id, smtp_session=smtp_session)
                        print("\n\n\nres",res)
                        print("\n\n\ncontext",self.env.context)

                        if processing_pid:
                            success_pids.append(processing_pid)
                        processing_pid = None
                    except AssertionError as error:
                        if str(error) == IrMailServer.NO_VALID_RECIPIENT:
                            # if we have a list of void emails for email_list -> email missing, otherwise generic email failure
                            if not email.get('email_to') and failure_type != "mail_email_invalid":
                                failure_type = "mail_email_missing"
                            else:
                                failure_type = "mail_email_invalid"
                            # No valid recipient found for this particular
                            # mail item -> ignore error to avoid blocking
                            # delivery to next recipients, if any. If this is
                            # the only recipient, the mail will show as failed.
                            _logger.info("Ignoring invalid recipients for mail.mail %s: %s",
                                         mail.message_id, email.get('email_to'))
                        else:
                            raise
                if res:  # mail has been sent at least once, no major exception occurred
                    mail.write({'state': 'sent', 'message_id': res, 'failure_reason': False})
                    _logger.info('Mail with ID %r and Message-Id %r successfully sent', mail.id, mail.message_id)
                    # /!\ can't use mail.state here, as mail.refresh() will cause an error
                    # see revid:odo@openerp.com-20120622152536-42b2s28lvdv3odyr in 6.1
                mail._postprocess_sent_message(success_pids=success_pids, failure_type=failure_type)
            except MemoryError:
                # prevent catching transient MemoryErrors, bubble up to notify user or abort cron job
                # instead of marking the mail as failed
                _logger.exception(
                    'MemoryError while processing mail with ID %r and Msg-Id %r. Consider raising the --limit-memory-hard startup option',
                    mail.id, mail.message_id)
                # mail status will stay on ongoing since transaction will be rollback
                raise
            except (psycopg2.Error, smtplib.SMTPServerDisconnected):
                # If an error with the database or SMTP session occurs, chances are that the cursor
                # or SMTP session are unusable, causing further errors when trying to save the state.
                _logger.exception(
                    'Exception while processing mail with ID %r and Msg-Id %r.',
                    mail.id, mail.message_id)
                raise
            except Exception as e:
                failure_reason = tools.ustr(e)
                _logger.exception('failed sending mail (id: %s) due to %s', mail.id, failure_reason)
                mail.write({'state': 'exception', 'failure_reason': failure_reason})
                mail._postprocess_sent_message(success_pids=success_pids, failure_reason=failure_reason, failure_type='unknown')
                if raise_exception:
                    if isinstance(e, (AssertionError, UnicodeEncodeError)):
                        if isinstance(e, UnicodeEncodeError):
                            value = "Invalid text: %s" % e.object
                        else:
                            value = '. '.join(e.args)
                        raise MailDeliveryException(value)
                    raise

            if auto_commit is True:
                self._cr.commit()
        return True

    # def _split_by_mail_configuration(self):
    #     """Group the <mail.mail> based on their "email_from" and their "mail_server_id".

    #     The <mail.mail> will have the "same sending configuration" if they have the same
    #     mail server or the same mail from. For performance purpose, we can use an SMTP
    #     session in batch and therefore we need to group them by the parameter that will
    #     influence the mail server used.

    #     The same "sending configuration" may repeat in order to limit batch size
    #     according to the `mail.session.batch.size` system parameter.

    #     Return iterators over
    #         mail_server_id, email_from, Records<mail.mail>.ids
    #     """
    #     mail_values = self.read(['id', 'email_from', 'mail_server_id'])

    #     # First group the <mail.mail> per mail_server_id and per email_from
    #     group_per_email_from = defaultdict(list)
    #     for values in mail_values:
    #         mail_server_id = values['mail_server_id'][0] if values['mail_server_id'] else False
    #         group_per_email_from[(mail_server_id, values['email_from'])].append(values['id'])

    #     # Then find the mail server for each email_from and group the <mail.mail>
    #     # per mail_server_id and smtp_from
    #     mail_servers = self.env['ir.mail_server'].sudo().search([], order='sequence')
    #     group_per_smtp_from = defaultdict(list)
    #     for (mail_server_id, email_from), mail_ids in group_per_email_from.items():
    #         if not mail_server_id:
    #             mail_server, smtp_from = self.env['ir.mail_server']._find_mail_server(email_from, mail_servers)
    #             mail_server_id = mail_server.id if mail_server else False
    #         else:
    #             smtp_from = email_from
    #         for mail_record in self:
    #             if mail_record.model in ['sale.order']:
    #                 sale_record_id = self.env['sale.order'].search([('id','=',mail_record.res_id)],limit=1)
    #                 if sale_record_id and sale_record_id.company_id:
    #                     smtp_from = '"' + 'Sales Team - '+sale_record_id.company_id.name + '" '+'<sales@softhealer.com>'
    #             elif mail_record.model in ['crm.lead']:
    #                 lead_record_id = self.env['crm.lead'].search([('id','=',mail_record.res_id)],limit=1)
    #                 if lead_record_id and lead_record_id.company_id:
    #                     smtp_from = '"' + 'Sales Team - '+lead_record_id.company_id.name + '" '+'<sales@softhealer.com>'
    #             elif mail_record.model in ['account.move']:
    #                 move_record_id = self.env['account.move'].search([('id','=',mail_record.res_id)],limit=1)
    #                 if move_record_id and move_record_id.company_id:
    #                     smtp_from = '"' + 'Accounting - '+move_record_id.company_id.name + '" '+'<sales@softhealer.com>'
    #             elif mail_record.model in ['sh.helpdesk.ticket']:
    #                 ticket_record_id = self.env['sh.helpdesk.ticket'].search([('id','=',mail_record.res_id)],limit=1)
    #                 if ticket_record_id and ticket_record_id.company_id:
    #                     smtp_from = '"' + 'Support Team - '+ticket_record_id.company_id.name + '" '+'<angeltest7890@gmail.com>'
    #         group_per_smtp_from[(mail_server_id, smtp_from)].extend(mail_ids)

    #     sys_params = self.env['ir.config_parameter'].sudo()
    #     batch_size = int(sys_params.get_param('mail.session.batch.size', 1000))
    #     for (mail_server_id, smtp_from), record_ids in group_per_smtp_from.items():
    #         for batch_ids in tools.split_every(batch_size, record_ids):
    #             yield mail_server_id, smtp_from, batch_ids