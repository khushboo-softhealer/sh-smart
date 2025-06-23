# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields


class FollowerDomain(models.Model):
    _name = 'sh.ticket.follower.domain'
    _description = 'Ticket Follower Domain'

    name = fields.Char('Domain Name',required=True)