# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields


class HelpdeskStages(models.Model):
    _name = 'sh.helpdesk.stages'
    _description = "Helpdesk Stages"
    _order = 'sequence, id'
    _rec_name = 'name'

    name = fields.Char("Name", required=True)
    mail_template_ids = fields.Many2many(
        'mail.template', string='Mail Template')
    sh_next_stage = fields.Many2one(
        comodel_name='sh.helpdesk.stages',
        string='Next Stage',
    )

    sh_group_ids = fields.Many2many(
        comodel_name='res.groups',
        string='Groups'
    )
    is_cancel_button_visible = fields.Boolean(
        string='Is Cancel Button Visible ?'
    )
    is_done_button_visible = fields.Boolean(
        string='Is Resolved Button Visible ?'
    )
    sequence = fields.Integer(string="Sequence", default=1)
    fold = fields.Boolean(string='Folded in Kanban',
                          help='This stage is folded in the kanban view when there are no records in that stage to display.')
    sh_portal_stage_name = fields.Char('Portal Stage Name')
    sh_visible_to_support_user = fields.Boolean('Visible To Support User?')
