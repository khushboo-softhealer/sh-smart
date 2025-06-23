# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, _
from lxml import etree
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

class SOPArtical(models.Model):
    _name = 'sh.sop.article'
    _description = 'SOP Article'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _rec_name = 'sh_document_no'


    def _get_default_stage_id(self):
        return self.env['sh.sop.stages'].search([], limit=1,order='id asc')

    def _get_default_manager_id(self):
        if self.env.user.employee_id and self.env.user.employee_id.coach_id:
            coach_id=self.env.user.employee_id.coach_id
            if coach_id.user_id:
                return coach_id.user_id

    name=fields.Char(string="Name")
    sh_title=fields.Char(string="Title", required=True)
    sh_document_no=fields.Char(string="Document Number",default="New")
    # sh_revision_no=fields.Integer(string="Revision No.")
    sh_revision_no = fields.Char(string="Revision No.")
    sh_parent_id=fields.Many2one(comodel_name='sh.sop.article',string="Parent Document")
    sh_child_id = fields.One2many(comodel_name='sh.sop.article',inverse_name= 'sh_parent_id', string='Children Article')
    state=fields.Selection([('draft','Draft'),('submit','Submit To Manager'), ('revision','Revision') ,('publish','Publish'),('reject','Reject'),('cancel','Cancel')],default="draft",tracking=True)
    stage_id=fields.Many2one("sh.sop.stages",default=_get_default_stage_id,ondelete='restrict',string="Stages")
    sh_create_date=fields.Date(string="Created Date")
    approve_date=fields.Date(string="Approved Date")
    approve_by=fields.Many2one('res.users',string="Approved By")
    review_date =fields.Date(string="Review Date")
    review_by=fields.Many2one('res.users',string="Review By")
    effective_date=fields.Date(string="Modified Date")
    sh_content=fields.Html(string="Content",store=True, readonly=False)
    banner = fields.Html(string="Cover Page")
    owner_id = fields.Many2one('res.users',default=lambda self: self.env.user)
    icon = fields.Binary(related='owner_id.image_1920')
    sh_category_id = fields.Many2one("sh.sop.article.categories",string="SOP Article Category")
    sh_tag_ids =fields.Many2many("sh.sop.article.tags",string="Tags")
    active = fields.Boolean(default=True, help="It's hide of article view.", string="Archive")
    recuring_review_process_date = fields.Date(string="Review Process Date")
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
        default=lambda self: self.env.company)
    sh_department_id=fields.Many2one('sh.helpdesk.team',string="Department")
    sh_sub_department_id=fields.Many2one('sh.sub.department',string="Sub Department")
    sh_process_id=fields.Many2one('sh.processes',string="Process")
    sh_subprocess_id=fields.Many2one('sh.sub.processes',string="Sub Process")
    owner_ids=fields.Many2many("res.users",string="Owners",default=lambda self: self.env.user,readonly=True)
    manager_ids=fields.Many2many("res.users","res_users_manger_sop_rel",string="Managers",default=_get_default_manager_id,readonly=True)
    submited_stage=fields.Many2one("sh.sop.stages",related="company_id.sh_draft_sop_id")
    sh_approve=fields.Boolean(default=False,compute="_sh_approve")
    sh_owner=fields.Boolean(default=False)
    knowledge_state=fields.Selection([('draft','Draft'),('published','Published')],default="draft",string='State')
    sh_url_ref=fields.Char  ('Reference')
    # sh_department_ids = fields.Many2many(related='sh_category_id.department_ids', string="Departments")
    # sh_user_ids = fields.Many2many(related='sh_category_id.user_ids', string="Users")
    department_ids = fields.Many2many('hr.department', string="Departments")
    sh_user_ids = fields.Many2many('res.users','sh_sop_article_user_id','sh_parent_id','user_id', default=lambda self: self.env.user, string="Users")
    sh_department_user_ids = fields.Many2many('res.users','sh_sop_article_department_user_rel','sh_parent_id','user_id',store=True,compute='_compute_sh_department_user_ids')
    is_coach = fields.Boolean(compute="_compute_is_coach_id")
    revision_count = fields.Integer()
    record_to_archive_id = fields.Integer()
    is_coach_or_owner = fields.Boolean(compute="_compute_is_coach_or_owner", default=True)
    is_owner = fields.Boolean(compute="_compute_is_owner")

    def _compute_is_owner(self):
        for rec in self:
            rec.is_owner = False
            if rec.owner_id.id == self.env.user.id:
                rec.is_owner = True

    def _compute_is_coach_or_owner(self):
        for rec in self:
            rec.is_coach_or_owner = False
            if rec.env.user.has_group('sh_project_task_base.group_project_officer'):
                rec.is_coach_or_owner = True
            elif rec.owner_id.id == self.env.user.id:
                rec.is_coach_or_owner = True

    def _compute_is_coach_id(self):
        for rec in self:
            rec.is_coach = False
            if rec.env.user.has_group('sh_project_task_base.group_project_officer'):
                rec.is_coach = True


    @api.depends('department_ids')
    def _compute_sh_department_user_ids(self):
        for rec in self:
            rec.sudo().sh_department_user_ids = [(6, 0, self.sudo().department_ids.mapped('member_ids.user_id').ids)]
            # rec.sudo().write({'sh_department_user_ids':self.sudo().department_ids.mapped('member_ids.user_id').ids})

    def sh_revision_manager(self):
        for rec in self:
            rec.state = 'draft'

    def sh_sop_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    def action_archive_record(self):
        for record in self:
            # Check if the current user is the owner
            if record.owner_id.id == self.env.uid:
                record.write({'active': False})  # Archive the record

    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        if ('name' not in default):
            default['name'] = _("%s (copy)", self.name)
        return super(SOPArtical, self).copy(default)

    def sh_revision_user(self):
        if self.state == 'publish':
            self.revision_count += 1
            temp_sh_revision_no = int(self.sh_revision_no)
            temp_sh_revision_no += 1
            self.sh_revision_no = str(temp_sh_revision_no)

            revision_rec = self.sudo().copy()
            revision_rec.sh_document_no =  revision_rec.sh_document_no.split('/')[0] +'/'+str(self.revision_count)
            revision_rec.sh_title = revision_rec.sh_document_no + ' - ' + revision_rec.sh_title.split('-')[1] if len(revision_rec.sh_title.split('-')) >= 2  else ''

            revision_rec.sh_user_ids = self.sh_user_ids
            revision_rec.department_ids = self.department_ids
            revision_rec.manager_ids = self.manager_ids
            revision_rec.sh_department_user_ids = self.sh_department_user_ids
            revision_rec.manager_ids = self.manager_ids

            # Todo
            # revision_rec.message_follower_ids = self.message_follower_ids
            # revision_rec.activity_ids = self.activity_ids
            # revision_rec.message_ids = self.message_ids

            if self.revision_count == 1:
                revision_rec.record_to_archive_id = self.id
        else:
            # self.state = 'draft'
            self.state = 'revision'
            # self.sh_revision_no += 1
            temp_sh_revision_no = int(self.sh_revision_no)
            temp_sh_revision_no += 1
            self.sh_revision_no = str(temp_sh_revision_no)

    def _sh_approve(self):
        for rec in self:
            if rec.owner_ids.ids:
                if self.env.user.id in rec.owner_ids.ids:
                    rec.sh_owner=True
                else:
                    rec.sh_owner=False
            else:
                rec.sh_owner=False
            if rec.manager_ids.ids:
                if self.env.user.id in rec.manager_ids.ids:
                    rec.sh_approve=True
                else:
                    rec.sh_approve=False
            else:
                rec.sh_approve=False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # TODO check seq
            print("\n\n\n\n vals",vals)
            vals['sh_user_ids'] = [(4, self.env.user.id)]

            if not 'revision_count' in vals:
                if vals.get('sh_document_no', 'New') == 'New':
                    vals['sh_document_no'] = self.env['ir.sequence'].next_by_code('sh.sop.article.sequence') or 'New'

                if 'sh_document_no' in vals and vals.get('sh_document_no') and 'sh_revision_no' in vals and vals.get('sh_revision_no'):
                    vals['name'] = vals['sh_document_no']+"/"+str(vals['sh_revision_no'])
                vals['sh_create_date'] = fields.Date.today()
                if vals['sh_title']:
                    vals['sh_title'] = vals['sh_document_no'] + ' - ' + vals['sh_title']

        res_ids = super(SOPArtical, self).create(vals_list)


        if res_ids:
            for res in res_ids:
                if res.sh_category_id:
                    # category=self.env['sh.article.categories'].browse(res.sh_category_id)
                    if res.sh_category_id.sh_responsible_user_id:
                        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                        self.env['user.push.notification'].push_notification([res.sh_category_id.sh_responsible_user_id],'New SOP Created :','SOP ref %s'% (res.sh_title),base_url+"/mail/view?model=sh.sop.article&res_id="+str(res.id),'sh.sop.article', res.id,'hr')

        return res_ids

    def write(self, vals):
        for rec in self:
            if 'sh_document_no' in vals and vals.get('sh_document_no') and 'sh_revision_no' in vals and vals.get('sh_revision_no'):
                    vals['name'] = vals['sh_document_no']+"/"+str(vals['sh_revision_no'])
            elif rec.sh_document_no and 'sh_revision_no' in vals and vals.get('sh_revision_no'):
                vals['name'] =rec.sh_document_no+"/"+str(vals['sh_revision_no'])
            elif 'sh_document_no' in vals and vals.get('sh_document_no'):
                    vals['name'] = vals['sh_document_no']+"/"+str(rec.sh_revision_no)
            vals['effective_date']= fields.Date.today()
        res = super(SOPArtical, self).write(vals)
        return res


    # _sql_constraints = [
    #     ('uniq_name', 'unique(banner)', 'name must be unique please check name and revision number!'),
    # ]

    def sh_submit_manager(self):
         self.write({'state':'submit','stage_id':self.company_id.sh_submit_manager_id.id,'review_date':fields.Date.today(),'review_by':self.env.user.id,'active':True})

    # def sh_review(self):
    #     self.write({'state':'review','review_date':fields.Date.today(),'review_by':self.env.user.id,'active':True})
    def sh_approve_button(self):
        if self.record_to_archive_id:
            self.browse(self.record_to_archive_id).active = False
            self.state = 'publish'
            self.record_to_archive_id = self.id
        else:
            self.state = 'publish'
        self.approve_date = fields.Date.today()
        self.approve_by = self.env.user.id
        # if self.sh_revision_no and self.sh_document_no:
        #     self.write({'state':'approved','sh_document_no':self.sh_document_no,'stage_id':self.env.company.sh_approved_id.id,'approve_date':fields.Date.today(),'approve_by':self.env.user.id,'active':True})
        # else:
        #     raise UserError(_('Revision Number Is Required !'))
    def sh_reject(self):
        # self.write({'state':'reject','stage_id':self.env.company.sh_reject_id.id,'active':False})
        self.write({'state': 'reject', 'active': False})

    def sh_draft(self):
        self.write({'state':'draft','stage_id':self.env.company.sh_draft_sop_id.id,'active':True})


    @api.onchange('sh_category_id')
    def _on_change_sh_category_id(self):
        self.write({'department_ids': [(6, 0, self.sh_category_id.mapped('department_ids').ids)],
                    'sh_user_ids': [(6, 0, self.sh_category_id.mapped('user_ids').ids)]})

    def sh_reset_to_draft(self):
        self.write({'state':'draft'})

