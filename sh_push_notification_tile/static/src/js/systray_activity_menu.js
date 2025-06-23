odoo.define('sh_push_notification_tile.FirebaseMenu', function (require) {

    var core = require('web.core');
    // var mailUtils = require('mail.utils');
    const { _t } = require('web.core');
    var session = require('web.session');
    var SystrayMenu = require('web.SystrayMenu');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;
    var time = require('web.time');
    /**
     * Menu item appended in the systray part of the navbar, redirects to the next
     * activities of all app
     */
    var FirebaseMenu = Widget.extend({
        name: 'firebase_menu',
        template: 'mail.systray.FirebaseMenu',
        events: {
            'click .o_mail_preview': '_onPushNotificationClick',
            'click .sh_view_read_all_btn': '_onClickReadAllNotification',
            'click .sh_view_all_btn': '_onClickAllNotification',
            'click a.openDropdown': '_onActivityMenuShow',
            'click .sh_view_hr_btn' : '_onclickHrButton',
            'click .sh_view_project_btn' : '_onclickProjectButton',
            'click .sh_view_sales_btn' : '_onclickSalesButton',
            'click .sh_view_support_btn' : '_onclickSupportButton',
            'click .sh_view_assignment_btn' : '_onclickAssignmentButton',
        },
        _onclickHrButton: function(event){
            var self = this;
            event.stopPropagation();            
            this.getSession()?.user_has_group('project.group_project_user').then(function(has_group) {
                self.has_group_project_user = has_group;
            });
            this.getSession()?.user_has_group('sales_team.group_sale_salesman').then(function(has_group) {
                self.has_group_sale_own_document = has_group;
            });
            this.getSession()?.user_has_group('sh_helpdesk.helpdesk_group_user').then(function(has_group) {
                self.has_group_helpdesk_user = has_group;
            });
            self._rpc({
                model: 'res.users',
                method: 'systray_get_firebase_notifications_type',
                args: [{type:"hr"}],
                kwargs: { context: session.user_context },
            }).then(function (data, counter) {
                self._notifications = data[0];
                _.each(data[0], function (each_data) {

                    each_data['datetime'] = self.timeFromNow(moment(time.auto_str_to_date(each_data['datetime'])))
                });
                self._$activitiesPreview.html(QWeb.render('mail.systray.FirebaseMenu.Previews', {
                    notifications: self._notifications,
                    'has_group_project_user' :self.has_group_project_user,
                    'has_group_helpdesk_user' : self.has_group_helpdesk_user,
                    'has_group_sale_own_document' : self.has_group_sale_own_document,
                    'has_allow_assignment_request_access_group' : self.has_allow_assignment_request_access_group,

                    'sale_type_noti_count' : data[2],
                    'project_type_noti_count' : data[3],
                    'support_type_noti_count' : data[4],
                    'hr_type_noti_count' : data[5],
                    'assingment_noti_count' : data[6],
                }));
                setTimeout(function(){
                    $(document).find('.sh_view_hr_btn').addClass("active");
                    $(document).find('.sh_view_project_btn').removeClass("active"); 
                    $(document).find('.sh_view_sales_btn').removeClass("active");
                    $(document).find('.sh_view_support_btn').removeClass("active");
                    $(document).find('.sh_view_assignment_btn').removeClass("active");
                }, 100);
            });

        },
        _onclickProjectButton : function(event){
            var self = this;
            event.stopPropagation();            
            this.getSession()?.user_has_group('project.group_project_user').then(function(has_group) {
                self.has_group_project_user = has_group;
            });
             this.getSession()?.user_has_group('sales_team.group_sale_salesman').then(function(has_group) {
                self.has_group_sale_own_document = has_group;
            });
             this.getSession()?.user_has_group('sh_helpdesk.helpdesk_group_user').then(function(has_group) {
                self.has_group_helpdesk_user = has_group;
            });
            self._rpc({
                model: 'res.users',
                method: 'systray_get_firebase_notifications_type',
                args: [{type:"project"}],
                kwargs: { context: session.user_context },
            }).then(function (data, counter) {
                self._notifications = data[0];
                _.each(data[0], function (each_data) {

                    each_data['datetime'] = self.timeFromNow(moment(time.auto_str_to_date(each_data['datetime'])))
                });
                self._$activitiesPreview.html(QWeb.render('mail.systray.FirebaseMenu.Previews', {
                    notifications: self._notifications,
                    'has_group_project_user' :self.has_group_project_user,
                    'has_group_helpdesk_user' : self.has_group_helpdesk_user,
                    'has_group_sale_own_document' : self.has_group_sale_own_document,
                    'has_allow_assignment_request_access_group' : self.has_allow_assignment_request_access_group,

                    'sale_type_noti_count' : data[2],
                    'project_type_noti_count' : data[3],
                    'support_type_noti_count' : data[4],
                    'hr_type_noti_count' : data[5],
                    'assingment_noti_count' : data[6],
                }));
                setTimeout(function(){
                    $(document).find('.sh_view_project_btn').addClass("active"); 
                    $(document).find('.sh_view_sales_btn').removeClass("active");
                    $(document).find('.sh_view_support_btn').removeClass("active");
                    $(document).find('.sh_view_hr_btn').removeClass("active");
                    $(document).find('.sh_view_assignment_btn').removeClass("active");
                }, 100);
            });
        },
        _onclickSalesButton : function(event){
            var self = this;
            event.stopPropagation();            
            this.getSession()?.user_has_group('project.group_project_user').then(function(has_group) {
                self.has_group_project_user = has_group;
            });
             this.getSession()?.user_has_group('sales_team.group_sale_salesman').then(function(has_group) {
                self.has_group_sale_own_document = has_group;
            });
             this.getSession()?.user_has_group('sh_helpdesk.helpdesk_group_user').then(function(has_group) {
                self.has_group_helpdesk_user = has_group;
            });
            self._rpc({
                model: 'res.users',
                method: 'systray_get_firebase_notifications_type',
                args: [{type:"sale"}],
                kwargs: { context: session.user_context },
            }).then(function (data, counter) {
                self._notifications = data[0];
                _.each(data[0], function (each_data) {

                    each_data['datetime'] = self.timeFromNow(moment(time.auto_str_to_date(each_data['datetime'])))
                });
                self._$activitiesPreview.html(QWeb.render('mail.systray.FirebaseMenu.Previews', {
                    notifications: self._notifications,
                    'has_group_project_user' :self.has_group_project_user,
                    'has_group_helpdesk_user' : self.has_group_helpdesk_user,
                    'has_group_sale_own_document' : self.has_group_sale_own_document,
                    'has_allow_assignment_request_access_group' : self.has_allow_assignment_request_access_group,

                    'sale_type_noti_count' : data[2],
                    'project_type_noti_count' : data[3],
                    'support_type_noti_count' : data[4],
                    'hr_type_noti_count' : data[5],
                    'assingment_noti_count' : data[6],
                }));
                setTimeout(function(){
                    $(document).find('.sh_view_sales_btn').addClass("active");
                    $(document).find('.sh_view_support_btn').removeClass("active");                
                    $(document).find('.sh_view_hr_btn').removeClass("active");   
                    $(document).find('.sh_view_project_btn').removeClass("active"); 
                    $(document).find('.sh_view_assignment_btn').removeClass("active");               
                }, 100);
            });
        },
        _onclickSupportButton : function(event){
            var self = this;
            event.stopPropagation();            
            this.getSession()?.user_has_group('project.group_project_user').then(function(has_group) {
                self.has_group_project_user = has_group;
            });
             this.getSession()?.user_has_group('sales_team.group_sale_salesman').then(function(has_group) {
                self.has_group_sale_own_document = has_group;
            });
             this.getSession()?.user_has_group('sh_helpdesk.helpdesk_group_user').then(function(has_group) {
                self.has_group_helpdesk_user = has_group;
            });
            self._rpc({
                model: 'res.users',
                method: 'systray_get_firebase_notifications_type',
                args: [{type:"support"}],
                kwargs: { context: session.user_context },
            }).then(function (data, counter) {
                self._notifications = data[0];
                _.each(data[0], function (each_data) {
                    each_data['datetime'] = self.timeFromNow(moment(time.auto_str_to_date(each_data['datetime'])))
                });
                self._$activitiesPreview.html(QWeb.render('mail.systray.FirebaseMenu.Previews', {
                    notifications: self._notifications,
                    'has_group_project_user' :self.has_group_project_user,
                    'has_group_helpdesk_user' : self.has_group_helpdesk_user,
                    'has_group_sale_own_document' : self.has_group_sale_own_document,
                    'has_allow_assignment_request_access_group' : self.has_allow_assignment_request_access_group,

                    'sale_type_noti_count' : data[2],
                    'project_type_noti_count' : data[3],
                    'support_type_noti_count' : data[4],
                    'hr_type_noti_count' : data[5],
                    'assingment_noti_count' : data[6],
                }));
                setTimeout(function(){            
                    $(document).find('.sh_view_support_btn').addClass("active");
                    $(document).find('.sh_view_sales_btn').removeClass("active");
                    $(document).find('.sh_view_hr_btn').removeClass("active");   
                    $(document).find('.sh_view_project_btn').removeClass("active");
                    $(document).find('.sh_view_assignment_btn').removeClass("active");
                }, 100);
            });
            
        },
        _onclickAssignmentButton : function(event){
            var self = this;
            event.stopPropagation();            
            this.getSession()?.user_has_group('project.group_project_user').then(function(has_group) {
                self.has_group_project_user = has_group;
            });
             this.getSession()?.user_has_group('sales_team.group_sale_salesman').then(function(has_group) {
                self.has_group_sale_own_document = has_group;
            });
            this.getSession()?.user_has_group('sh_global_requests.allow_assignment_request_access_group').then(function(has_group) {
                self.has_allow_assignment_request_access_group = has_group;
            });
            self._rpc({
                model: 'res.users',
                method: 'systray_get_firebase_notifications_type',
                args: [{type:"assignment"}],
                kwargs: { context: session.user_context },
            }).then(function (data, counter) {
                self._notifications = data[0];
                _.each(data[0], function (each_data) {
                    each_data['datetime'] = self.timeFromNow(moment(time.auto_str_to_date(each_data['datetime'])))
                });
                self._$activitiesPreview.html(QWeb.render('mail.systray.FirebaseMenu.Previews', {
                    notifications: self._notifications,
                    'has_group_project_user' :self.has_group_project_user,
                    'has_group_helpdesk_user' : self.has_group_helpdesk_user,
                    'has_group_sale_own_document' : self.has_group_sale_own_document,
                    'has_allow_assignment_request_access_group' : self.has_allow_assignment_request_access_group,

                    'sale_type_noti_count' : data[2],
                    'project_type_noti_count' : data[3],
                    'support_type_noti_count' : data[4],
                    'hr_type_noti_count' : data[5],
                    'assingment_noti_count' : data[6],
                }));
                setTimeout(function(){            
                    $(document).find('.sh_view_assignment_btn').addClass("active");
                    $(document).find('.sh_view_support_btn').removeClass("active");
                    $(document).find('.sh_view_sales_btn').removeClass("active");
                    $(document).find('.sh_view_hr_btn').removeClass("active");   
                    $(document).find('.sh_view_project_btn').removeClass("active");
                }, 100);
            });
            
        },
        _onPushNotificationClick: function (event) {
            // fetch the data from the button otherwise fetch the ones from the parent (.o_mail_preview).
            var data = _.extend({}, $(event.currentTarget).data(), $(event.target).data());
            var context = {};

            var self = this;

            this._rpc({
                model: 'user.push.notification',
                method: 'write',
                args: [data.id, { 'msg_read': true }],
            }).then(function () {
                self._updateActivityPreview();
                self._updateCounter();
                $(document).find('.o_notification_systray_item a.openDropdown').click()
                if (data.res_model == 'sh.hr.dashboard') {
                    self.do_action({
                        type: 'ir.actions.client',
                        tag: 'hr_dashboard.dashboard',
                        context: context,
                    }, {
                        clear_breadcrumbs: true,
                    });
                } else if(data.res_model == 'sh.high.five'){
                    var action_name = 'High Fives'
                    self.do_action({
                        type: 'ir.actions.act_window',
                        name: action_name,
                        view_mode: 'list',
                        res_model: data.res_model,
                        views: [[false, 'list']],
                        search_view_id: [false],
                        // domain: [['id', '=', data.res_id]],
                        // res_id: data.res_id,
                        context: context,
                    }, {
                        clear_breadcrumbs: true,
                    });
                }else if(data.res_model == 'sh.employee.task.allocation'){
                    self.do_action({
                        type: 'ir.actions.act_window',
                        name: data.model_name,
                        res_model: data.res_model,
                        views: [[false, 'form'], [false, 'tree'], [false, 'kanban']],
                        search_view_id: [false],
                        domain: [['id', '=', data.res_id]],
                        res_id: data.res_id,
                        context: {
                            'create': false,
                            'delete': false,
                        },
                    }, {
                        clear_breadcrumbs: true,
                    });
                }else {
                    self.do_action({
                        type: 'ir.actions.act_window',
                        name: data.model_name,
                        res_model: data.res_model,
                        views: [[false, 'form'], [false, 'tree']],
                        search_view_id: [false],
                        domain: [['id', '=', data.res_id]],
                        res_id: data.res_id,
                        context: context,
                    }, {
                        clear_breadcrumbs: true,
                    });
                }



            });

        },
        _onClickReadAllNotification: function (event) {
            var self = this;
            self._rpc({
                model: 'res.users',
                method: 'systray_get_firebase_all_notifications',
                args: [],
                kwargs: { context: session.user_context },
            }).then(function () {
                self._updateActivityPreview();
                self._updateCounter();
            });
        },
        _onClickAllNotification: function (event) {
            this.do_action({
                type: 'ir.actions.act_window',
                name: 'Notifications',
                res_model: 'user.push.notification',
                views: [[false, 'list']],
                view_mode: "list",
                target: 'current',
                domain: [['user_id', '=', session.uid]],
            }, {
                clear_breadcrumbs: true,
            });
        },

        _onNotification: function ({ detail: notifications }) {
            for (var i = 0; i < notifications.length; i++) {
                var channel = notifications[i]['type'];
                if (channel == 'sh.push.notification') {
                    this._updateActivityPreview();
                    this._updateCounter();
                }
            }
        },
        start: function () {
            var self = this;
            self.has_group_project_user = true;
            self.has_group_sale_own_document = true;
            self.has_group_helpdesk_user = true;
            self.has_allow_assignment_request_access_group = true
            this.getSession()?.user_has_group('project.group_project_user').then(function(has_group) {
                self.has_group_project_user = has_group;
            });
            this.getSession()?.user_has_group('sales_team.group_sale_salesman').then(function(has_group) {
                self.has_group_sale_own_document = has_group;
            });
            this.getSession()?.user_has_group('sh_helpdesk.helpdesk_group_user').then(function(has_group) {
                self.has_group_helpdesk_user = has_group;
            });
            this.getSession()?.user_has_group('sh_global_requests.allow_assignment_request_access_group').then(function(has_group) {
                self.has_allow_assignment_request_access_group = has_group;
            });
            this._$activitiesPreview = this.$('.o_notification_systray_dropdown_items');
            core.bus.on('web_client_ready', null, () => {
                this.call('bus_service', 'addEventListener', 'notification', this._onNotification.bind(this));
            });

            this._updateActivityPreview();
            this._updateCounter();
            return self._super();
        },

        timeFromNow:function(date) {
            if (moment().diff(date, 'seconds') < 45) {
                return _t("now");
            }
            return date.fromNow();
        },
        //--------------------------------------------------
        // Private
        //--------------------------------------------------
        /**
         * Make RPC and get current user's activity details
         * @private
         */
        _getActivityData: function () {
            var self = this;
            let noti_type = ''
            if (self.has_group_sale_own_document){
                noti_type = "sale"
            }else if (self.has_group_project_user){
                noti_type = "project"
            }else if(self.has_group_helpdesk_user){
                noti_type = 'support'
            }
            else if(self.has_allow_assignment_request_access_group){
                noti_type = 'assignment'
            }
            return self._rpc({
                model: 'res.users',
                method: 'systray_get_firebase_notifications_type',
                args: [{type:noti_type}],
                kwargs: { context: session.user_context },
            }).then(function (data, counter) {

                self._notifications = data[0];
                self._counter = data[1];

                _.each(data[0], function (each_data) {

                    each_data['datetime'] = self.timeFromNow(moment(time.auto_str_to_date(each_data['datetime'])))
                });


                self._updateCounter();

            });
        },
        /**
         * Get particular model view to redirect on click of activity scheduled on that model.
         * @private
         * @param {string} model
         */
        _getActivityModelViewID: function (model) {
            return this._rpc({
                model: model,
                method: 'get_activity_view_id'
            });
        },
        /**
         * Update(render) activity system tray view on activity updation.
         * @private
         */
        _updateActivityPreview: function () {
            var self = this;
             this.getSession()?.user_has_group('project.group_project_user').then(function(has_group) {
                self.has_group_project_user = has_group;
            });
             this.getSession()?.user_has_group('sales_team.group_sale_salesman').then(function(has_group) {
                self.has_group_sale_own_document = has_group;
            });
             this.getSession()?.user_has_group('sh_helpdesk.helpdesk_group_user').then(function(has_group) {
                self.has_group_helpdesk_user = has_group;
            });
            this.getSession()?.user_has_group('sh_global_requests.allow_assignment_request_access_group').then(function(has_group) {
                self.has_allow_assignment_request_access_group = has_group;
            });
            self._getActivityData().then(function () {
                self._$activitiesPreview.html(QWeb.render('mail.systray.FirebaseMenu.Previews', {
                    notifications: self._notifications,
                    'has_group_project_user' :self.has_group_project_user,
                    'has_group_helpdesk_user' : self.has_group_helpdesk_user,
                    'has_group_sale_own_document' : self.has_group_sale_own_document,
                    'has_allow_assignment_request_access_group' : self.has_allow_assignment_request_access_group,
                }));                
            });
        },
        /**
         * update counter based on activity status(created or Done)
         * @private
         * @param {Object} [data] key, value to decide activity created or deleted
         * @param {String} [data.type] notification type
         * @param {Boolean} [data.activity_deleted] when activity deleted
         * @param {Boolean} [data.activity_created] when activity created
         */
        _updateCounter: function () {
            var counter = this._counter;
            if (counter > 0) {
                this.$('.o_notification_counter').text(counter);
            } else {
                this.$('.o_notification_counter').text('');
            }
        },

        //------------------------------------------------------------
        // Handlers
        //------------------------------------------------------------

        /**
         * Redirect to specific action given its xml id
         * @private
         * @param {MouseEvent} ev
         */
        _onActivityActionClick: function (ev) {
            ev.stopPropagation();
            var actionXmlid = $(ev.currentTarget).data('action_xmlid');
            this.do_action(actionXmlid);
        },

        /**
         * Redirect to particular model view
         * @private
         * @param {MouseEvent} event
         */
        _onActivityFilterClick: function (event) {
            // fetch the data from the button otherwise fetch the ones from the parent (.o_mail_preview).
            var data = _.extend({}, $(event.currentTarget).data(), $(event.target).data());
            var context = {};
            if (data.filter === 'my') {
                context['search_default_activities_overdue'] = 1;
                context['search_default_activities_today'] = 1;
            } else {
                context['search_default_activities_' + data.filter] = 1;
            }
            this.do_action({
                type: 'ir.actions.act_window',
                name: data.model_name,
                res_model: data.res_model,
                views: [[false, 'kanban'], [false, 'form']],
                search_view_id: [false],
                domain: [['activity_user_id', '=', session.uid]],
                context: context,
            }, {
                clear_breadcrumbs: true,
            });
        },
        /**
         * @private
         */
        _onActivityMenuShow: async function () {
            if ($('.o_notification_systray_dropdown').css('display') == 'none')
            {                   
                $('.o_notification_systray_dropdown').css('display','block')
            }else{                   
                $('.o_notification_systray_dropdown').css('display','none')
            }
            await this._updateActivityPreview();
            var self = this;            
            if (self.has_group_sale_own_document){
                $(document).find('.sh_view_sales_btn').click();
            }
            else if(self.has_group_helpdesk_user){
                $(document).find('.sh_view_support_btn').click();
            }
            else if(self.has_group_project_user){
                $(document).find('.sh_view_project_btn').click();
            }
            else if(self.has_allow_assignment_request_access_group){
                $(document).find('.sh_view_assignment_btn').click();
            }
            else{
                $(document).find('.sh_view_hr_btn').click();
            }            
        },
    });
    $(document).on('click', ".pause_entry_list", function (ev) {
        if ($('.o_notification_systray_dropdown').css('display') != 'none')
        {                   
            $('.o_notification_systray_dropdown').css('display','none')
        }
    });
    SystrayMenu.Items.push(FirebaseMenu);
    return FirebaseMenu;
});