// ===========================================
//	Quick Menu List
// ===========================================

odoo.define("sh_global_requests.global_request_menulist", function (require) {
    "use strict";

    var core = require("web.core");
    var Widget = require("web.Widget");
    var SystrayMenu = require("web.SystrayMenu");
    var _t = core._t;
    var session = require('web.session');

    var group_allow_global_request = false
    var allow_idea_global_request_access_group = false
    var allow_complain_request_access_group = false
    var allow_knowledge_request_access_group = false
    var allow_sop_request_access_group = false
    var allow_maintenance_request_access_group = false
    var allow_assignment_request_access_group = false
    var allow_project_create_access_group = false
    // document.addEventListener('click', alert(555));

    session.user_has_group("sh_global_requests.global_request_access_group").then(function (has_group) {
        group_allow_global_request = has_group;
    });

    session.user_has_group("sh_global_requests.allow_idea_global_request_access_group").then(function (has_group) {
        allow_idea_global_request_access_group = has_group;
    });

    session.user_has_group("sh_global_requests.allow_complain_request_access_group").then(function (has_group) {
        allow_complain_request_access_group = has_group;
    });
    session.user_has_group("sh_global_requests.allow_knowledge_request_access_group").then(function (has_group) {
        allow_knowledge_request_access_group = has_group;
    });
    session.user_has_group("sh_global_requests.allow_sop_request_access_group").then(function (has_group) {
        allow_sop_request_access_group = has_group;
    });
    session.user_has_group("sh_global_requests.allow_maintenance_request_access_group").then(function (has_group) {
        allow_maintenance_request_access_group = has_group;
    });
    session.user_has_group("sh_global_requests.allow_assignment_request_access_group").then(function (has_group) {
        allow_assignment_request_access_group = has_group;
    });
    session.user_has_group("sh_global_requests.allow_project_create_access_group").then(function (has_group) {
        allow_project_create_access_group = has_group;
    });


    var global_request_menulist = Widget.extend({
        template: "global.request.menu",

        events: {
            "click span.sh_request_management": "redirect_request_creation",
            "click a.sh_request_view": "redirect_request_direct_view",

            "click a.openDropdown": "open_quick_menu",
        },


        _onNotification: function ({ detail: notifications }) {
            for (var i = 0; i < notifications.length; i++) {
                var channel = notifications[i]['type'];
                // if (channel == 'sh.timer.render') {

            }
        },


        open_quick_menu: function (e) {

            if (allow_idea_global_request_access_group) {
                $('.idea_global').removeClass('d-none')
            }
            if (allow_complain_request_access_group) {
                $('.complain_global').removeClass('d-none')
            }
            if (allow_knowledge_request_access_group) {
                $('.knowledge_global').removeClass('d-none')
            }
            if (allow_sop_request_access_group) {
                $('.sop_global').removeClass('d-none')
            }
            if (allow_maintenance_request_access_group) {
                $('.maintenance_global').removeClass('d-none')
            }
            if (allow_assignment_request_access_group) {
                $('.assignment_global').removeClass('d-none')
            }
            if (allow_project_create_access_group) {
                $('.project_global').removeClass('d-none')
            }

            if ($('.sh_global_submenu_list_cls').css('display') == 'none') {
                $('.sh_global_submenu_list_cls').css('display', 'block')
            } else {
                $('.sh_global_submenu_list_cls').css('display', 'none')
            }
        },

        redirect_request_creation: function (ev) {
            var type = $(ev.currentTarget).attr('type');

            if (type == 'maintenance') {
                this.do_action({
                    type: "ir.actions.act_window",
                    view_type: "form",
                    view_mode: "form",
                    views: [[false, "form"]],
                    res_model: "assets.request.wizard",
                    target: "new",
                });
            }
            else {
                this.do_action({
                    name: "Global Request",
                    type: "ir.actions.act_window",
                    view_type: "form",
                    view_mode: "form",
                    views: [[false, "form"]],
                    res_model: "sh.global.request.wizard",
                    target: "new",
                    context: {
                        default_request_type: type,

                    },
                });
            }

        },

        redirect_request_direct_view: function (ev) {
            ev.preventDefault();
            ev.stopPropagation();
            var type = $(ev.currentTarget).attr('type');

            if (type == 'sop') {
                this.do_action({
                    name: "SOP",
                    type: "ir.actions.act_window",
                    view_type: "list",
                    view_mode: "list",
                    views: [[false, "list"], [false, "form"]],
                    res_model: "sh.sop.article",
                    target: "current",
                });
            }

            else if (type == 'knowledge') {
                this.do_action({
                    name: "Knowledge",
                    type: "ir.actions.act_window",
                    view_type: "list",
                    view_mode: "list",
                    views: [[false, "list"], [false, "form"]],
                    res_model: "sh.knowledge.article",
                    target: "current",
                });
            }

            else if (type == 'idea') {
                this.do_action({
                    name: "Idea",
                    type: "ir.actions.act_window",
                    view_type: "list",
                    view_mode: "list",
                    views: [[false, "list"], [false, "form"]],
                    res_model: "sh.idea",
                    target: "current",
                    context: {
                        'create': true
                    },
                });
            }

            else if (type == 'complain') {
                this.do_action({
                    name: "Complain",
                    type: "ir.actions.act_window",
                    view_type: "list",
                    view_mode: "list",
                    views: [[false, "list"], [false, "form"]],
                    res_model: "sh.complain",
                    target: "current",
                    context: {
                        default_sh_artical_type: 'sop_base',
                    },
                });
            }
            else if (type == 'maintenance') {
                this.do_action({
                    name: "Maintenance",
                    type: "ir.actions.act_window",
                    view_type: "list",
                    view_mode: "list",
                    views: [[false, "list"], [false, "form"]],
                    res_model: "asset.request",
                    target: "current",
                });
            }
            else if (type == 'assignment') {
                this.do_action({
                    name: "My Allocation",
                    type: "ir.actions.act_window",
                    view_type: "list",
                    view_mode: "list",
                    views: [[false, "kanban"], [false, "list"], [false, "form"]],
                    res_model: "sh.employee.task.allocation",
                    context: {
                        'create': false,
                        'edit': false,
                        'delete': false,
                        'search_default_group_employee': 1,
                        'search_default_filter_today': 1,
                    },
                    target: "current",
                });
            }

            else if (type == 'project') {
                this.do_action({
                    name: "Projects",
                    type: "ir.actions.act_window",
                    view_type: "list",
                    view_mode: "list",
                    views: [[false, "kanban"], [false, "list"], [false, "form"]],
                    res_model: "project.project",
                    context: {
                        'create': false,
                        'edit': false,
                        'delete': false,
                        'search_default_groupby_child_project': 1,
                        'search_default_groupby_stage': 1,
                    },
                    target: "current",
                });
            }

        },


        init: function () {
            this._super.apply(this, arguments);

        },
        start: function () {
            var self = this
            if (group_allow_global_request) {
                self.$el.removeClass('d-none')
            }
            else {
                self.$el.addClass('d-none')

            }

            core.bus.on('web_client_ready', null, () => {
                this.call('bus_service', 'addEventListener', 'notification', this._onNotification.bind(this));
            });

            // Add a click event listener to the document
            $(document).on('click', function (e) {
                if (!$(e.target).closest('.sh_global_submenu_list_cls, .openDropdown').length) {
                    // Close the wizard when the click is outside the wizard area and the button
                    $('.sh_global_submenu_list_cls').css('display', 'none');
                }
            });
        },
    });

    global_request_menulist.prototype.sequence = 30;
    SystrayMenu.Items.push(global_request_menulist);

    //return quick_menu;
    return {
        global_request_menulist: global_request_menulist,
    };
});
