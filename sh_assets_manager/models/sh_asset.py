# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import *
import math
import re
import werkzeug.exceptions
import base64


class Assets(models.Model):
    _inherit = ['mail.thread',
                'mail.activity.mixin']
    _name = "sh.asset"
    _description = "Asset Details"

    name = fields.Char("Name", required=True, tracking=True)
    asset_category_id = fields.Many2one("sh.asset.type",
                                        string="Asset Category",
                                        required=True, tracking=True)
    amount = fields.Integer(string="Amount", tracking=True)
    vendor_id = fields.Many2one(
        "res.partner", string="Vendor", tracking=True)
    bill_number = fields.Char(string="Bill Number",
                              tracking=True)
    employee_id = fields.Many2one(
        "hr.employee", string="Employee", tracking=True)
    warranty_date = fields.Date(
        string="Warranty Date", required=True, tracking=True)
    warranty_expiry_date = fields.Date(
        string="Warranty Expiry Date", required=True, tracking=True)
    warranty_month = fields.Integer(
        string="Warranty Month", required=True, tracking=True)

    allocated = fields.Boolean("Allocated", tracking=True)
    state = fields.Selection(
        [
            ("unused", "Unused"),
            ("running", "Running"),
            ("scrap", "Scrap"),
            ("repairing", "Repairing"),
        ],
        default="unused",
        tracking=True,
    )
    is_parent = fields.Boolean(string='Parent ', tracking=True)
    is_child = fields.Boolean(string='Child', tracking=True)
    parent = fields.Many2one('sh.asset', tracking=True)
    sh_ebs_barcode = fields.Char(
        string="Barcode", readonly=True, tracking=True)
    sh_ebs_barcode_img = fields.Binary(
        string="Barcode Image", readonly=True, tracking=True)
    sh_is_general_asset = fields.Boolean("Is General Asset", tracking=True)

    @api.constrains('sh_ebs_barcode')
    def _check_promo_code_constraint(self):
        """ Program code must be unique """
        for program in self.filtered(lambda p: p.sh_ebs_barcode):
            domain = [('id', '!=', program.id),
                      ('sh_ebs_barcode', '=', program.sh_ebs_barcode)]
            if self.search(domain):
                raise ValidationError(_('The program code must be unique!'))

    @api.onchange('warranty_date', 'warranty_month')
    def onchange_warranty_date(self):
        if self.warranty_date != False:
            date_obj = self.warranty_date
            expiry_date = date_obj + relativedelta(months=self.warranty_month)
            self.warranty_expiry_date = expiry_date

    @api.onchange('parent')
    def onchange_parent(self):
        emp_id = self.parent.employee_id.id
        self.employee_id = emp_id

    def action_mass_emp_update(self):
        return {
            'name':
            'Mass Employee Update',
            'res_model':
            'emp.mass.update.wizard',
            'view_mode':
            'form',
            'context': {
                'default_assets_ids':
                [(6, 0, self.env.context.get('active_ids'))]
            },
            'view_id':
            self.env.ref(
                'sh_assets_manager.sh_emp_update_wizard_form_view').id,
            'target':
            'new',
            'type':
            'ir.actions.act_window'
        }

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('employee_id'):
                vals['allocated'] = True
                vals['state'] = 'running'

        res = super(Assets, self).create(vals_list)
        ean = generate_ean(str(res.id))
        res.sh_ebs_barcode = ean

        try:
            barcode = self.env['ir.actions.report'].barcode('EAN13',
                                                            ean,
                                                            width=500,
                                                            height=90,
                                                            humanreadable=0)
            if barcode:
                res.sh_ebs_barcode_img = base64.b64encode(barcode)

        except (ValueError, AttributeError):
            raise werkzeug.exceptions.HTTPException(
                description='Cannot convert into barcode.')
        return res

    def write(self, vals):
        if 'employee_id' in vals:
            emp = vals.get('employee_id')
            if emp == False:
                vals['allocated'] = False
                vals['state'] = 'unused'
            else:
                vals['allocated'] = True
                vals['state'] = 'running'
        res = super(Assets, self).write(vals)
        return res


def ean_checksum(eancode):
    """returns the checksum of an ean string of length 13, returns -1 if
    the string has the wrong length"""
    if len(eancode) != 13:
        return -1
    oddsum = 0
    evensum = 0
    eanvalue = eancode
    reversevalue = eanvalue[::-1]
    finalean = reversevalue[1:]

    for i in range(len(finalean)):
        if i % 2 == 0:
            oddsum += int(finalean[i])
        else:
            evensum += int(finalean[i])
    total = (oddsum * 3) + evensum

    check = int(10 - math.ceil(total % 10.0)) % 10
    return check


def check_ean(eancode):
    """returns True if eancode is a valid ean13 string, or null"""
    if not eancode:
        return True
    if len(eancode) != 13:
        return False
    try:
        int(eancode)
    except:
        return False
    return ean_checksum(eancode) == int(eancode[-1])


def generate_ean(ean):
    """Creates and returns a valid ean13 from an invalid one"""
    if not ean:
        return "0000000000000"
    ean = re.sub("[A-Za-z]", "0", ean)
    ean = re.sub("[^0-9]", "", ean)
    ean = ean[:13]
    if len(ean) < 13:
        ean = ean + '0' * (13 - len(ean))
    return ean[:-1] + str(ean_checksum(ean))
