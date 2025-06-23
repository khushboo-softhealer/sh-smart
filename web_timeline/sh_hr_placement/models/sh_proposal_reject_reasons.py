# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields


class ShProposalRejectedReason(models.Model):
    _name = "sh.proposal.reject.reasons"
    _description = "Sh Proposal Rejected Reason"

    name = fields.Char("Reason")
