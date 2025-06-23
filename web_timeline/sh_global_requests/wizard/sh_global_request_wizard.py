# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models

# sh.idea approve Wizard

class GlobalRequestWizard(models.TransientModel):
    _name = 'sh.global.request.wizard'
    _description = 'Global Request Wizard'

    def _get_default_manager_id(self):
        if self.env.user.employee_id and self.env.user.employee_id.coach_id:
            coach_id=self.env.user.employee_id.coach_id
            if coach_id.user_id:
                return coach_id.user_id

    name = fields.Char(string='Title', required=True)
    request_type=fields.Selection([('idea','Idea'),('knowledge','Knowledge'),('sop','SOP'),('complain','Complain')],default="idea")
    sh_complain_category = fields.Many2one(
        'sh.complain.categories', string="Complain Category")
    sh_knowledge_sop_category_id = fields.Many2one("sh.article.categories",string="Article Category")
    sh_sop_category_id = fields.Many2one("sh.sop.article.categories",string="SOP Article Category")
    sh_idea_category = fields.Many2one(
        'sh.idea.categories', string="Idea Category")

    sh_content=fields.Html(string="Content",store=True, readonly=False)
    owner_ids=fields.Many2many("res.users",string="Owners",default=lambda self: self.env.user)
    manager_ids=fields.Many2many("res.users","res_users_manger_relation",string="Managers",default=_get_default_manager_id)

    def create_request(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        if self.request_type=='complain':
            complain_vals={
                'subject':self.name,
                'complain_category':self.sh_complain_category.id,
                'description':self.sh_content,
                'state':'waiting',
            }
            complain_id=self.env['sh.complain'].sudo().create(complain_vals)
            listt = []
            for user in complain_id.complain_category.responsible_persons:
                listt.append(user)
            self.env['user.push.notification'].push_notification(listt,'New Complain Created :','Complain ref %s'% (complain_id.subject),base_url+"/mail/view?model=sh.complain&res_id="+str(complain_id.id),'sh.complain', complain_id.id,'hr')

        elif self.request_type=='idea':
            idea_vals={
                'subject':self.name,
                'idea_category':self.sh_idea_category.id,
                'description':self.sh_content,
                'state':'waiting',
            }
            idea_id=self.env['sh.idea'].sudo().create(idea_vals)

            listt = []
            if idea_id.idea_category:
                for user in idea_id.idea_category.responsible_persons:
                    listt.append(user)
            self.env['user.push.notification'].push_notification(listt,'New Idea Created :','Idea ref %s'% (idea_id.subject),base_url+"/mail/view?model=sh.idea&res_id="+str(idea_id.id),'sh.idea', idea_id.id,'hr')

        elif self.request_type=='knowledge':
            knowledge_vals={
                'sh_title':self.name,
                'sh_category_id':self.sh_knowledge_sop_category_id.id,
                'sh_content':self.sh_content,
                'knowledge_state':'published',
            }
            self.env['sh.knowledge.article'].sudo().create(knowledge_vals)

        elif self.request_type=='sop':
            sop_vals={
                'sh_title':self.name,
                'sh_category_id':self.sh_sop_category_id.id,
                'sh_content':self.sh_content,
                'owner_ids':self.owner_ids,
                'manager_ids':self.manager_ids,
            }
            self.env['sh.sop.article'].sudo().create(sop_vals)