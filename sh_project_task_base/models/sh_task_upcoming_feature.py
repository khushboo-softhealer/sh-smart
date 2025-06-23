# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models, api
from odoo.tools import html2plaintext


class ShTaskUpcomingFeature(models.Model):
    _name = "sh.task.upcoming.feature"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Upcoming Task Feature"

    name = fields.Char('Name')
    # suggested_by_id = fields.Many2one(
    #     'res.users', string='Suggested By', tracking=True)
    state_id = fields.Many2one('sh.cr.state', string='State', tracking=True)
    date = fields.Date(default=fields.Date.today, tracking=True)
    user_id = fields.Many2one(
        "res.users", default=lambda self: self.env.user, readonly=1, string="Suggested By", tracking=True)
    description = fields.Html("Description", tracking=True)
    task_id = fields.Many2one("project.task", tracking=True)
    ref_task_id = fields.Many2one(
        "project.task", "Reference Task", tracking=True)
    company_id = fields.Many2one(
        'res.company', string='Company', default=lambda self: self.env.company)

    @api.model_create_multi
    def create(self, vals_list):
        all_cr = super(ShTaskUpcomingFeature, self).create(vals_list)
        for cr in all_cr:
            update_vals = {}
            state = self.env['sh.cr.state'].sudo().search([
                ('is_default_state', '=', True)
            ], limit=1)
            if state:
                update_vals['state_id'] = state.id
            update_vals['name'] = self.env['ir.sequence'].next_by_code(
                'sh.cr.seq') or 'New'
            # update_vals['suggested_by_id'] = self.env.user.id
            cr.sudo().write(update_vals)
        return all_cr

    def write(self, vals):
        # Check for log note for Decription tracing
        log_note = False
        before_description = False
        if vals.get('description'):
            log_note = True
            before_description = html2plaintext(self.description or "")
        # Override write method
        status = super(ShTaskUpcomingFeature, self).write(vals)
        # Create a log note for Decription tracing
        if log_note:
            if not before_description:
                before_description = 'None'
            after_description = html2plaintext(self.description or "")
            if not after_description:
                after_description = 'None'
            log_note = "%s -> %s (Description)" % (before_description,
                                                   after_description)
            self.message_post(body=log_note)

        return status