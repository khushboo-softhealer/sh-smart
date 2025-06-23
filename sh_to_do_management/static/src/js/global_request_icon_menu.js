
odoo.define("sh_to_do_management.sh_emp_task_assignment_menulist", function (require) {
    "use strict";

    var { global_request_menulist } = require("sh_global_requests.global_request_menulist")

    global_request_menulist.include({
        /**
         * @override
         */
        events: _.extend({}, global_request_menulist.prototype.events, {
            "click span.assignment_global": function (event) {
                event.stopPropagation();
                event.preventDefault();
                this.do_action({
                    name: "Assignment",
                    type: "ir.actions.act_window",
                    view_type: "form",
                    view_mode: "form",
                    views: [[false, "form"]],
                    res_model: "sh.employee.task.allocation.wizard",
                    target: "new",
                });
            },

        }),
    });
});