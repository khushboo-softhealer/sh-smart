odoo.define('sh_timesheet_dashboard.timesheet_dashboard', function (require) {
	"use strict";
	var rpc = require('web.rpc');
	var viewRegistry = require('web.view_registry');
	var KanbanRenderer = require('web.KanbanRenderer');
	var KanbanView = require('web.KanbanView');
	var core = require('web.core');
	var QWeb = core.qweb;
	var TimesheetKanbanRenderer = KanbanRenderer.extend({
		_renderView: function () {
			var self = this;
			return this._super.apply(this, arguments).then(function () {
				self.get_table_data();
				self.get_employee_wise_hours();
				var cuurent_emp = self.$el.find('#dashboard_counter').find('#employee_filter_list').val()
				$.get('/get_project_list', {
					employe: cuurent_emp
				}, function (result) {
					var data = JSON.parse(result);
					for (const [key, value] of Object.entries(data)) {
						self.$el.find('#dashboard_counter').find("#project_filter_list").append('<option value="' + key + '" >' + value + '</option>');
					}
				});
				// self.$el.find('#dashboard_counter').find('#sh_temp_dashboard_activity').find('.timesheet_trasnfer').on('click', self, self.action_timesheet_transfer.bind(self));

			});
		},
		get_table_data: function (e) {
			var self = this;
			var dashboard = self.$el.find('#dashboard_counter');
			var days_filter = dashboard.find('#timesheet_days_filter_list').val();
			var project_value = dashboard.find('#project_filter_list').val();
			var task_value = dashboard.find('#task_filter_list').val();
			var cuurent_emp = dashboard.find('#employee_filter_list').val()
			var start_date = '';
			var end_date = '';
			if (days_filter == 'custom') {
				var start_date = dashboard.find('#start_date').val();
				var end_date = dashboard.find('#end_date').val();
			}
			// else {
			// 	dashboard.find('#start_date').style.display = 'none';
			// 	dashboard.find('#end_date').style.display = 'none';
			// 	dashboard.find('#start_date').value = '';
			// 	dashboard.find('#end_date').value = '';
			// }

			$.get('/get_sh_crm_activity_done_tbl', {
				days_filter: days_filter,
				start_date: start_date,
				end_date: end_date,
				project_value: project_value,
				task_value: task_value,
				employe: cuurent_emp

			}, function (result) {
				var data = JSON.parse(result);
				dashboard.find('.js_cls_activity_table_wrapper').html(data.html_tbl)
			});

			$.get('/get_sh_temporary_done_tbl', {
				days_filter: days_filter,
				start_date: start_date,
				end_date: end_date,
				project_value: project_value,
				task_value: task_value,
				employe: cuurent_emp
			}, function (result) {
				var data = JSON.parse(result);
				dashboard.find('.js_cls_temporary_table_wrapper').html(data.html_tbl)
			})
		},
		get_employee_wise_hours: function (e) {
			var self = this;
			var dashboard = self.$el.find('#dashboard_counter');
			var days_filter = dashboard.find('#timesheet_days_filter_list').val();
			var project_value = dashboard.find('#project_filter_list').val();
			var start_date = '';
			var end_date = '';

			if (days_filter == 'custom') {
				var start_date = $('#start_date').val();
				var end_date = $('#end_date').val();
			}
			// else {
			// 	dashboard.find('start_date').style.display = 'none';
			// 	dashboard.find('end_date').style.display = 'none';
			// 	dashboard.find('start_date').value = '';
			// 	dashboard.find('end_date').value = '';
			// }
			$.get('/get_sh_emplooyee_tbl', {
				days_filter: days_filter,
				start_date: start_date,
				end_date: end_date,
				project_value: project_value,

			}, function (result) {
				var data = JSON.parse(result);
				dashboard.find('.js_cls_hours_data').html(data)
			});
		},
		action_timesheet_transfer: function (e) {
			alert("hishiushdfui");
			var self = this;
			var dashboard = self.$el.find('#dashboard_counter');
			var analytic_id = dashboard.find(e.currentTarget).attr('data-analytic_id')
		},
	});


	// $(document).on('click', '.timesheet_trasnfer', function (event) {
	// 	var analytic_id = $(event.currentTarget).attr('data-analytic_id')
	// 	return web_client.do_action({
	// 		type: 'ir.actions.act_window',
	// 		view_type: 'form',
	// 		view_mode: 'form',
	// 		views: [
	// 			[false, 'form']
	// 		],
	// 		res_model: 'sh.transfer.timesheet',
	// 		target: 'new',
	// 		context: {
	// 			'analytic_id': analytic_id
	// 		},
	// 	})
	// });



	// $.get('/get_employee_list', {
	// }, function (result) {
	// 	var data = JSON.parse(result);
	// 	for (const [key, value] of Object.entries(data)) {
	// 		$("#employee_filter_list").append('<option value="' + key + '" >' + value + '</option>');
	// 	}
	// });

	// $('#employee_filter_list').change(function () {
	// 	$("#project_filter_list option:not(:first)").remove();
	// 	var cuurent_emp = $('#employee_filter_list').val()
	// 	$.get('/get_project_list', {
	// 		employe: cuurent_emp
	// 	}, function (result) {
	// 		var data = JSON.parse(result);
	// 		for (const [key, value] of Object.entries(data)) {
	// 			$("#project_filter_list").append('<option value="' + key + '" >' + value + '</option>');
	// 		}
	// 	});
	// 	get_table_data();
	// });


	// $('#project_filter_list').change(function () {
	// 	$("#task_filter_list option:not(:first)").remove();
	// 	var current_project = $('#project_filter_list').val()
	// 	if (current_project != 'all') {
	// 		$.get('/get_project_wise_task', {
	// 			type: current_project,
	// 		}, function (result) {
	// 			var data = JSON.parse(result);
	// 			for (const [key, value] of Object.entries(data)) {
	// 				$("#task_filter_list").append('<option value="' + key + '" >' + value + '</option>');
	// 			}
	// 		})
	// 	}
	// 	get_table_data();
	// 	get_employee_wise_hours();
	// });

	// 	$('#timesheet_days_filter_list').change(function () {
	// 		var days_filter = $('#timesheet_days_filter_list').val();
	// 		if (days_filter == 'custom') {
	// 			document.getElementById('start_date').style.display = 'block';
	// 			document.getElementById('end_date').style.display = 'block';
	// 		}
	// 		else {
	// 			document.getElementById('start_date').style.display = 'none';
	// 			document.getElementById('end_date').style.display = 'none';
	// 			document.getElementById('start_date').value = '';
	// 			document.getElementById('end_date').value = '';
	// 		}
	// 	});

	// 	$('#timesheet_days_filter_list').change(function () {
	// 		get_table_data();
	// 		get_employee_wise_hours()
	// 	});
	// 	$('#end_date').change(function () {
	// 		get_table_data();
	// 		get_employee_wise_hours()
	// 	});
	// 	$('#task_filter_list').change(function () {
	// 		get_table_data();
	// 	});

	var TimesheetKanbanView = KanbanView.extend({
		config: _.extend({}, KanbanView.prototype.config, {
			Renderer: TimesheetKanbanRenderer,
		}),
	});
	viewRegistry.add('js_cls_timesheet_dashboard', TimesheetKanbanView);
});