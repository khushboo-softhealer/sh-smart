# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api
import re
import html2text
from bs4 import BeautifulSoup
from odoo.exceptions import UserError


# class MailMessage(models.Model):
#     _inherit = 'mail.message'

#     @api.model
#     def create(self, vals):
#         if vals.get('model') and vals.get('model') == 'sh.helpdesk.ticket':
#             ticket_id = self.env['sh.helpdesk.ticket'].sudo().browse(
#                 vals.get('res_id'))
#             if ticket_id:
#                 if vals.get('author_id') and vals.get('author_id') == ticket_id.partner_id.id:
#                     ticket_id.state = 'customer_replied'
#                     ticket_id.replied_date = vals.get('date')
#                 elif vals.get('author_id') and vals.get('author_id') != 2 and vals.get('author_id') != ticket_id.partner_id.id:
#                     ticket_id.state = 'staff_replied'
#                     ticket_id.replied_date = vals.get('date')
#         return super(MailMessage, self).create(vals)


class MailComposeWizard(models.TransientModel):
    _inherit = 'mail.compose.message'

    sh_quick_reply_template_id = fields.Many2one(
        'sh.quick.reply', string='Quick Reply Template')
    body_str = fields.Html('Body')
    is_wp = fields.Boolean('Whatsapp ?')

    @api.model
    def default_get(self, fields_list):
        res = super(MailComposeWizard, self).default_get(fields_list)
        result = """
            <div class='predefined'>
            </div>"""
        res.update({
            'body': result
        })
        return res

    @api.onchange('sh_quick_reply_template_id')
    def onchange_sh_quick_reply_template_id(self):
        if self.sh_quick_reply_template_id and self.sh_quick_reply_template_id.sh_description:
            self.body=self.sh_quick_reply_template_id.sh_description 
            html_code = self.sh_quick_reply_template_id.sh_description
            if self.model == 'sh.helpdesk.ticket':
                ticket = self.env['sh.helpdesk.ticket'].browse(self.res_id)
                if ticket:
                    soup = BeautifulSoup(html_code, 'html.parser')
                    a_tag = soup.find_all('a')
                    if a_tag:
                        for link in a_tag:
                            if 'wa.me' in link.get('href', ''):
                                old_href = link['href']
                                old_href += '%s' %(ticket.name) 
                                link['href'] = old_href
                                modified_html_code = str(soup)
                                self.body=modified_html_code
        # body_str = self.body
        # if not self.body_str:
        #     self.body_str = body_str
        # if not self.sh_quick_reply_template_id:
        #     self.body = self.body_str
        # else:
        #     if 'div class="predefined"' in body_str:
        #         tag_1 = 'div class="predefined"'
        #         tag_2 = "div"
        #         reg_str = "<" + tag_1 + ">(.*?)</" + tag_2 + ">"
        #         res = re.findall(reg_str, body_str.strip())
        #         if len(res) > 0:
        #             original_split_str = '<div class="predefined">' + \
        #                 str(res[0]) + '</div>'
        #             original_splited_str = body_str.split(original_split_str)
        #             original_joined_str = original_splited_str[0] + \
        #                 '<div class="predefined"></div>' + \
        #                 original_splited_str[1]
        #             body_str = original_joined_str
        #         if self.sh_quick_reply_template_id:
        #             joined_str = ''
        #             splited_str = body_str.split(
        #                 '<div class="predefined"></div>')
        #             if len(splited_str) > 1:
        #                 joined_str = splited_str[0] + '<div class="predefined">'+str(
        #                     self.sh_quick_reply_template_id.sh_description) + '</div>'+splited_str[1]
        #                 self.body = joined_str
        #             elif len(splited_str) == 1:
        #                 joined_str = splited_str[0] + '<div class="predefined">'+str(
        #                     self.sh_quick_reply_template_id.sh_description) + '</div>'
        #                 self.body = joined_str

    def action_send_wp(self):
        text = html2text.html2text(self.body)
        if not self.partner_ids[0].mobile:
            raise UserError('Partner Mobile Number Not Exist !')
        phone = str(self.partner_ids[0].mobile)
        base_url = self.env['ir.config_parameter'].sudo(
        ).get_param('web.base.url')
        if self.attachment_ids:
            text += '%0A%0A Other Attachments :'
            for attachment in self.attachment_ids:
                attachment.generate_access_token()
                text += '%0A%0A'
                text += base_url+'/web/content/ir.attachment/' + \
                    str(attachment.id)+'/datas?access_token=' + \
                    attachment.access_token
        context = dict(self._context or {})
        active_id = context.get('active_id', False)
        active_model = context.get('active_model', False)

        if text and active_id and active_model:
            message = str(text).replace('*', '').replace('_', '').replace('%0A',
                                                                          '<br/>').replace('%20', ' ').replace('%26', '&')
            if active_model == 'sh.helpdesk.ticket' and self.env['sh.helpdesk.ticket'].browse(
                    active_id).company_id.sh_display_in_chatter:
                self.env['mail.message'].create({
                    'partner_ids': [(6, 0, self.partner_ids.ids)],
                    'model': 'sh.helpdesk.ticket',
                    'res_id': active_id,
                    'author_id': self.env.user.partner_id.id,
                    'body': message or False,
                    'message_type': 'comment',
                })
        url = "https://web.whatsapp.com/send?l=&phone="+phone+"&text=" + text
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }
