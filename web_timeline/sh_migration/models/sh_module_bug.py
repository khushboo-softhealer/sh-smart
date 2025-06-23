# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models, api
from datetime import datetime
from odoo.tools import html2plaintext
from bs4 import BeautifulSoup
import base64
import re
import requests
import mimetypes


class ShModuleBug(models.Model):
    _name = 'sh.module.bug'
    _description = 'Module Bug'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    # _order = 'name'

    name = fields.Char('Name', default='New')
    title = fields.Char('Title', tracking=True)
    # sequence = fields.Integer('Sequence', index=True, default=1)
    description = fields.Html('Description', tracking=True)
    bug_type = fields.Selection([
        ('bug', 'BUG'),
        ('cr', 'CR'),
        ('client_bug','CLIENT BUG'),
        ('client_cr','CLIENT CR'),
    ], string='Type', default='bug', tracking=True)
    bugs_for = fields.Selection([
        ('developer', 'Developer'),
        ('designer', 'Designer')
    ], string='Bugs For', default='developer', tracking=True)
    state_id = fields.Many2one('sh.bug.state', string='State', tracking=True)
    is_bug_state_testing = fields.Boolean(default=False)
    version = fields.Char('Version', tracking=True)
    resolved_by_id = fields.Many2one(
        'res.users', string='Resolved By', tracking=True)
    resolved_date = fields.Datetime('Resolved Date', tracking=True)
    root_cause = fields.Char('Root Cause', tracking=True)
    impact_on_business = fields.Selection(
        [
            ('p1', 'P1'),
            ('p2', 'P2'),
            ('p3', 'P3'),
        ],
        string='Impact On Business',
        help='''
            P1:- Impact on the operation we can not move forward
            P2 :- Impact on the reporting and others which is not part of the operations
            P3 :- Which is known issue can not solved as of now due to odoo standard..
            With P1 defect we can not move forward.
        ''',
        tracking=True
    )
    task_id = fields.Many2one('project.task', string='Task', tracking=True)
    project_id = fields.Many2one(
        'project.project', string='Project', related='task_id.project_id', store=True)
    is_appstore_project = fields.Boolean('Is Appstore Project', default=False)
    is_v17_task = fields.Boolean(
        'Is v17 Task', related='task_id.sh_migration_is_v17_task')
    company_id = fields.Many2one(
        'res.company', string='Company', default=lambda x: x.env.company)
    sh_bug_state_log_line = fields.One2many(
        'sh.bug.state.log', 'sh_bug_module_id', string='Bug State Log Line')
    link = fields.Text('Link', tracking=True)
    bug_counter = fields.Integer(
        "Repeat Counter", compute="_compute_bug_repeating_counter")
    major_code_changes_occured = fields.Boolean(default=False, tracking=True)
    
    def _create_bug_log(self):
        if self.sh_bug_state_log_line:
            return
        bug_line = {
            'state_id': self.state_id.id,
            'date_in': datetime.now(),
            'date_in_by': self.env.user.id,
        }
        self.sh_bug_state_log_line = [(0, 0, bug_line)]

    def _write_default_state(self):
        state = self.env['sh.bug.state'].sudo().search([
            ('is_default_state', '=', True)
        ], limit=1)
        if state:
            self.sudo().with_context({'first_bug_log': True}).write({
                'state_id': state.id
            })
            # self.state_id = state.id

    def _add_seq(self):
        if self.name and self.name != 'New':
            return
        seq = 'BUG'
        id_len = len(str(self.id))
        if id_len == 1:
            seq += '000'
        elif id_len == 2:
            seq += '00'
        elif id_len == 3:
            seq += '0'
        seq += str(self.id)
        self.sudo().with_context({'name_seq': True}).write({
            'name': seq
        })

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        active_ids = self._context.get('default_task_id')
        if active_ids:
            bug_task_id = self.env['project.task'].browse(active_ids)

            if bug_task_id and bug_task_id.stage_id.sh_is_uat:
                defaults['bug_type'] = "client_bug"
        return defaults

    @api.model_create_multi
    def create(self, vals_list):
        bugs = super(ShModuleBug, self).create(vals_list)
        for bug in bugs:
            if bug.project_id.id == bug.company_id.appstore_project_id.id:
                bug.is_appstore_project = True
            bug._add_seq()


            # bug.name = self.env['ir.sequence'].next_by_code(
            #     'sh.bug.seq') or 'New'
            bug._write_default_state()
            bug._create_bug_log()
        return bugs

    def _remove_images_from_html(self, html_content):
        """Removes all <img> tags from HTML content and returns clean text."""
        soup = BeautifulSoup(html_content, "html.parser")

        # Remove all image tags
        for img in soup.find_all("img"):
            img.decompose()

        # Get cleaned text without image URLs
        return soup.get_text().strip()

    def write(self, vals):
        # Check for log note for Description tracing
        log_note = False
        before_description = False
        after_description = False
        before_description = self._remove_images_from_html(self.description or "None")
        attachments = []

        if vals.get('description'):
            log_note = True
            after_description = self._remove_images_from_html(vals["description"])

            # Extract images from new description
            soup = BeautifulSoup(vals['description'], 'html.parser')
            img_tags = soup.find_all('img')

            for img in img_tags:
                img_url = img.get('src')

                if not img_url:
                    continue

                if img_url and img_url.startswith("http"):  # Check if it's an external URL
                    try:
                        response = requests.get(img_url, timeout=10)
                        if response.status_code == 200:
                            # Determine file extension
                            content_type = response.headers.get('Content-Type')
                            ext = mimetypes.guess_extension(content_type) or ".png"

                            # Create attachment in Odoo
                            attachment = self.env['ir.attachment'].create({
                                'name': f'image{ext}',
                                'datas': base64.b64encode(response.content),
                                'res_model': self._name,
                                'res_id': self.id,
                                'mimetype': content_type,
                            })
                            attachments.append(attachment.id)
                    except requests.RequestException:
                        continue  # Skip image if request fails

                elif "/web/image/" in img_url:
                    match = re.search(r"/web/image/(\d+)", img_url)
                    if match:
                        attachment_id = int(match.group(1))
                        attachments.append(attachment_id)

        # Override write method
        res = super(ShModuleBug, self).write(vals)
        # if (not self.name or self.name == 'New'):
        self._add_seq()
        # Create a log note for Description tracing
        if log_note:
            log_note = f"{before_description} -> {after_description} (Description)"
            if attachments:
                # Post message with attachments
                self.message_post(body=log_note, attachment_ids=attachments)
            else:
                self.message_post(body=log_note)

        # Create the first Bug log line
        if vals.get('state_id') and not self.env.context.get('first_bug_log'):
            self._create_bug_state_log()
        # Auto fill-up resolved by and resolved date
        # base on who change the state to testing
        if self.env.context.get('testing'):
            return res
        if vals.get('state_id'):
            if self.state_id and self.company_id.sh_migration_bug_testing_state_id:
                if self.state_id.id == self.company_id.sh_migration_bug_testing_state_id.id:
                    self.sudo().with_context({'testing': True}).write({
                        'resolved_by_id': self.env.user.id,
                        'resolved_date': datetime.now()
                    })
        return res

    def _create_bug_state_log(self):
        last_create_id = self.sh_bug_state_log_line.ids
        if last_create_id:
            previous_id = self.env['sh.bug.state.log'].browse(
                last_create_id[-1])
            sub_time = datetime.now() - previous_id.date_in

            # for days difference
            day_diff = sub_time.days

            # for hours difference
            test = str(sub_time.seconds//3600) + ':' + \
                str(((sub_time.seconds//60) % 60))
            vals = test.split(':')
            time, hours = divmod(float(vals[0]), 24)
            time, minutes = divmod(float(vals[1]), 60)
            minutes = minutes / 60.0
            time_to_fl = hours + minutes

            # for total time count
            if day_diff > 0:
                test = str(sub_time.seconds//3600) + ':' + \
                    str(((sub_time.seconds//60) % 60))
                vals = test.split(':')
                time, hours = divmod(float(vals[0]), 24)
                time, minutes = divmod(float(vals[1]), 60)
                minutes = minutes / 60.0
                hours += day_diff*24
                total_time_to_fl = hours + minutes
            else:
                total_time_to_fl = time_to_fl

            stage_history = {
                'date_out':  datetime.now(),
                'date_out_by': self.env.user,
                'day_diff': day_diff,
                'time_diff': time_to_fl,
                'total_time_diff': total_time_to_fl,
            }
            self.sh_bug_state_log_line = [
                (1, last_create_id[-1], stage_history)]

        # for new record====================
        stage_history = {
            'state_id': self.state_id.id,
            'date_in': datetime.now(),
            'date_in_by': self.env.user.id,
        }
        self.sh_bug_state_log_line = [(0, 0, stage_history)]

    # @api.depends('state_id')
    def _compute_bug_repeating_counter(self):
        domain = [('is_default_state', '=', True)]
        default_bug = self.env['sh.bug.state'].search(domain, limit=1)
        for rec in self:
            if default_bug:
                count = rec.sh_bug_state_log_line.filtered(
                    lambda x: x.state_id.id == default_bug.id)
                rec.bug_counter = len(count)
            else:
                rec.bug_counter = 0

    
    @api.onchange('state_id')
    def _onchange_state_id(self):
        if self.state_id.is_testing_state is True:
            self.is_bug_state_testing = True
        else:
            self.is_bug_state_testing = False
    
