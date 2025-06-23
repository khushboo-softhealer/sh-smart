# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models
import requests


class InheritImportBaseBlogTagCategory(models.Model):
    _inherit = "sh.import.base"

    def import_blog_tag_category(self):
        ''' ============= blog.tag.category ============= '''
        confid = self.env['sh.import.base'].search([], limit=1)
        response = requests.get('''%s/api/public/blog.tag?query={*}''' % (confid.base_url))
        if response.status_code == 200:
            response_json = response.json()
            if response_json.get('error') != '0':
                return False

            count = 0
            fail = 0

            for blog_tag in response_json['result']:
                # try:
                if not blog_tag.get('id'):
                    continue
                find_rec = self.env['blog.tag'].search([('remote_blog_tag_id', '=', blog_tag.get('id'))])
                blog_tag_vals = {
                    "remote_blog_tag_id": blog_tag.get('id'),
                    "name": blog_tag.get('name'),
                    "display_name": blog_tag.get('display_name'),
                    "is_seo_optimized": blog_tag.get('is_seo_optimized'),
                    "website_meta_title": blog_tag.get('website_meta_title'),
                    "website_meta_description": blog_tag.get('website_meta_description'),
                    "website_meta_keywords": blog_tag.get('website_meta_keywords'),
                    "website_meta_og_img": blog_tag.get('website_meta_og_img'),
                }
                if find_rec:
                    find_rec.write(blog_tag_vals)
                else:
                    blog_id=self.env['blog.tag'].create(blog_tag_vals)
                count += 1

                # except Exception as e:
                #     fail += 1
                #     self.create_fail_log(
                #         name=blog_tag.get('id'),
                #         field_type='blog_basic',
                #         error=e,
                #         import_json=blog_tag,
                #     )

            if count > 0:
                self.create_log(field_type='blog_basic', error="%s Blog Tag Imported Successfully" % (count), state='success')
            if fail > 0:
                self.create_log(field_type='blog_basic', error="%s Blog Tag Failed To Import." % (fail))
        else:
            self.create_log(field_type='blog_basic', error=response.text)
