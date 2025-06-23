# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from lxml import html as htmltree
import re
from odoo import _, api, models


class MailTemplate(models.AbstractModel):
    _inherit = "mail.thread"

    @api.model
    def _debrand_body(self, html):
        using_word = _('using')
        odoo_word = _('Odoo')
        html = re.sub(
            using_word + "(.*)[\r\n]*(.*)>" + odoo_word + r"</a>", "", html,
        )
        powered_by = _("Powered by")
        if powered_by not in html:
            return html
        root = htmltree.fromstring(html)
        powered_by_elements = root.xpath(
            "//*[text()[contains(.,'%s')]]" % powered_by
        )
        for elem in powered_by_elements:
            # make sure it isn't a spurious powered by
            if any(
                [
                    "www.odoo.com" in child.get("href", "")
                    for child in elem.getchildren()
                ]
            ):
                for child in elem.getchildren():
                    elem.remove(child)
                elem.text = None
        return htmltree.tostring(root).decode("utf-8")

    def _replace_local_links(self, html, base_url=None):
        html = super()._replace_local_links(html,base_url)
        html = self._debrand_body(html)
        return html
    
