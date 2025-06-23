odoo.define('sh_helpdesk.AbstractController', function (require) {
	var AbstractController = require('web.AbstractController');
	var ActivityController = AbstractController.include({
		/**
		 * @override
		 * @param {Widget} parent
		 * @param {DiagramModel} model
		 * @param {DiagramRenderer} renderer
		 * @param {Object} params
		 */
		init: function (parent, model, renderer, params) {
			this._super.apply(this, arguments);
			if (params.modelName == 'sh.ticket.dashboard') {
				$('.o_control_panel').css("display", "none");
			} else {
				$('.o_control_panel').css("display", "");
			}
		},
	});
});