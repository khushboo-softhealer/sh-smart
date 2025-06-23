# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields


class GitProject(models.Model):
    _inherit = 'project.project'

    gituser_name = fields.Char(
        "Github Username", compute="_add_github_usernames")

    def _add_github_usernames(self):
        final_name = ''
        for data in self.message_follower_ids:
            domain = [('partner_id', '=', data.partner_id.id)]
            find_user = self.env['res.users'].search(domain,limit=1)
            if find_user:
                domain = [('user_id', '=', find_user.id)]
                find_employee = self.env['hr.employee'].search(domain, limit=1)
                if find_employee:
                    if find_employee.gituser_name:
                        final_name += find_employee.gituser_name + ','
        self.gituser_name = final_name
