// odoo.define('sh_task_time.time_track', function (require) {
// "use strict";
// var AbstractField = require('web.AbstractField');
// var core = require('web.core');
// var field_registry = require('web.field_registry');
// var time = require('web.time');
// var Widget = require('web.Widget');
// var _t = core._t;

// var TimeCounter = AbstractField.extend({
//     supportedFieldTypes: [],

//     willStart: function () {
//         var self = this;
//         var def = this._rpc({
//             model: 'account.analytic.line',
//             method: 'search_read',
//             domain: [
//                 ['task_id', '=', this.record.data.id],
//                 ['end_date','=',false],
//                 ['start_date','!=',false]
//               //  ['employee_id.user_id', '=', this.getSession().uid],
//             ],
//         }).then(function (result) {
//             if (self.mode === 'readonly') {
//                 var currentDate = new Date();
//                 self.duration = 0;
//                 _.each(result, function (data) {
//                     self.duration += data.end_date ?
//                         self._getDateDifference(data.start_date, data.end_date) :
//                         self._getDateDifference(time.auto_str_to_date(data.start_date), currentDate);
//                 });
//             }
//         });
//         return $.when(this._super.apply(this, arguments), def);
//     },


//     destroy: function () {
//         this._super.apply(this, arguments);
//         clearTimeout(this.timer);
//     },

//     isSet: function () {
//         return true;
//     },

//     _getDateDifference: function (dateStart, dateEnd) {
//         return moment(dateEnd).diff(moment(dateStart));
//     },

//     _render: function () {
//         this._startTimeCounter();
//     },

//     _startTimeCounter: function () {
//         var self = this;
//         this.timer = '';
//         clearTimeout(this.timer);
//         if (this.record.data.is_user_working) {
//             this.timer = setTimeout(function () {
//                 self.duration += 1000;
//                 self._startTimeCounter();
//             }, 1000);
//         } else {
//             clearTimeout(this.timer);
//         }
//         this.$el.html($('<span>' + moment.utc(this.duration).format("HH:mm:ss") + '</span>'));
//     },
// });

// field_registry
//     .add('task_time_counter', TimeCounter);

// });

odoo.define('sh_task_time.TaskTimerTemplate', function (require) {
	
	var core = require('web.core');
    var Dialog = require('web.Dialog');
    var Widget = require('web.Widget');
    var rpc = require('web.rpc');    
    var SystrayMenu = require('web.SystrayMenu');

    var _t = core._t;
    var QWeb = core.qweb;
	var TimerMenu = Widget.extend({
		template: 'TaskTimerTemplate',
		events: {
			'click #timer_start': '_start_timer',
			'click #timer_stop': '_stop_timer',
			'click #timer_pause': '_pause_timer',
			// 'click #timer_resume': '_resume_timer',
		},
		_onNotification: function ({ detail: notifications }) {
            for (var i = 0; i < notifications.length; i++) {
                var channel = notifications[i]['type'];
                if (channel == 'sh.timer.render') {					
					this.render_the_buttons()					
                }
            }
        },
		/**
		 * @override
		 */
		start: function () {
			var self = this;
			this._super.apply(this, arguments);
			// self.render_the_buttons(self)
			core.bus.on('web_client_ready', null, () => {
                this.call('bus_service', 'addEventListener', 'notification', this._onNotification.bind(this));
            });


		},

		// NEW METHOD ADDED INIT

		init: function () {
            this._super.apply(this, arguments);
            var self = this;
		
			// for calling busnotification
			// core.bus.on('web_client_ready', null, () => {
            //     this.call('bus_service', 'addEventListener', 'notification', this._onNotification.bind(this));
            // });

            this._rpc({
                model: "res.users",
                method: "search_read",
                fields: ["task_id","task_running_ids"],
                domain: [["id", "=", this.getSession().uid]],
            }).then(function (data) {                
                if (data) {
                    _.each(data,function (user) {
                        if (user.task_running_ids){
                            self._rpc({
                                model: "sh.pause.task.entry",
                                method: "get_duration",
                                args: [user.id],
                            }).then(function (duration) {

                                if (duration){
                                    self.$("#timer_start").css("display", "none");                            
                                    self.$("#timer_stop").css("display", "flex");
                                    // self.$("#user_task").text(user.task_id[1]);
                                    self.$("#user_task").text(user.task_id[1]).attr("title",user.task_id[1]);



									// rare_case
									self.$("#timer_pause").css("display", "flex");


                                    self.$("#task_timer").html($("<span>" + moment.utc(duration).format("HH:mm:ss") + "</span>"));
                                    self._startTimeCounter(duration);

                                } else {
                                    // customization
                                    self.$("#timer_pause").css("display", "none");
                                    // =================

                                    self.$("#timer_stop").css("display", "none");
                                    self.$("#task_timer").css("display", "none");
                                    self.$("#timer_start").css("display", "flex");
                                }
                            });
                        } else {
                            // customization
                            self.$("#timer_pause").css("display", "none");
                            // =================

                            self.$("#timer_stop").css("display", "none");
                            self.$("#task_timer").css("display", "none");                            
                            self.$("#timer_start").css("display", "flex");
                        }
                    });
                }
            });
        },


		// old_one
        _startTimeCounter: function (duration) {
        	var self = this;
			clearTimeout(self.running_timer);
        	self.running_timer = setTimeout(function () {
                	duration += 1000;
                    $("#task_timer").html($('<span>' + moment.utc(duration).format("HH:mm:ss") + '</span>'));
                    self._startTimeCounter(duration);
                }, 1000);
        },

		// old_one

		// _start_timer: function (e) {
		// 	e.preventDefault();
		// 	// this._super.apply(this, arguments);
        //     var self = this;
		// 	this._rpc({
		// 		model: 'sh.start.timesheet',
		// 		method: 'button_start_task',
		// 		args: []
		// 	}).then(function(){				
		// 		self.render_the_buttons(self)
		// 	})
		// 	location.reload()
		// },

        _start_timer: function (e) {
            e.preventDefault();
            this.do_action({
				name :'Start Task Timesheet',
                type: "ir.actions.act_window",
                view_type: "form",
                view_mode: "form",
                views: [[false, "form"]],
                res_model: "sh.start.timesheet",
                target: "new",
                context: {
                    form_view_ref: "sh_task_track.start_timesheet_form",
                },
            });
        },
		// _resume_timer : function (e) {
		// 	e.preventDefault();
		// 	var self = this;
		// 	  this._rpc({
	    //             model: 'res.users',
	    //             method: 'search_read',
	    //             fields: ['support_task_id','support_start_time'],
	    //             domain: [['id','=',this.getSession().uid]]
	    //         }).then(function(data) {
	    //             if (data) {
	    //             	 _.each(data, function (user) {
	    //             		 if(user.support_task_id){
	    //             			 self._rpc({
		// 			                model: 'project.task',
		// 			                method: 'search_read',
		// 			                fields: ['start_time','end_time','total_time'],
		// 			                domain: [['id','=',user.support_task_id[0]]]
		// 				         }).then(function(task) {
						        	 
		// 				        	return self.do_action({
		//                 					type: 'ir.actions.act_window',
		//                 					// view_type: 'form',
		//                 					view_mode: 'form',
		//                 					views: [
		//                 						[false, 'form']
		//                 					],
		//                 					res_model: 'task.time.account.line',
		//                 					target: 'new',
		//                 					context: {
		//                 						'default_start_date': user.support_start_time,
		//                 						'active_id':user.support_task_id[0],
		//                 						'active_model':'project.task',
		// 										'task_type' : 'support'
		//                 					},
		// 									on_close: function () {												
		// 										self.render_the_buttons(self)
		// 									},
		//                 				},{
		// 								})
		// 				          });
	                			
	                				
	    //             		 }
	    //             	 });
	    //             }
	    //         });
		// },

		//OLD PAUSE TASK METHOD 

		// _pause_timer : function (e) {
		// 	e.preventDefault();
        //     var self = this;
		// 	this._rpc({
		// 		model: 'sh.start.timesheet',
		// 		method: 'button_pause_task',
		// 		args: []
		// 	}).then(function(){
		// 		self.render_the_buttons(self)
		// 	})
		// },

		// NEW PAUSE TASK METHOD
        _pause_timer: function (e) {
            e.preventDefault();

            var self = this;
            this._rpc({
                model: "res.users",
                method: "search_read",
                fields: ["task_id"],
                domain: [["id", "=", this.getSession().uid]],
            }).then(function (data) {
                if (data) {
                    _.each(data, function (user) {
                        if (user.task_id) {
                            self._rpc({
                                model: "project.task",
                                method: "search_read",
                                fields: ["start_time", "end_time", "total_time"],
                                domain: [["id", "=", user.task_id[0]]],
                            }).then(function (task) {

                                vals={
                                    'start_date': task[0]["start_time"],
                                    'task_id': user.task_id[0],
                                }
                                self._rpc({
                                    model: "project.task",
                                    method: "paush_running_timer",
                                    args: [user.task_id[0],vals],
                                })

                                self.$("#timer_pause").css("display", "none");
                                self.$("#timer_stop").css("display", "none");
                                self.$("#task_timer").css("display", "none");
                                self.$("#timer_start").css("display", "flex");
                                self.$("#user_task").css("display", "none");

                                // location.reload(true);
								// self.render_the_buttons(self)

                            });
                        }
                    });
                }
            });
        },

		_stop_timer: function (e) {
			e.preventDefault();
			var self = this;
			  this._rpc({
	                model: 'res.users',
	                method: 'search_read',
	                fields: ['task_id','start_time','ticket_id'],
	                domain: [['id','=',this.getSession().uid]]
	            }).then(function(data) {
	                if (data) {
	                	 _.each(data, function (user) {
	                		 if(user.task_id){
	                			 self._rpc({
					                model: 'project.task',
					                method: 'search_read',
					                fields: ['start_time','end_time','total_time'],
					                domain: [['id','=',user.task_id[0]]]
						         }).then(function(task) {
						        	 
						        	return self.do_action({
											name : "End Task Timesheet",
		                					type: 'ir.actions.act_window',
		                					view_mode: 'form',
		                					views: [[false, 'form']],
		                					res_model: 'task.time.account.line',
		                					target: 'new',
		                					context: {
		                						'default_start_date': user.start_time,
		                						'active_id':user.task_id[0],
		                						'active_model':'project.task',
												'task_type' : 'main',
												'ticket_id':user.ticket_id[0]
		                					},
											// on_close: function () {												
											// 	self.render_the_buttons(self)
											// },
		                				})
						          });
	                			
	                				
	                		 }
	                	 });
	                }
	            });									
		},
		
		render_the_buttons : function(abc){
			var ki_self = this;

			$("#timer_stop").css("display","none");
			// $("#").css("display","none");
			$("#timer_resume").css("display","none");
			$("#timer_start").css("display","inline-block");
			$(".sh_timer_task").attr("style","display:none !important");
			$(".sh_timer").attr("style","display:none !important");
			$("#user_task").css("display","none")

			// NEW CODE HERE
			$("#task_timer").css("display", "none");


			// // NEW CODE HERE
            ki_self._rpc({
                model: "res.users",
                method: "search_read",
                fields: ["task_id","task_running_ids"],
                domain: [["id", "=", this.getSession().uid]],
            }).then(function (data) {                
                if (data) {
                    _.each(data,function (user) {
                        if (user.task_running_ids){
                            ki_self._rpc({
                                model: "sh.pause.task.entry",
                                method: "get_duration",
                                args: [user.id],
                            }).then(function (duration) {

                                if (duration){
                                    ki_self.$("#timer_start").css("display", "none");                            
                                    ki_self.$("#timer_stop").css("display", "flex");
                                    ki_self.$("#user_task").text(user.task_id[1]).attr("title",user.task_id[1]);


									// rare_case
									ki_self.$("#timer_pause").css("display", "flex");
									ki_self.$("#user_task").css("display", "flex");

									ki_self.$("#task_timer").css("display", "flex");
                                    ki_self.$("#task_timer").html($("<span>" + moment.utc(duration).format("HH:mm:ss") + "</span>"));
                                    ki_self._startTimeCounter(duration);

                                } else {
                                    // customization
                                    ki_self.$("#timer_pause").css("display", "none");
                                    // =================

                                    ki_self.$("#timer_stop").css("display", "none");
                                    ki_self.$("#task_timer").css("display", "none");
                                    ki_self.$("#timer_start").css("display", "flex");
                                }
                            });
                        } else {


                            // customization
                            ki_self.$("#timer_pause").css("display", "none");
                            // =================

                            ki_self.$("#timer_stop").css("display", "none");
                            ki_self.$("#task_timer").css("display", "none");                            
                            ki_self.$("#timer_start").css("display", "flex");
                        }
                    });
                }
            });


		}
	});
	$(document).on('click', ".bell_notification", function (ev) {
        if ($('.sh_task_menu_submenu_list_cls').css('display') != 'none')
        {                   
            $('.sh_task_menu_submenu_list_cls').css('display','none')
        }
    });
	TimerMenu.prototype.sequence = 2;
	SystrayMenu.Items.push(TimerMenu);

	//return quick_menu;
	return {
		TimerMenu: TimerMenu,
	};

});


