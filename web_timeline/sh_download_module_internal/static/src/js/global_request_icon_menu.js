odoo.define("sh_download_module_internal.sh_download_module_internal_menulist", function (require) {
    "use strict";

    var {global_request_menulist} = require("sh_global_requests.global_request_menulist")

    global_request_menulist.include({
        /**
         * @override
         */
        events: _.extend({}, global_request_menulist.prototype.events, {
            "click span.sh_module_request_view": function (event) {
                event.stopPropagation();
                event.preventDefault();
                this.do_action({
                    name: "Module Request",
                    type: "ir.actions.act_window",
                    view_type: "form",
                    view_mode: "form",
                    views: [[false, "form"]],
                    res_model: "sh.module.req.wizard",
                    target: "new",
                });
            }
        }),
    });
});