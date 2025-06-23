# Copyright (C) Softhealer Technologies.

from odoo import models,  _
from odoo.exceptions import AccessDenied, UserError
from odoo.http import request
import logging
from decorator import decorator

_logger = logging.getLogger(__name__)

ACTION_DICT = {
    'view_type': 'form',
    'view_mode': 'form',
    'res_model': 'base.module.upgrade',
    'target': 'new',
    'type': 'ir.actions.act_window',
}


def assert_log_admin_access(method):
    """Decorator checking that the calling user is an administrator, and logging the call.

    Raises an AccessDenied error if the user does not have administrator privileges, according
    to `user._is_admin()`.
    """
    def check_and_log(method, self, *args, **kwargs):
        user = self.env.user
        origin = request.httprequest.remote_addr if request else 'n/a'
        log_data = (method.__name__, self.sudo().mapped(
            'name'), user.login, user.id, origin)
        if not self.env.is_admin():
            _logger.warning(
                'DENY access to module.%s on %s to user %s ID #%s via %s', *log_data)
            raise AccessDenied()
        _logger.info(
            'ALLOW access to module.%s on %s to user %s #%s via %s', *log_data)
        return method(self, *args, **kwargs)
    return decorator(check_and_log, method)


class Module(models.Model):
    _inherit = "ir.module.module"

    @assert_log_admin_access
    def button_upgrade(self):
        dependency = self.env['ir.module.module.dependency'].sudo()
        self.update_list()

        todo = list(self)
        i = 0
        while i < len(todo):
            module = todo[i]
            i += 1

            self.check_external_dependencies(module.name, 'to upgrade')
            for dep in dependency.search([('name', '=', module.name)]):
                if dep.module_id.state == 'installed' and dep.module_id not in todo:
                    todo.append(dep.module_id)

        self.browse(module.id for module in todo).write(
            {'state': 'to upgrade'})

        to_install = []
        for module in todo:
            for dep in module.dependencies_id:
                if dep.state == 'unknown':
                    raise UserError(_('You try to upgrade the module %s that depends on the module: %s.\nBut this module is not available in your system.') % (
                        module.name, dep.name,))
                if dep.state == 'uninstalled':
                    to_install += self.search([('name', '=', dep.name)]).ids

        self.browse(to_install).button_install()
        return dict(ACTION_DICT, name=_('Apply Schedule Upgrade'))
