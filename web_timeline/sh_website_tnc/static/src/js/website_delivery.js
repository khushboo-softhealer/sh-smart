odoo.define("sh_website_tnc.checkout", function(require) {
    "use strict";

    var core = require("web.core");
    var publicWidget = require("web.public.widget");
    var _t = core._t;
    var concurrency = require("web.concurrency");
    var dp = new concurrency.DropPrevious();
    
    publicWidget.registry.websiteSaleDelivery.include({
        /**
         * @override
         */
        _handleCarrierUpdateResultBadge: function(result) {
            this._super.apply(this, arguments);
            if ($("#show_terms_website").val() && !$("#chk_terms").is(":checked")) {
                var totalClicked = $("input[name='input_checkbox']:checkbox:checked").length;
                var len = $("input[type=checkbox]").length;
                if (totalClicked >= len) {
                    $("#tnc_msg_alert").addClass("o_hidden");
                    $("button[name='o_payment_submit_button']").attr("disabled", false);
                } else {
                    $("#tnc_msg_alert").removeClass("o_hidden");
                    $("button[name='o_payment_submit_button']").attr("disabled", true);
                }
            }
        },
    });
});
