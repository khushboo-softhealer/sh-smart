# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models
from lxml import html
from odoo import models


class ShBlogPostSortAttachments(models.Model):
    _inherit = "blog.post"

    def replace_post_attachments(self):
        sh_post_ids = self.env['blog.post'].browse(
            self.env.context.get('active_ids'))
        if sh_post_ids:
            success_counter = 0
            failed_counter = 0
            not_found_list = []
            exceptions_list = []
            for post in sh_post_ids:
                # -----------------------------------------------------
                # FIRST PARSER HTML TO TRAVEL
                # -----------------------------------------------------
                post_content = post.content
                html_post_content = html.fromstring(post_content.encode(
                    'UTF-8'), parser=html.HTMLParser(encoding='UTF-8'))
                # -----------------------------------------------------
                # FIND IMAGE TAG IN POST CONTENT
                # -----------------------------------------------------
                list_element_img = html_post_content.xpath("//img")
                if list_element_img:

                    for element_img in list_element_img:
                        # -----------------------------------------------------
                        # IF WE ALREADY REPLACE NEW SOURCE IN POST CONTENT THEN SKIP IT.
                        # -----------------------------------------------------
                        for key, val in element_img.items():
                            if key == 'src':
                                # -----------------------------------------------------
                                # FIRST GET IMAGE FROM SOURCE AND REPLACE
                                # WITH PROPER ERROR HANDING
                                # -----------------------------------------------------
                                try:
                                    if '/web/image/' in val:
                                        attachment_id_and_name = val.split(
                                            '/web/image/')[1]
                                        if '/' in attachment_id_and_name:
                                            v12_attachment_id = attachment_id_and_name.split(
                                                '/')[0]
                                            # v12_attachment_id_str = attachment_id_and_name.split('/')[0]
                                            # v12_attachment_id = False
                                            # try:
                                            #     v12_attachment_id = int(v12_attachment_id_str)
                                            # except:
                                            #     pass
                                            if v12_attachment_id:
                                                attachment = self.env['ir.attachment'].sudo().search(
                                                    [('remote_ir_attachment_id', '=', v12_attachment_id)], limit=1)
                                                if attachment:
                                                    attachment.sudo().write(
                                                        {'public': True})
                                                    new_url = f"/web/image/{attachment.id}/{attachment.name}"
                                                    element_img.set(
                                                        'src', new_url)
                                                    success_counter += 1
                                                else:
                                                    not_found_list.append(
                                                        v12_attachment_id)
                                                    failed_counter += 1
                                                    continue
                                except Exception as e:
                                    exceptions_list.append(e)
                                    failed_counter += 1
                # -----------------------------------------------------
                # FINALLY PUT NEW MODIFIED HTML IN POST CONTENT.
                # -----------------------------------------------------
                html_content = html.tostring(
                    html_post_content, pretty_print=False, encoding='UTF-8')
                if isinstance(html_content, bytes):
                    html_content = html_content.decode()
                post.content = html_content
            message = ''
            if success_counter:
                message += f'{message} Image Links Updated Successfully.\n'
            if failed_counter:
                message += f"{failed_counter} Images Links Failed To Update.\n"
            if not_found_list:
                message += f"Attachments Are Not Found With Remote Id:\n{not_found_list}\n"
            if exceptions_list:
                message += f"Some Other Exceptions Are:\n{exceptions_list}\n"
            if not message:
                message = 'Nothing Found To Update!'
            view = self.env.ref("sh_message.sh_message_wizard")
            context = dict(self._context or {})
            context['message'] = message
            return {
                "name": "Success",
                "type": "ir.actions.act_window",
                "view_type": "form",
                "view_mode": "form",
                "res_model": "sh.message.wizard",
                "views": [(view.id, "form")],
                "view_id": view.id,
                "target": "new",
                "context": context,
            }
        return None
