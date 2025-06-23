
# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields,models
import requests
import json
from datetime import datetime

class InheritImportBase(models.Model):
    _inherit = "sh.import.base"
    
    def process_mail_follower_data(self,data):
        ''' ============= Prepare follower Follower related task list =============  '''
        mail_follower_ids=[]
        for follower in data:
            follower_vals={
                'remote_mail_followers_id':follower.get('id'),
                'display_name':follower.get('display_name'),
                'res_model':follower.get('res_model'), 
                # 'res_id':follower.get('res_id'),
            }
            # ======== Get Partner if already created or create =========
        
            if follower.get('partner_id'):
                domain = [('remote_res_partner_id', '=', follower.get('partner_id'))]
                find_customer = self.env['res.partner'].search(domain)
                if find_customer:
                    follower_vals['partner_id']=find_customer.id
                
            # ============== CONNECT subtype_ids WITH MAIL FOLLOWER =================
            if follower.get('subtype_ids'):
                subtype_list=[]
                for subtype in follower.get('subtype_ids'):
                    domain = [('remote_mail_message_subtype_id', '=', subtype)]
                    find_subtype = self.env['mail.message.subtype'].search(domain,limit=1)        
                    if find_subtype:
                        subtype_list.append((4,find_subtype.id))

                if subtype_list:
                    follower_vals['subtype_ids']=subtype_list 
                
            find_follower = self.env['mail.followers'].search([('remote_mail_followers_id','=',follower.get('id'))])
            print("\n\n======find_follower",find_follower)
            if not find_follower:
                mail_follower_ids.append((0,0,follower_vals)) 
            else:
                find_follower.write(follower_vals)
        print("\n\n-------mail_follower_ids",mail_follower_ids)
        return mail_follower_ids               