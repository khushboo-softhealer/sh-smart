# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
import re
from markupsafe import Markup
from odoo import api, models, tools


class MailRenderMixin(models.AbstractModel):
    _inherit = "mail.render.mixin"

    def remove_href_odoo(self, value, remove_parent=True, to_keep=None):
        
        if len(value) < 20:
            return value
        # value can be bytes type; ensure we get a proper string
        if type(value) is bytes:
            back_to_bytes = True
            value = value.decode()
        else:
            back_to_bytes = False

        has_dev_odoo_link = re.search(
            r"<a\s(.*)dev\.odoo\.com", value, flags=re.IGNORECASE
        )        
        has_odoo_link = re.search(
            r"<a\s(.*)odoo\.com", value, flags=re.IGNORECASE)
        
        # -------------------------------------------------------
        # REMOVE ANCHOR TAG IF IT'S RELATED TO ODOO
        # -------------------------------------------------------
        # if has_odoo_link:
        #     value = re.sub(r"<a\s(.*)odoo\.com.*?</a>", "", value, flags=re.IGNORECASE)

        # if has_dev_odoo_link:
        #     value = re.sub(r"<a\s(.*)dev\.odoo\.com*?</a>", "", value, flags=re.IGNORECASE)        
        # -------------------------------------------------------
        # REMOVE ANCHOR TAG IF IT'S RELATED TO ODOO
        # -------------------------------------------------------
        

        # -------------------------------------------------------
        # REMOVE ODOO KEYWORD FROM MAIL BODY
        # -------------------------------------------------------
        # value = re.sub(r"Odoo|odoo|OdooBot|@OdooBot@Odoo|@odoo", "Softhealer Technologies", value)

        # value = value.replace('Odoo',get_keyword.value)
        # -------------------------------------------------------
        # REMOVE ODOO KEYWORD FROM MAIL BODY
        # -------------------------------------------------------

        if back_to_bytes:
            value = value.encode()
        
        return value
    
    @api.model
    def _render_template(self, template_src, model, res_ids, engine="inline_template", add_context=None, options=None, post_process=False):
        """replace anything that is with odoo in templates
        if is a <a that contains odoo will delete it completely
        original:
         Render the given string on records designed by model / res_ids using
        the given rendering engine.

        :param str template_src: template text to render (jinja) or  (qweb)
          this could be cleaned but hey, we are in a rush
        :param str model: model name of records on which we want to perform rendering
        :param list res_ids: list of ids of records (all belonging to same model)
        :param string engine: inline_template, qweb or qweb_view;
        :param post_process: perform rendered str / html post processing (see
          ``_render_template_postprocess``)

        :return dict: {res_id: string of rendered template based on record}"""
        orginal_rendered = super()._render_template(template_src,model,res_ids,engine=engine,add_context=add_context,options=options,post_process=post_process)

        for key in res_ids:
            
            orginal_rendered[key] = self.remove_href_odoo(orginal_rendered[key])

        return orginal_rendered

    def _replace_local_links(self, html, base_url=None):
        message = super()._replace_local_links(html, base_url=base_url)

        wrapper = Markup if isinstance(message, Markup) else str
        message = tools.ustr(message)
        if isinstance(message, Markup):
            wrapper = Markup

        message = re.sub(
            r"""(Powered by\s(.*)Odoo</a>)""", "<div>&nbsp;</div>", message
        )

        return wrapper(message)
