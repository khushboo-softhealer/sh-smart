# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.


from odoo import models, fields, api,SUPERUSER_ID


class Lead(models.Model):
    _inherit = 'crm.lead'

    sh_replied_status = fields.Selection([('staff_replied','Staff Replied'),('customer_replied','Customer Replied')],string="Replied Status")
    sh_replied_status_id = fields.Many2one('sh.replied.status',string='Replied Status ', index=True, group_expand='_read_group_replied_stage_ids',tracking=True)

    @api.model
    def _read_group_replied_stage_ids(self, stages, domain, order):
        all_stages = self.env['sh.replied.status'].sudo().search([])
        search_domain = [('id', 'in', all_stages.ids)]

        # perform search
        stage_ids = stages._search(
            search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    # def _compute_replied_status(self):
    #     for rec in self:
    #         status = 'staff_replied'
    #         message_id = self.env['mail.message'].sudo().search([('subtype_id','!=',self.env.ref('mail.mt_note').id),('res_id','=',rec.id),('model','=','crm.lead')],limit=1)
    #         if message_id:
    #             if message_id.author_id:
    #                 user_id = self.env['res.users'].sudo().search([('partner_id','=',message_id.author_id.id)],limit=1)
    #                 if user_id and user_id.has_group('base.group_portal'):
    #                     status = 'customer_replied'
    #                 elif user_id and not user_id.has_group('base.group_portal'):
    #                     status = 'staff_replied'
    #                 elif not user_id:
    #                     status = 'customer_replied'
    #         rec.sh_replied_status = status
    
    # @api.model
    # def _search_replied_status(self, operator, operand):
    #     staff_replied_leads = []
    #     customer_replied_leads = []
    #     for rec in self.search([]):
    #         if rec.sh_replied_status == 'staff_replied':
    #             staff_replied_leads.append(rec.id)
    #         elif rec.sh_replied_status == 'customer_replied':
    #             customer_replied_leads.append(rec.id)
        
    #     if operator == '=' and operand == 'staff_replied':
    #         return [('id', 'in', staff_replied_leads)]
    #     elif operator == '=' and operand == 'customer_replied':
    #         return [('id', 'in', customer_replied_leads)]
    #     else:
    #         return []

