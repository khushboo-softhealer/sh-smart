// ===========================================
//	Quick Menu List
// ===========================================

odoo.define("sh_task_time.task_menulist", function (require) {
    "use strict";

    var core = require("web.core");
    var Widget = require("web.Widget");
    var rpc = require("web.rpc");
    var SystrayMenu = require("web.SystrayMenu");
    var _t = core._t;
    var QWeb = core.qweb;
    var session = require('web.session');
    var group_allow_edit = false;

    session.user_has_group("sh_task_time.group_edit_timesheet").then(function (has_group) {
        group_allow_edit = has_group;
    });

    var task_menulist = Widget.extend({
        template: "task.menulist",

        events: {
            // "click li.sh_resume_task_menu_cls i": "resume_task_menu",
            "click li a.sh_resume_task_menu_cls i": "resume_task_menu",
            // "click li.sh_end_task_menu_cls i": "end_task_menu",
            "click li a.sh_end_task_menu_cls i": "end_task_menu",
            "click a.sh_edit_pause_task_cls i": "edit_pause_task_entry_task",
            "click a.openDropdown": "open_quick_menu",
        },

        _onNotification: function ({ detail: notifications }) {
            for (var i = 0; i < notifications.length; i++) {
                var channel = notifications[i]['type'];
                if (channel == 'sh.timer.render') {
                    // UPDATE PAUSE TASK ENTRY
                    // =======================
                    var self = this;
                    var quick_menus_var = rpc.query({
                        model: 'sh.pause.task.entry',
                        method: 'get_task_menu_data',
                        args: ['', ['name', 'task_id','duration_timer']],
                    })
                        .then(function (menus) {
                            if (menus.length > 0) {
                                self.$el.find('.sh_task_menu_submenu_list_cls').html(QWeb.render("task.menulist.actions", { 'task_menulist_actions': menus }));
                            } else {
                                self.$el.find('.sh_task_menu_submenu_list_cls').html(QWeb.render("task.menulist.actions", { 'no_menu': 1 }));
                            }
                        });
                }
            }
        },

        open_quick_menu: function (e) {

            // FOR UPDATE PAUSE TASK ENTRY
            // ===========================

            var self = this;
            var quick_menus_var = rpc.query({
                model: 'sh.pause.task.entry',
                method: 'get_task_menu_data',
                args: ['', ['name', 'task_id','duration_timer']],
            })
                .then(function (menus) {
                    if (menus.length > 0) {
                        self.$el.find('.sh_task_menu_submenu_list_cls').html(QWeb.render("task.menulist.actions", { 'task_menulist_actions': menus }));
                    } else {
                        self.$el.find('.sh_task_menu_submenu_list_cls').html(QWeb.render("task.menulist.actions", { 'no_menu': 1 }));
                    }
                });

            // HIDE EDIT BUTTON IF NO ACCESS

            if (group_allow_edit){
                if ($('.sh_edit_pause_task_cls').css('display') == 'none')
                {
                    $('.sh_edit_pause_task_cls').css('display','inline-block')
                }
            }
            else{
                $('.sh_edit_pause_task_cls').css('display','none')
            }
            
            // FOR PAUSE TASK ENTRY DROPDOWN LIST
            
            if ($('.sh_task_menu_submenu_list_cls').css('display') == 'none')
            {                   
                $('.sh_task_menu_submenu_list_cls').css('display','block')
            }else{
                $('.sh_task_menu_submenu_list_cls').css('display','none')
            }
        },

        resume_task_menu: function (e) {
            e.stopPropagation();
            var self = this;
            var id = parseInt($(e.currentTarget).data('id'));

            if (id !== NaN) {
                self._rpc({
                        model: "sh.pause.task.entry",
                        method: "resume_task",
                        args: [id],
                    }).then(function (res) {
                        if (res.id) {
                            if ($.bbq.getState(true).action == res.action_id) {
                                self.$el.parents().find('.o_user_bookmark_menu > a').removeClass('active');
                            }
                            // location.reload(true);
                        }
                    });
            }
            return false;
        },

        end_task_menu: function (e) {
            e.stopPropagation();
            var self = this;
            var id = parseInt($(e.currentTarget).data('id'));
            if (id !== NaN) {
                self._rpc({
                    model: "sh.pause.task.entry",
                    method: "search_read",
                    fields: ["task_id","start_date","sh_pause_time"],
                    domain: [["id", "=", id]],
                }).then(function (data) {
                    if (data[0]) {
                        // _.each(data, function (user) {
                        if (data[0].task_id[0]) {
                            self._rpc({
                                model: "project.task",
                                method: "search_read",
                                fields: ["start_time", "end_time", "total_time"],
                                domain: [["id", "=", data[0].task_id[0]]],
                            }).then(function (task) {
                                self.do_action({
                                    type: "ir.actions.act_window",
                                    view_type: "form",
                                    view_mode: "form",
                                    views: [[false, "form"]],
                                    res_model: "task.time.account.line",
                                    // res_model: "sh.task.time.account.line",
                                    target: "new",
                                    context: {
                                        default_start_date: data[0]["start_time"],
                                        active_id: id,
                                        active_model: "sh.pause.task.entry",
                                    },
                                });
                            });
                        }
                        // });
                    }
                });

            }
            return false;
        },


        // ===============================
        // EDIT TASK FROM PAUSE TASK ENTRY
        // ===============================

        edit_pause_task_entry_task: function (e) {
            e.stopPropagation();
            var self = this;
            var id = parseInt($(e.currentTarget).data('id'));

            if (id !== NaN) {
                self._rpc({
                    model: "sh.pause.task.entry",
                    method: "search_read",
                    fields: ["task_id","difference_time_float","sh_pause_time"],
                    domain: [["id", "=", id]],
                }).then(function (data) {
                    if (data[0]) {
                        self.do_action({
                            name:"Edit Timesheet",
                            type: "ir.actions.act_window",
                            view_type: "form",
                            view_mode: "form",
                            views: [[false, "form"]],
                            res_model: "sh.edit.timesheet",
                            target: "new",
                            context: {
                                default_sh_pause_timesheet_id: id,
                                default_difference_time_float: data[0]["difference_time_float"],
                                active_id: id,
                                active_model: "sh.pause.task.entry",
                            },
                        });
                    }
                });
            }
            return false;
        },



        init: function () {
            this._super.apply(this, arguments);

        },
        start: function () {

            // for call busnotification
            core.bus.on('web_client_ready', null, () => {
                this.call('bus_service', 'addEventListener', 'notification', this._onNotification.bind(this));
            });
            
            //this.$var = this.$el.find('.sh_task_menu_submenu_list_cls');
            var self = this;
            var quick_menus_var = rpc.query({
                model: 'sh.pause.task.entry',
                method: 'get_task_menu_data',
                args: ['', ['name', 'task_id','duration_timer']],
            })
                .then(function (menus) {
                    if (menus.length > 0) {
                        self.$el.find('.sh_task_menu_submenu_list_cls').html(QWeb.render("task.menulist.actions", { 'task_menulist_actions': menus }));
                    } else {
                        self.$el.find('.sh_task_menu_submenu_list_cls').html(QWeb.render("task.menulist.actions", { 'no_menu': 1 }));
                    }
                });
            return this._super();
        },
    });

    task_menulist.prototype.sequence = 3;
    SystrayMenu.Items.push(task_menulist);

    //return quick_menu;
    return {
        task_menulist: task_menulist,
    };
});
