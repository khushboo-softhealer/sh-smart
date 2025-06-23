# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

class ShKnowledgeArtical(models.Model):
    _name = 'sh.knowledge.article'
    _description = 'knowledge Article'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']


    def _get_default_stage_id(self):
        return self.env['sh.sop.stages'].search([], limit=1,order='id asc')
    
    def _get_default_manager_id(self):
        if self.env.user.employee_id and self.env.user.employee_id.coach_id:
            coach_id=self.env.user.employee_id.coach_id
            if coach_id.user_id:
                return coach_id.user_id

    name=fields.Char(string="Name")
    sh_title=fields.Char(string="Title")
    sh_document_no=fields.Char(string="Document Number")
    sh_revision_no=fields.Char(string="Revision No.")
    sh_parent_id=fields.Many2one('sh.knowledge.article',string="Parent Document")
    sh_child_id = fields.One2many('sh.knowledge.article', 'sh_parent_id', string='Children Article')
    state=fields.Selection([('draft','Draft'),('submit','Submit To Manager'),('approved','Approved'),('reject','Reject')],default="draft")
    stage_id=fields.Many2one("sh.sop.stages",default=_get_default_stage_id,ondelete='restrict',string="Stages")
    sh_create_date=fields.Date(string="Created Date")
    effective_date=fields.Date(string="Modified Date")        
    sh_content=fields.Html(string="Content",store=True, readonly=False)
    banner = fields.Html(string="Cover Page")
    owner_id = fields.Many2one('res.users', default=lambda self: self.env.user)
    icon = fields.Binary(related='owner_id.image_1920')
    sh_category_id = fields.Many2one("sh.article.categories",string="Article Category")
    sh_tag_ids =fields.Many2many("sh.article.tags",string="Tags")
    active = fields.Boolean(default=True, help="It's hide of article view.")
    recuring_review_process_date = fields.Date(string="Review Process Date")
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
        default=lambda self: self.env.company)
    # sh_department_id=fields.Many2one('sh.helpdesk.team',string="Department")
    # sh_sub_department_id=fields.Many2one('sh.sub.department',string="Sub Department")
    # sh_process_id=fields.Many2one('sh.processes',string="Process")
    # sh_subprocess_id=fields.Many2one('sh.sub.processes',string="Sub Process")
    owner_ids=fields.Many2many("res.users",string="Owners",default=lambda self: self.env.user)
    manager_ids=fields.Many2many("res.users","res_users_manger_rel",string="Managers",default=_get_default_manager_id)
    submited_stage=fields.Many2one("sh.sop.stages",related="company_id.sh_draft_sop_id")
    # sh_approve=fields.Boolean(default=False,compute="_sh_approve")    
    sh_owner=fields.Boolean(default=False)
    
    # sh_artical_type = fields.Selection(
    #     selection=[
    #         ('knowledge_base', 'Knowledge Base'),
    #         ('sop_base', 'SOP Base'),
    #     ],default='sop_base',required=True,string='Artical Type')
    knowledge_state=fields.Selection([('draft','Draft'),('published','Published')],default="draft",string='State')

    # def _sh_approve(self):
    #     for rec in self:
    #         if rec.owner_ids.ids:
    #             if self.env.user.id in rec.owner_ids.ids:
    #                 rec.sh_owner=True
    #             else:
    #                 rec.sh_owner=False
    #         else:
    #             rec.sh_owner=False
    #         if rec.manager_ids.ids:
    #             if self.env.user.id in rec.manager_ids.ids:
    #                 rec.sh_approve=True
    #             else:
    #                 rec.sh_approve=False
    #         else:
    #             rec.sh_approve=False



    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'sh_document_no' in vals and vals.get('sh_document_no') and 'sh_revision_no' in vals and vals.get('sh_revision_no'):
                vals['name'] = vals['sh_document_no']+"/"+str(vals['sh_revision_no'])
            vals['sh_create_date'] = fields.Date.today()      

        res_ids = super(ShKnowledgeArtical, self).create(vals_list)
        if res_ids:
            for res in res_ids:
                if res.sh_category_id:
                    if res.sh_category_id.sh_responsible_user_id :
                        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                        self.env['user.push.notification'].push_notification([res.sh_category_id.sh_responsible_user_id],'New Knowledge Artical Created :','Knowledge ref %s'% (res.sh_title),base_url+"/mail/view?model=sh.knowledge.article&res_id="+str(res.id),'sh.knowledge.article', res.id,'hr')


        return res_ids
    
    def write(self, vals):
        for rec in self:
            if 'sh_document_no' in vals and vals.get('sh_document_no') and 'sh_revision_no' in vals and vals.get('sh_revision_no'):
                    vals['name'] = vals['sh_document_no']+"/"+str(vals['sh_revision_no'])
            elif rec.sh_document_no and 'sh_revision_no' in vals and vals.get('sh_revision_no'):
                vals['name'] =rec.sh_document_no+"/"+str(vals['sh_revision_no'])
            elif  'sh_document_no' in vals and vals.get('sh_document_no'):
                    vals['name'] = vals['sh_document_no']+"/"+str(rec.sh_revision_no)
            vals['effective_date']= fields.Date.today()
        res = super(ShKnowledgeArtical, self).write(vals)       
        return res
    

    _sql_constraints = [
        ('uniq_name', 'unique(name)', 'name must be unique please check name and revision number!'),
    ]


    # def update_document(self):        
    #     vals={}        
    #     if self.sh_document_no:
    #         vals.update({
    #             'default_sh_document_no':self.sh_document_no,
    #         })        
    #     if self.id:
    #         vals.update({
    #             'default_sh_parent_id':self.id,
    #         })

    #     if self.sh_content:
    #         vals.update({
    #             'default_sh_content':self.sh_content,
    #         })    

    #     if self.icon:
    #         vals.update({
    #             'default_icon':self.icon,
    #         })    
    #     if self.banner:
    #         vals.update({
    #             'default_banner':self.banner,
    #         })
    #     return {
    #         'name':'Update Articale',
    #         'res_model':'sh.knowledge.article.wizard',
    #         'view_mode':'form',
    #         'view_id': self.env.ref('sh_knowledge_base_customised.sh_knowledge_article_wizard').id,
    #         'target': 'new',
    #         'type':'ir.actions.act_window',
    #         'context': vals
    #     }