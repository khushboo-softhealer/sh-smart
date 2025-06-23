odoo.define("sh_website_tnc.custom_js", function (require) {
    var ajax = require("web.ajax");
	var publicWidget = require('web.public.widget');

	publicWidget.registry.ShWebsiteTncCustomJs = publicWidget.Widget.extend({
		selector: '.oe_cart',
	    events: {
			'click input.chk_terms_multi':'_onClickCheckInput',
			'click #btn_website_terms_conditions':'_onClickOpenModal',
			'click #btn_website_terms_conditions_multi':'_onClickOpenMultiModal',
	    },

		/**
         * @override
         */
        start: function () {
			var self = this;
			this._checkClicked()
			return this._super(...arguments);
		},
		
		_onClickCheckInput: function () {
			this._checkClicked()
		},
		
		_checkClicked:function(){
			var totalClicked = $("input.chk_terms_multi:checked").length;
            var len = $("input.chk_terms_multi").length;
            if (totalClicked >= len) {
                $("#tnc_msg_alert").css("display","none");
                $("button[name='o_payment_submit_button']").attr("disabled", false).css({"pointer-events": "unset", "opacity": "1"});
            } else {
                $("#tnc_msg_alert").css("display","block");
                $("button[name='o_payment_submit_button']").attr("disabled", true).css({"pointer-events": "none", "opacity": "0.65"});;
            }
		},
		
		_onClickOpenModal:function(){
			var self = this;
			var $modal = self.$el.find('#website_terms_modal')
			$modal.modal('show')
		},
		
		_onClickOpenMultiModal:function(ev){
			var self = this;
			var $btn = $(ev.currentTarget);
			var target = $btn.attr('data-target')
			var $modal = self.$el.find(target)
			if($modal){
				$modal.modal('show')
			}
						
		},

	});
});
