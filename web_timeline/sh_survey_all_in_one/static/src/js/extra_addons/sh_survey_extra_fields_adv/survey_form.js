odoo.define("sh_survey_all_in_one.survey_3", function (require) {
    "use strict";

    var core = require("web.core");
    var publicWidget = require("web.public.widget");
    require("survey.form");

    var _t = core._t;
    var QWeb = core.qweb;

    require("sh_survey_all_in_one.survey");
	 
    publicWidget.registry.SurveyFormWidget.include({
   
        
        //--------------------------------------------------------------------------
        // Widget
        //--------------------------------------------------------------------------

        /**
         * @override
         */
    	start: function () {
            this._super.apply(this, arguments);
            //softhealer custom code
        },
        
        
        
        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        /**
         * @private
         */
        getLocation: function () {	
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(this.showPosition, this.errorCallback);
            } else {
                // x.innerHTML = "Geolocation is not supported by this browser.";
            }    	
        },    
        
        /**
         * @private
         */
        showPosition: function (position) {
            var sh_loc = position.coords.latitude + "&" + position.coords.longitude;
            $(".js_cls_tmpl_sh_location").val(sh_loc);
            //this.$el.val(sh_loc);	
        },  
        
        /**
         * @private
         */
        errorCallback: function (error) {
        },  
        
        
                
        
        
        /**
         * Will automatically focus on the first input to allow the user to complete directly the survey,
         * without having to manually get the focus (only if the input has the right type - can write something inside -)
         */
         _focusOnFirstInput: function () {
        	 
             this._super.apply(this, arguments);
             
     	    if (this.$(".js_cls_tmpl_sh_location").length ){   
     	    	this.getLocation();
     	    }	
			

         },

 
        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        /**
         * @overwrite
         */
        
        _prepareSubmitValues: function (formData, params) {
            var self = this;
            formData.forEach(function (value, key) {
                switch (key) {
                    case "csrf_token":
                    case "token":
                    case "page_id":
                    case "question_id":
                        params[key] = value;
                        break;
                }
            });

            // Get all question answers by question type
            this.$("[data-question-type]").each(function () {
				switch ($(this).data("questionType")) {
                    case "text_box":
                    case "char_box":
                    case "numerical_box":
                        params[this.name] = this.value;
                        break;
                    case "date":
                        params = self._prepareSubmitDates(params, this.name, this.value, false);
                        break;
                    case "datetime":
                        params = self._prepareSubmitDates(params, this.name, this.value, true);
                        break;
                    case "simple_choice_radio":
                    case "multiple_choice":
                        params = self._prepareSubmitChoices(params, $(this), $(this).data("name"));
                        break;
                    case "matrix":
                        params = self._prepareSubmitAnswersMatrix(params, $(this));
                        break;
                    case "que_sh_color":
                        params[this.name] = this.value;
                        break;
                    case "que_sh_email":
                        params[this.name] = this.value;
                        break;
                    case "que_sh_url":
                        params[this.name] = this.value;
                        break;
                    case "que_sh_time":
                        params[this.name] = this.value;
                        break;
                    case "que_sh_range":
                        params[this.name] = this.value;
                        break;
                    case "que_sh_week":
                        params[this.name] = this.value;
                        break;
                    case "que_sh_month":
                        params[this.name] = this.value;
                        break;
                    case "que_sh_password":
                        params[this.name] = this.value;
                        break;
                    case "que_sh_file":
                        params[this.name] = this.value;
                        break;
                    case "que_sh_address":
                        params = self._prepareSubmitAnswersAddress(params, this.name, $(this));
                        break;
                    case "que_sh_many2one":
                        params[this.name] = $(this).parent().find("input").val();
                        break;
                    case "que_sh_many2many":
                        params = self._prepareSubmitAnswersMany2many(params, $(this), $(this).attr("name"));
                        break;
                    case "que_sh_signature":
                        params = self._prepareSubmitAnswersSignature(params, this.name, $(this));
                        break;                        
                    case "que_sh_qrcode":
                        params[this.name] = this.value;
                        break;
                    case "que_sh_barcode":
						params[this.name] = this.value;
                        break;
                    case "que_sh_location":         
                        params[this.name] = this.value;
                        break;
                }
            });
        },
    });
});
