# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models
from lxml import etree
import base64
from datetime import datetime


MEDIA_TAGS = ['source', 'img']
SRC_REPLACE = [('%20', ' ')]
SCRIPT = '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>'
STYLE = '''
    <style>
        .sh_blog_content ul.nav .nav-item .nav-link {
            color: #000000;
        }
        #o_wblog_post_main,
        #o_wblog_post_main .o_container_small{
            max-width:100% !important;
            padding:0 !important;
        }
        @media only screen and(max-width: 991.98px){
            #o_wblog_post_main .o_container_small{padding-left:6px !important; padding-right: 6px !important;}
        }
    </style>
'''
INDEX_REPLCAE = [
    ('mr-', 'me-'),
    ('ml-', 'ms-'),
    ('pl-', 'ps-'),
    ('pr-', 'pe-'),
    ('badge-', 'bg-'),
    ('text-right', 'text-end'),
    ('text-left', 'text-start'),
    ('data-toggle', 'data-bs-toggle'),
    ('data-target', 'data-bs-target'),
    # ('<body>', '<body><section class="sh_blog_content">'),
    # ('</body>', f'</section>{SCRIPT}{STYLE}</body>')
]
# FLAG_NAME = ('eng.png', 'english.png', 'german.png', 'aarab.png', 'spanish.jpg', 'chinese.png', 'french.png')


class ShModuleIndex(models.Model):
    _inherit = "sh.module"

    # ====================================================
    #  Create/Update Index Queue Record
    # ====================================================
    def create_update_index_queue(self, connector_obj):
        find_index = self.env["sh.index.queue"].sudo().search(
            [("sh_module_id", "=", self.id)], limit=1)
        if find_index:
            find_index.sudo().write({
                'state': 'draft',
                'sh_message': ''
            })
            return
        is_small_index = self.is_small_index(connector_obj)
        self.env["sh.index.queue"].sudo().create({
            "sh_module_id": self.id,
            "state": "draft",
            'is_small_index': is_small_index
        })

    # def get_counter(self, connector_obj, json_data, counter):
    #     for data in json_data:
    #         if data.get('type') == 'file':
    #             counter += 1
    #         elif data.get('type') == 'dir':
    #             response = connector_obj.get_req(data.get("url"))
    #             self.get_counter(connector_obj, response.json(), counter)

    def is_small_index(self, connector_obj):
        # url = self.sh_module_url.replace(
        #     self.name, f'{self.name}/static/description')
        # response = connector_obj.get_req(url)
        # if response.status_code != 200:
        #     return False
        # counter = 0
        # self.get_counter()
        # for dict in response.json():
        #     if dict.get('type') == 'file':
        #         counter += 1
        #     elif dict.get('type') == 'dir':
        #         counter += 1
        return False

    # ====================================================
    #  Noftify The Partners
    # ====================================================

    def _notify_partners(self):
        ''' Notify the partners about the product if not already notified. '''
        try:
            if not self.sh_product_id:
                if not self.sh_blog_post_id.sh_product_id:
                    connector_obj.create_log('notify', 'product', f'Missing product reference !')
                    return False
                self.sudo().write({
                    'sh_product_id': self.sh_blog_post_id.sh_product_id.id
                })
            elif not self.sh_blog_post_id.sh_product_id:
                self.sh_blog_post_id.sudo().write({
                    'sh_product_id': self.sh_product_id.id
                })
            connector_obj = self.env["sh.github.connector"].sudo().search(
                [("state", "=", "success")], limit=1)
            if not connector_obj:
                return False
            # # Connector obj or product not have the version ref !
            # if not (connector_obj.notify_version_id and self.sh_product_id.product_template_variant_value_ids):
            #     return False
            # # Diff version !
            # notify = False
            # for line in self.sh_product_id.product_template_variant_value_ids:
            #     if connector_obj.notify_version_id.name == line.name:
            #         notify = True
            #         break
            # if not notify:
            #     return False
            notify_me_recs = self.env['sh.migration.notify.me'].sudo().search([
                ('product_id', '=', self.sh_product_id.id),
                ('is_notified', '=', False)
            ])
            if not notify_me_recs:
                return False
            # Get the email template
            email_template_id = self.env.ref('sh_github_connector.sh_github_notify_partners', raise_if_not_found=False)
            if not email_template_id:
                connector_obj.create_log('notify', 'product', 'Failed to get mail template view !')
                return False
            email_template = self.env['mail.template'].browse(email_template_id.id)
            if not email_template:
                connector_obj.create_log('notify', 'product', 'Failed to get mail template record !')
                return False
            count = 0
            status_list = []
            for notify_me_rec in notify_me_recs:
                if not notify_me_rec.partner_id:
                    continue
                # Send mail
                status_list.append(email_template.sudo().send_mail(notify_me_rec.id, force_send=True))
                notify_me_rec.is_notified = True
                count += 1
            if count:
                message = f'Notify {count} partners about the poduct ({self.sh_product_id.name}) launched.\nStatus: {status_list}'
                connector_obj.create_log('notify', 'product', message, 'success')
            return True
        except Exception as e:
            connector_obj.create_log('notify', 'product', f'Error: {e} !')

    # ====================================================
    #  Create/Update Blog
    # ====================================================

    def create_blog_post(self, connector_obj):
        domain = [
            ('sh_product_id', '=', self.sh_product_id.id),
            ('active', '=', True)
        ]
        # if connector_obj.blog_blog_id:
        #     domain.append(('blog_id', '=', connector_obj.blog_blog_id.id))
        # if connector_obj.website_id:
        #     domain.append(('website_id', '=', connector_obj.website_id.id))
        blog = self.env['blog.post'].sudo().search(domain, limit=1)
        if blog:
            self.sudo().write({"sh_blog_post_id": blog.id})
            self.sh_product_id.sudo().write({"sh_blog_post_id": blog.id})
            return blog
        if not connector_obj.blog_blog_id:
            return False
        # self.create_update_index_queue(connector_obj)
        blog_name = self.sh_product_id.name
        try:
            blog_name += f' v{self.sh_branch_id.name.split(".")[0]}'
        except:
            pass
        blog_vals = {
            "name": blog_name,
            "sh_product_id": self.sh_product_id.id,
            "blog_id": connector_obj.blog_blog_id.id,
            'is_published': False
        }
        if self.sh_product_id.last_updated_date:
            blog_vals['post_date'] = self.sh_product_id.last_updated_date
        blog = self.env["blog.post"].sudo().create(blog_vals)
        self.sudo().write({"sh_blog_post_id": blog.id})
        self.sh_product_id.sudo().write({"sh_blog_post_id": blog.id})
        return blog

    # ========================================================================================================
    #  INDEX / BLOG POST
    # ========================================================================================================

    def remove_sections(self, html_tree, connector_obj):
        section_tags = html_tree.findall('.//section[@id="sh_multi_language"]')
        if section_tags is not None:
            if len(section_tags) > 1:
                connector_obj._generate_activity('product.product', self.sh_product_id, 'Check Blog For Multi Language.')
            elif len(section_tags) == 1:
                parent = section_tags[0].getparent()
                index = parent.index(section_tags[0])
                siblings = parent[index:]
                for sibling in siblings:
                    parent.remove(sibling)
            else:
                # if other (sh_like_module) sections found
                if html_tree.findall('.//section[@id="sh_like_module"]') is not None:
                    connector_obj._generate_activity('product.product', self.sh_product_id, 'Check Blog For Multi Language.')

    def get_index_data(self, connector_obj):
        # ======= Get Blog Content =======
        response_obj = connector_obj.get_req(self.sh_module_url.replace(
            self.name, f"{self.name}/static/description/index.html"))
        if response_obj.status_code != 200:
            return False
        response = response_obj.text
        if not response:
            return False
        # ======= Get Blog Content =======
        global INDEX_REPLCAE, SCRIPT, STYLE
        for replace_pair in INDEX_REPLCAE:
            response = response.replace(replace_pair[0], replace_pair[1])
        html_tree = etree.HTML(response)
        html_body_tree = etree.HTML(response).find('body')
        if html_body_tree is not None:
            html_tree = html_body_tree
        if html_tree is None:
            return False
        try:
            for tag_name in ('script', 'link'):
                tags = html_tree.xpath(f'.//{tag_name}')
                if tags is not None:
                    for tag in tags:
                        tag.getparent().remove(tag)
            # =============== Remove sh_multi_language (FLAGS) ===============
            self.remove_sections(html_tree, connector_obj)
            # =============== Add Video Link ===============
            video_div_obj_list = html_tree.findall(".//*[@data-video-id]")
            if video_div_obj_list is None:
                return etree.tostring(html_tree, pretty_print=True, encoding="unicode")
            for video_div_obj in video_div_obj_list:
                data_video_id = video_div_obj.get("data-video-id")
                yt_video_id = data_video_id.split("?")[0]
                a_tag = video_div_obj.find("a")
                if a_tag is not None:
                    a_tag.set("href", f"https://youtu.be/{yt_video_id}")
                    a_tag.set("target", "_blank")
        except:
            pass
        return etree.tostring(html_tree, pretty_print=True, encoding="unicode")
        # ========================================================

    def process_blog(self):
        connector_obj = self.env["sh.github.connector"].sudo().search(
            [("state", "=", "success")], limit=1)
        if not self.sh_blog_post_id:
            if self.sh_product_id.sh_blog_post_id:
                self.sudo().write(
                    {'sh_blog_post_id': self.sh_product_id.sh_blog_post_id.id})
            elif self.state in ('draft', '', None):
                self.sync_module(connector_obj, pop_up=False)
            else:
                return False, f"Can't Fine Blog Post For Module {self.name} ({self.sh_branch_id.name})!"
        try:
            # =============================================
            content = self.get_index_data(connector_obj)
            if not content:
                return False, f"Failed To Get The Index Content!\nPlease Check That Index File Is Located At '{self.name}/static/description/index.html' Or Not."
            # =============================================
            self.sh_blog_post_id.sudo().write({
                'content': content,
                # 'is_published': False
            })
            self.sh_img_url = self.sh_module_url.replace(
                self.name, f"{self.name}/static/description") + ','
            return True, 'Index Is In Progress.'
        except Exception as e:
            connector_obj.create_log("sync", "index", e, "error")
            return False, e

    def get_blog_media(self):
        try:
            if not self.sh_img_url:
                if self.sh_media_list:
                    self.unlink_extra_attachments()
                return 2, 'Sync Index Successfully.'
            url_list = self.sh_img_url.split(',')
            current_url = False
            for url in url_list:
                if url:
                    current_url = url
                    break
            if not current_url:
                if self.sh_media_list:
                    self.unlink_extra_attachments()
                return 2, 'Sync Index Successfully.'
            connector_obj = self.env["sh.github.connector"].sudo().search(
                [("state", "=", "success")], limit=1)
            response = connector_obj.get_req(current_url)
            if response.status_code != 200:
                return False, response.text
            # Get Index and Images(.png, .gif, .jpg) files Data
            media_dict, next_url_list = self.get_media_data(
                response.json())
            if not media_dict:
                return False, "Failed to Get Blog Medias!"
            # if self.arrange_imgs(media_dict):
            #     if next_url_list:
            #         for url in next_url_list:
            #             self.sh_img_url += f'{url},'
            #     self.sh_img_url = self.sh_img_url.replace(
            #         f'{current_url},', '')
            #     return True, 'Some Media Attached Successfully.'
            # return True, ''
            self.arrange_imgs(connector_obj, media_dict)
            if next_url_list:
                for url in next_url_list:
                    self.sh_img_url += f'{url},'
            self.sh_img_url = self.sh_img_url.replace(
                f'{current_url},', '')
            return True, 'Some Media Attached Successfully.'
            # =============== Process Images ===============
        except Exception as e:
            connector_obj.create_log("sync", "index", e, "error")
            return False, e

    def get_media_data(self, res_json_list):
        media_dict = {}
        next_url_list = []
        for res_dict in res_json_list:
            key = res_dict["path"].split("description/")[1]
            if res_dict["type"] == 'file':
                media_dict[key] = res_dict.get("url")
            elif res_dict["type"] == "dir":
                next_url_list.append(res_dict.get("url"))
        return media_dict, next_url_list

    def _get_src_data(self, html_tree, connector_obj, url_dict):
        global MEDIA_TAGS, SRC_REPLACE
        path_str = ''
        for find_tag in MEDIA_TAGS:
            try:
                tags = html_tree.findall(f'.//{find_tag}')
                if tags is None:
                    continue
                path = '/web/content'
                if find_tag == 'img':
                    path = '/web/image'
                for tag in tags:
                    try:
                        src = tag.get('src')
                        if not src:
                            continue
                        if not url_dict.get(src):
                            continue
                        for pair in SRC_REPLACE:
                            src = src.replace(pair[0], pair[1])
                        attachment = self.get_img_attachment(
                            connector_obj, url_dict[src], src)
                        if attachment:
                            tag.set("src", f"{path}/{attachment.id}/{attachment.name}")
                        path_str += f'{src},'
                    except:
                        pass
            except:
                pass
        return path_str

    def arrange_imgs(self, connector_obj, url_dict):
        html_tree = etree.HTML(self.sh_blog_post_id.content)
        if html_tree is None:
            return False
        # ================ Append Images In Content Field ================
        all_img_tags = html_tree.findall(".//img")
        if all_img_tags is None:
            return False
        # ================ Get Media ================
        # path_str = ''
        path_str = self._get_src_data(html_tree, connector_obj, url_dict)
        # Unlink Extra Attachments For This Blog If Its Remove From The Index
        if path_str:
            if self.sh_media_list:
                self.sh_media_list += path_str
            else:
                self.sh_media_list = path_str
            return self.sh_blog_post_id.sudo().write({
                'content': etree.tostring(html_tree, pretty_print=True, encoding="unicode")
            })
        return False

    def unlink_attachments(self, path_list):
        index = self.env["sh.index.queue"].sudo().search(
            [("sh_module_id", "=", self.id)], limit=1)
        if index and len(path_list) < 31:
            index.is_small_index = True
        attachments = self.env['ir.attachment'].sudo().search([
            ('res_id', '=', self.sh_blog_post_id.id),
            ('res_model', '=', 'blog.post'),
        ])
        if not attachments:
            return
        for attachment in attachments:
            if attachment.sh_path and attachment.sh_path not in path_list:
                attachment.unlink()

    def unlink_extra_attachments(self):
        path_list = self.sh_media_list.split(',')
        self.unlink_attachments(path_list)
        self.sh_media_list = ''
        # self.sh_blog_post_id.is_published = True

    # =======================================================================
    #  Get Blog Content
    # =======================================================================

    def get_blog_attachment(self, sh_path, data, name):
        ir_attachment = self.env['ir.attachment'].sudo().search([
            ('sh_path', '=', sh_path),
            ('res_id', '=', self.sh_blog_post_id.id),
            ('res_model', '=', 'blog.post')
        ], limit=1)
        if ir_attachment:
            ir_attachment.sudo().write({
                'datas': data.decode(),
                'name': name,
            })
        else:
            ir_attachment = self.env['ir.attachment'].sudo().create({
                'sh_path': sh_path,
                'name': name,
                'res_id': self.sh_blog_post_id.id,
                'res_model': 'blog.post',
                'public': True,
                'datas': data.decode(),
            })
        return ir_attachment

    def get_img_attachment(self, connector_obj, url, src):
        response = connector_obj.get_req(url)
        if response.status_code != 200:
            return False
        data = base64.b64encode(response.content)
        name = src
        if '/' in src:
            name = src.split('/')
            name = name[-1]
        return self.get_blog_attachment(src, data, name)

    def get_src_data(self, html_tree, connector_obj, path_list):
        global MEDIA_TAGS
        for find_tag in MEDIA_TAGS:
            try:
                tags = html_tree.findall(f'.//{find_tag}')
                if tags is None:
                    continue
                path = '/web/content'
                if find_tag == 'img':
                    path = '/web/image'
                for tag in tags:
                    try:
                        src = tag.get('src')
                        if not src:
                            continue
                        encoded_src = src.replace(' ', '%20')
                        url = self.sh_module_url.replace(
                            self.name, f'{self.name}/static/description/{encoded_src}')
                        attachment = self.get_img_attachment(connector_obj, url, src)
                        if attachment:
                            tag.set("src", f"{path}/{attachment.id}/{attachment.name}")
                        path_list.append(src)
                    except:
                        pass
            except:
                pass

    def get_blog_content(self, index_file_data, connector_obj):
        html_tree = etree.HTML(index_file_data)
        if html_tree is None:
            return False
        # ================ Append Images/Video In Content Field ================
        try:
            path_list = []
            self.get_src_data(html_tree, connector_obj, path_list)
            # === Unlink Extra Attachments For This Blog If Its Remove From The Index ===
            if path_list:
                self.unlink_attachments(path_list)
        except:
            pass
        # ========================================================
        return etree.tostring(html_tree, pretty_print=True, encoding="unicode")

    def process_full_blog(self, connector_obj=False):
        if not connector_obj:
            connector_obj = self.env["sh.github.connector"].sudo().search(
                [("state", "=", "success")], limit=1)
        if not self.sh_blog_post_id:
            if self.sh_product_id.sh_blog_post_id:
                self.sudo().write(
                    {'sh_blog_post_id': self.sh_product_id.sh_blog_post_id.id})
            # elif self.state in ('draft', '', None):
            #     self.sync_module(connector_obj, pop_up=False)
            else:
                return False, f"Can't Fine Blog Post For Module {self.name} ({self.sh_branch_id.name})!"
        try:
            # Api call for getting description dir data
            # Replace module name(path) with its description path
            response = connector_obj.get_req(self.sh_module_url.replace(
                self.name, f"{self.name}/static/description"))
            if response.status_code != 200:
                index_error = ''
                try:
                    index_error = response.json().get('message')
                except:
                    index_error = response.text
                return False, f"Sync Index Error: {index_error}"

            index_last_commit = False
            vals = {}

            try:
                # Get the last commit id for the index
                for desc_dir_item in response.json():
                    # desc_dir_item is Dict
                    item_name = desc_dir_item.get('name')
                    if not item_name:
                        continue
                    if item_name == 'index.html':
                        index_last_commit = desc_dir_item.get('sha')
                        break
            except:
                pass

            # Check that index is update ?
            # Then only proceed for it
            if index_last_commit:
                if self.sh_blog_post_id.sh_github_last_commit:
                    if self.sh_blog_post_id.sh_github_last_commit == index_last_commit:
                        # Index file is not modified, so don't need to sync it
                        return True, ''
                # Store the latest commit id of index file in the Blog Post
                vals.update({
                    'sh_github_last_commit': index_last_commit
                })

            # ============================
            #  Content (HTML Field)
            # ============================
            index_file_data = self.get_index_data(connector_obj)
            if not index_file_data:
                return False, f"Failed To Get The Index Content!\nPlease Check That Index File Is Located At '{self.name}/static/description/index.html' Or Not."

            global SCRIPT, STYLE
            index_file_data = '<section class="sh_blog_content">' + index_file_data + f'</section>{SCRIPT}{STYLE}'
            content = self.get_blog_content(index_file_data, connector_obj)
            if not content:
                return False, "Failed to get body tag from Index!"

            vals.update({"content": content})
            # ====== Update Other Blog Vals ======
            if self.sh_product_id.last_updated_date:
                vals['post_date'] = self.sh_product_id.last_updated_date
            if connector_obj.website_id:
                vals['website_id'] = connector_obj.website_id.id
            if not self.sh_blog_post_id.sh_product_id:
                vals['sh_product_id'] = self.sh_product_id.id
            # ====== Update Blog ======
            self.sh_blog_post_id.sudo().write(vals)
            self.sudo().write({
                'sh_media_list': '',
                'sh_img_url': self.sh_module_url.replace(self.name, f"{self.name}/static/description") + ','
            })
            return True, "Sync Index Successfully."

        except Exception as e:
            return False, f"Sync Index Error: {e}"
