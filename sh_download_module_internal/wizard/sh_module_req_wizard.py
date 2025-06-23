# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from datetime import datetime
import uuid
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ShModuleReq(models.TransientModel):
    _name = 'sh.module.req.wizard'
    _description = 'Employee can request the module from here'

    for_which = fields.Selection([
        ('project', 'Project'),
        ('ticket', 'Ticket')
    ], string='For Which', default='project')
    project_id = fields.Many2one('project.project', string='Project')
    task_id = fields.Many2one('project.task', string='Task')
    # product_task_ids = fields.Many2many('project.task', string='Product Task')
    product_ids = fields.Many2many('product.product', string='Product Variants')
    ticket_id = fields.Many2one('sh.helpdesk.ticket', string='Ticket')
    # product_ids = fields.Many2many(related='ticket_id.product_ids', string='Products')
    btn_already_pressed = fields.Boolean("Button Already Pressed ?")
    req_ref = fields.Char('Request Reference')


    @api.onchange('for_which')
    def _onchange_for_which(self):
        self.ensure_one()
        self.update({
            'project_id': False,
            'task_id': False,
            # 'product_task_ids': False,
            'product_ids': False,
            'ticket_id': False
        })
        if self.for_which == 'ticket':
            self.project_id = self.env.company.appstore_project_id.id

    def btn_module_request(self):
        if self.btn_already_pressed:
            return False
        self.btn_already_pressed = True
        if self.for_which == 'ticket':
            if not self.ticket_id:
                raise UserError(_("Please enter the ticket !"))
            if not self.ticket_id.product_ids:
                raise UserError(_(f"Ticket({self.ticket_id.name}) doesn't contain the Module/Product, Please ensure that 'Product' field value is set on that ticket !"))

        return {
            # 'close': True,
            'type': 'ir.actions.act_url',
            'url': f"/github/sh_download_module_internal?wizard_id={self.id}",
            'target': 'self'
        }

    def _log(self, module_list, for_migration=False):
        '''Manage the log when downloading the modules'''
        self.env['sh.download.module.log'].create({
            'module_ids': [(6, 0, [module.id for module in module_list])],
            'for_which': self.for_which,
            'project_id': self.project_id.id,
            'task_id': self.task_id.id,
            'ticket_id': self.ticket_id.id,
            'is_for_migration': for_migration
        })

    def _req(self, not_access_list):
        req_obj = self.env['sh.download.module.req'].with_context(from_wizard=True).create({
            'module_ids': [(6, 0, [module.id for module in not_access_list])],
            'for_which': self.for_which,
            'project_id': self.project_id.id,
            'task_id': self.task_id.id,
            'ticket_id': self.ticket_id.id,
            'request_token': str(uuid.uuid4())
        })
        self.req_ref = req_obj.id

        # Bell Notification
        user_objs = self.env['res.users'].search([
            ('groups_id', '=', self.env.ref('sh_download_module_internal.sh_appstore_module_req_manager').id)
        ])

        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for user_obj in user_objs:
            self.env['user.push.notification'].push_notification(
                list_of_user_ids=[user_obj],
                title=f"{user_obj.name}'s Module Request",
                message=f"For modules: {', '.join([module.name for module in not_access_list])}",
                link=f'{base_url}/mail/view?model=sh.download.module.req&res_id={str(req_obj.id)}',
                res_model='sh.download.module.req',
                res_id=req_obj.id,
                type='project'
            )

    def _message_popup(self, message):
        '''Failed message pop-up'''
        self.env['bus.bus']._sendone(self.env.user.partner_id, 'simple_notification', {
            'type': 'success',
            'sticky':True,
            'title': _("Module Request"),
            'message': _(message),
        })

    # ------------------------------------------
    #  Create Activity
    # ------------------------------------------

    def _generate_activity(self, users):
        if not users:
            return
        if self.for_which != 'project':
            return
        # Don't create the Billing activity for the Appstore Project
        if self.project_id.id == self.env.company.appstore_project_id.id:
            return
        # if not self.activity_user_ids:
        #     return

        # note = f"Billing Activity for project '{self.project_id.name}'"
        products = []
        for product in self.product_ids:
            # print(f"\n\n\n\t--------------> 126 product.name",product.name)
            # print(f"\n\n\n\t--------------> 127 product_template_variant_value_ids",product.product_template_variant_value_ids.name)
            # print(f"\n\n\n\t--------------> 128 sh_technical_name",product.sh_technical_name)
            products.append(f"{product.name}({product.sh_technical_name}) - {product.product_template_variant_value_ids.name}")
        note = f"{', '.join(products)}"


        res_model_id = self.env['ir.model'].sudo().search([
            ('model', '=', 'project.task')
        ], limit=1)
        for user in users:

            activity = self.env['mail.activity'].search([
                ('user_id', '=', user.id),
                ('res_model', '=', 'project.task'),
                ('res_id', '=', self.task_id.id),
                ('note', '=', note),
                ('res_model_id', '=', res_model_id.id),
            ], limit=1)
            if not activity:
                activity = self.env['mail.activity'].create({
                    'res_model_id': res_model_id.id,
                    'user_id': user.id,
                    'res_model': 'project.task',
                    'res_id': self.task_id.id,
                    'activity_type_id': self.env.company.sh_billing_activity.id,
                    'note': note,
                    'date_deadline': datetime.now(),
                })


class ProductProduct(models.Model):
    _inherit='product.product'
    _description='product product'

    def name_get(self):

        if self.env.context.get('sh_module_req_wizard'):
            return [
                (product.id, '('+ product.product_template_variant_value_ids.name +') ' + product.name)
                for product in self
            ]
        return super().name_get()