# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models


class ShHighFive(models.Model):
    _name = "sh.high.five"
    _description = "High Five Menu For BR-enage"

    name = fields.Char("Your High Five")
    sh_high_five_creation_date = fields.Text("Date Of Creation")
    sh_from_user_id = fields.Many2one('res.users', "From User")
    sh_to_user_id = fields.Many2one('res.users', "To User")
    sh_parent_id = fields.Many2one("sh.high.five", string="Parent High Five")
    sh_child_ids = fields.One2many("sh.high.five", "sh_parent_id", string="Child High Fives")
    sh_liked_by_ids = fields.Many2many('res.users', string="Store Liked By Ids")
    sh_is_private_comment = fields.Boolean("Is Private Comment")
    sh_third_mention_id = fields.Many2one("res.users", string="Third Person Mention")
    sh_manage_badges_id = fields.Many2one("sh.manage.badge", string="Manage Badges")
    sh_high_five_create_date_search = fields.Date("Create Date")



    def create(self,vals):
        res = super(ShHighFive,self).create(vals)
        # self.env['sh.br.engage.push.notification'].new_notification_method_for_test(user=self.env.user,name="Manage Question",description="Manage Question Edited",res_model="sh.manage.questions",res_id=self.id)
        self.env['user.push.notification'].high_five_realtime_update(user=res.sh_from_user_id)
        self.env['user.push.notification'].high_five_realtime_update(user=res.sh_to_user_id)
        return res