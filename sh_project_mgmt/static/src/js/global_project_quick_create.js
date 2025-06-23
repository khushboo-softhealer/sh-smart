
odoo.define("sh_project_mgmt.sh_project_quick_create_menulist", function (require) {
    "use strict";

    var { global_request_menulist } = require("sh_global_requests.global_request_menulist")

    global_request_menulist.include({
        /**
         * @override
         */
        events: _.extend({}, global_request_menulist.prototype.events, {

            "click span.project_global": function (event) {
                event.stopPropagation();
                event.preventDefault();
                this.do_action({
                    name: "Project",
                    type: "ir.actions.act_window",
                    view_type: "form",
                    view_mode: "form",
                    views: [[false, "form"]],
                    res_model: "sh.project.create.wizard",
                    target: "new",
                });
            }

        }),
    });
});