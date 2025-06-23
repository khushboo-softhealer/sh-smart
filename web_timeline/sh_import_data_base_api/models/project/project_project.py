# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models

class ProjectProject(models.Model):
    _inherit = 'project.project'

    remote_project_project_id = fields.Char("Remote Project ID",copy=False)
    
    
class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    remote_project_task_type_id = fields.Char("Remote Project Task Type ID",copy=False)
    
class ProjectTag(models.Model):
    _inherit = 'project.tags'

    remote_project_tag_id = fields.Char("Remote Project Tag ID",copy=False)
    
class ProjectTask(models.Model):
    _inherit = 'project.task'

    remote_project_task_id = fields.Char("Remote Task ID",copy=False)
 
    
class ProjectStages(models.Model):
    _inherit = 'project.project.stage'

    remote_project_project_stage_id = fields.Char("Remote Project Stage ID",copy=False)

class PreDefineTaskLine(models.Model):
    _inherit = 'pre.define.task.line'

    remote_pre_define_task_line_id = fields.Char("Remote Pre Define Task Line ID",copy=False)


    
