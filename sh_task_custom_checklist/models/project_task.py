# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import fields, models, api, _
from odoo.exceptions import UserError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.depends('custom_checklist_ids')
    def _compute_custom_checklist(self):
        if self:
            for rec in self:
                total_cnt = self.env['task.custom.checklist.line'].search_count([
                    ('task_id', '=', rec.id)])
                compl_cnt = self.env['task.custom.checklist.line'].search_count([
                    ('task_id', '=', rec.id), ('state', '=', 'completed')
                ])

                if total_cnt > 0:
                    rec.custom_checklist = (100.0 * compl_cnt) / total_cnt
                else:
                    rec.custom_checklist = 0

    custom_checklist_ids = fields.One2many("task.custom.checklist.line",
                                           "task_id",
                                           string="Checklist")
    custom_checklist = fields.Float("Checklist Completed",
                                    compute="_compute_custom_checklist", digits=(12, 0))
    check_list = fields.Many2many('sh.task.checklist.template')

    def _show_message(self, message):
        ''' Show Message '''
        view = self.env.ref("sh_message.sh_message_wizard")
        context = dict(self._context or {})
        context["message"] = message
        return {
            "name": "Add Checklist",
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "sh.message.wizard",
            "views": [(view.id, "form")],
            "view_id": view.id,
            "target": "new",
            "context": context,
        }

    def _add_checklists_in_task(self, pt_checklists):
        task_count = checklist_added_tasks = already_has_checklists_count = 0
        for task in self:
            task_count += 1
            if task.custom_checklist_ids:
                already_has_checklists_count += 1
                continue
            # already_has_checklists = False
            # covered_checklist = []
            if not pt_checklists:
                return "Can't get the project task checklist templates !"
            line_list = []
            # already_task_checklists = task.custom_checklist_ids.mapped(
            #     'task_custom_checklist_id')
            for pt_checklist in pt_checklists:
                # Add the pt_checklists's checklists
                if not pt_checklist.sh_project_task_checklist_line:
                    continue
                for line in pt_checklist.sh_project_task_checklist_line:
                    if not line.checklist_template_ids:
                        continue
                    # ======== Prepare Section Vals ========
                    section = ''
                    is_first = True
                    for state in line.at_which_state_ids:
                        if not is_first:
                            section += ' | '
                        section += state.name
                        is_first = False
                    if section and line.from_wich_state_id:
                        section = f'{line.from_wich_state_id.name} -> {section}'
                    section_vals = {
                        'display_type': 'line_section',
                        'name': section,
                    }
                    section_is_not_added = True
                    # ======== Add Checklists ========
                    for checklist_tmpl in line.checklist_template_ids:
                        if not checklist_tmpl.checklist_ids:
                            continue
                        # ======== Prepare Note Vals ========
                        note_vals = {
                            'display_type': 'line_note',
                            'name': checklist_tmpl.name,
                        }
                        note_is_not_added = True
                        # ======== Add Checklists ========
                        for checklist in checklist_tmpl.checklist_ids:
                            # if already_task_checklists:
                            #     if checklist in already_task_checklists:
                            #         already_has_checklists = True
                            #         continue
                            # if checklist.id in covered_checklist:
                            #     continue
                            # ======== Add a Section ========
                            if section_is_not_added:
                                line_list.append((0, 0, section_vals))
                                section_is_not_added = False
                            # ======== Add a Note ========
                            if note_is_not_added:
                                line_list.append((0, 0, note_vals))
                                note_is_not_added = False
                            # ======== Add a Checklist ========
                            vals = {
                                'name': checklist.name,
                                'task_custom_checklist_id': checklist.id,
                                'description': checklist.description,
                                'pt_checklist_line_id': line.id
                            }
                            line_list.append((0, 0, vals))
                            # covered_checklist.append(checklist.id)
            if line_list:
                task.custom_checklist_ids = line_list
                checklist_added_tasks += 1
            # elif already_has_checklists:
            #     already_has_checklists_count += 1
        message = ''
        if task_count:
            if checklist_added_tasks:
                task_count -= checklist_added_tasks
                message += f'Checklists added in the {checklist_added_tasks} tasks.\n'
            if already_has_checklists_count:
                task_count -= already_has_checklists_count
                message += f'{already_has_checklists_count} task(s) already have the checklists.\n'
            if task_count:
                message += f"Failed to add checklists in the {task_count} task(s) !\n"
                message += f"Reasons should be:\n"
                message += f"   - Project task checklist template doesn't contains any lines\n"
                message += f"   - Project task checklist templates lines doesn't contains any checklists"
        return message

    # ===========================
    #  Multi Action
    # ===========================

    def mul_action_add_checklists(self):
        return {
            "name": "Add Checklist",
            "type": "ir.actions.act_window",
            "res_model": "sh.add.checklist.wizard",
            "view_type": "form",
            "view_mode": "form",
            "view_id": self.env.ref("sh_task_custom_checklist.sh_add_checklist_wizard").id,
            "target": "new",
            "context": {
                'default_task_ids': [(6, 0, [task.id for task in self])]
            },
        }

    def mul_action_remove_checklists(self):
        message = ''
        remove_count = not_have_checklist_count = 0
        for task in self:
            if not task.custom_checklist_ids:
                not_have_checklist_count += 1
                continue
            checklist_list = [(2, checklist.id)
                              for checklist in task.custom_checklist_ids]
            if checklist_list:
                task.write({
                    'custom_checklist_ids': checklist_list
                })
                remove_count += 1
        if remove_count:
            message += f'Checklists remove from the {remove_count} task(s).'
        if not_have_checklist_count:
            message += f"\n{not_have_checklist_count} Task(s) doesn't contains any checklists to remove."
        if not message:
            message = "Task(s) doesn't contains any checklists."
        return self._show_message(message)

    # ===========================
    #  ORM Methods
    # ===========================

    def write(self, vals):
        from_state_id = self.stage_id
        res = super(ProjectTask, self).write(vals)
        if not vals.get('stage_id'):
            return res
        if not self.custom_checklist_ids:
            return res
        message = ''
        for checklist_line in self.custom_checklist_ids:
            if not (checklist_line.task_custom_checklist_id.accepted_state_ids and checklist_line.pt_checklist_line_id):
                continue
            if not checklist_line.pt_checklist_line_id.at_which_state_ids:
                continue
            # Task from state
            if from_state_id.id != checklist_line.pt_checklist_line_id.from_wich_state_id.id:
                continue
            # Tast to state
            if vals['stage_id'] not in checklist_line.pt_checklist_line_id.at_which_state_ids.ids:
                continue
            if checklist_line.state_id.id in checklist_line.task_custom_checklist_id.accepted_state_ids.ids:
                # Go forward (check list match with acceptable state)
                continue
            # else:
            state_list = []
            for state in checklist_line.task_custom_checklist_id.accepted_state_ids:
                state_list.append(state.name)
            message += f"\n   - Checklist '{checklist_line.name}' only accepted in the {state_list} state"
        if message:
            message = f'Please review the checklist before changing the task stage because:{message}'
            raise UserError(_(message))
        return res
