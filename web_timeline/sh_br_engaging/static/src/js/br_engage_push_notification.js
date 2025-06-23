odoo.define('mail.systray.UserNotificationMenu', function (require) {
    "use strict";

    var core = require('web.core');
    var mailUtils = require('@mail/js/utils');
    var session = require('web.session');
    var SystrayMenu = require('web.SystrayMenu');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;

    var time = require('web.time');
    /**
     * Menu item appended in the systray part of the navbar, redirects to the next
     * activities of all app
     */
    var UserNotificationMenu = Widget.extend({
        name: 'firebase_menu',
        template: 'mail.systray.UserNotificationMenu',
        events: {
            'click .o_mail_preview': '_onPushNotificationClick',
            'click a.openDropdown': '_onActivityMenuShow',
        },
        
        _onPushNotificationClick: function (event) {
            // fetch the data from the button otherwise fetch the ones from the parent (.o_mail_preview).
            var data = _.extend({}, $(event.currentTarget).data(), $(event.target).data());
            var context = {};
            var self = this;
            this._rpc({
                model: 'sh.br.engage.push.notification',
                method: 'write',
                args: [data.id, { 'msg_read': true }],
            }).then(function () {                
                self._updateActivityPreview();
                self._updateCounter();
                if (data.res_model != '')
                if (data.res_model == 'sh.realtime.feedback' || data.res_model=='sh.high.five') {
                    var action_name = ''
                    if (data.res_model == 'sh.realtime.feedback'){
                        action_name = "Feedback"
                    }
                    else if (data.res_model == 'sh.high.five'){
                        action_name = "High Fives"
                    }
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
                }
                else {
                    self.do_action({
                        type: 'ir.actions.act_window',
                        name: data.res_model,
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

        _onNotification: function ({ detail: notifications }) {
            for (var i = 0; i < notifications.length; i++) {
                var channel = notifications[i]['type'];
                if (channel == 'sh.br.engage.push.notification') {
                    this._updateActivityPreview();
                    this._updateCounter();
                    $(document).find(".o_searchview_input").click()
                    $(document).click()
                }
            }
        },

        start: function () {
            // Hide Our Notifications OnCLick Of Outside
            // ========================================================================= 
            $(document).on('click', function (e) {
            if ($('.o_notification_systray_dropdown').css('display') == 'block')
            {                   
                $('.o_notification_systray_dropdown').css('display','none')
            }
            });
            // ========================================================================= 
            var self = this;
            this._$activitiesPreview = this.$('.o_notification_systray_dropdown_items');
            core.bus.on('web_client_ready', null, () => {
                // console.log("\n\n\n\n\n\n this", this);
                this.call('bus_service', 'addEventListener', 'notification', this._onNotification.bind(this));
            });
            this._updateActivityPreview();
            this._updateCounter();
            return this._super();
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

            return self._rpc({
                model: 'res.users',
                method: 'systray_get_firebase_notifications',
                args: [],
                kwargs: { context: session.user_context },
            }).then(function (data, counter) {
                self._notifications = data[0];
                self._counter = data[1];

                _.each(data[0], function (each_data) {
                    // console.log("\n\n\n\n Each Data", each_data['datetime']);

                    each_data['datetime'] = mailUtils.timeFromNow(moment(time.auto_str_to_date(each_data['datetime'])))
                    // console.log("\n\n\n\n Each Data Afterrr", each_data);
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
            self._getActivityData().then(function () {
                // console.log("\n\n\n\n\ Notifications", self._notifications);
                self._$activitiesPreview.html(QWeb.render('mail.systray.FirebaseMenu.Previews', {
                    notifications: self._notifications
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
         * @private
         */
        _onActivityMenuShow: async function (ev) {
            ev.preventDefault();
            ev.stopPropagation();
            if ($('.o_notification_systray_dropdown').css('display') == 'none')
            {                   
                $('.o_notification_systray_dropdown').css('display','block')
            }else{
                $('.o_notification_systray_dropdown').css('display','none')
            }
            await this._updateActivityPreview(); 
        },
    });

    SystrayMenu.Items.push(UserNotificationMenu);
    return UserNotificationMenu;

});