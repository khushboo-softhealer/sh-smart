# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
# import aspose.words as aw

class ShKnowledgeArticalwizard(models.TransientModel):
    _name = 'sh.knowledge.article.wizard'
    _description = "Knowledge Artical Wizard"

    name=fields.Char(string="Name")
    sh_document_no=fields.Char(string="Document Number",required=True)    
    sh_parent_id=fields.Many2one('sh.knowledge.article',string="Parent Document")    
    effective_date=fields.Date(string="Effective Date")       
    sh_content=fields.Html(string="Content")
    banner = fields.Html(string="Banner")
    icon = fields.Binary(string="Icon")

    def update_article(self):       
        if self.sh_parent_id and self.sh_document_no:                   
            vals={
                'sh_document_no':self.sh_document_no,                
                'sh_parent_id':self.sh_parent_id.id,
                'sh_content':self.sh_content,
                'state':'draft',
            }
            if self.banner:
                vals.update({
                    'banner':self.banner,
                })
            if self.icon:
                vals.update({
                    'icon':self.icon,
                })
            obj = self.env['sh.knowledge.article'].sudo().create(vals)            
