odoo.define("sh_survey_all_in_one.survey", function (require) {
    "use strict";

    var core = require("web.core");
    var publicWidget = require("web.public.widget");
    require("survey.form");

    var _t = core._t;

    publicWidget.registry.SurveyFormWidget.include({
    	
    	
        _prepareSubmitAnswersMatrix: function (params, $matrixTable) {
            var self = this;
            $matrixTable.find("input").each(function () {
                if (this.type != "file") {
                    if ($(this).data("col-id") == this.value && $(this).prop("checked") == true) {
                        params = self._prepareSubmitAnswerMatrix(params, $matrixTable.data("name"), $(this).data("rowId"), this.value);
                    } else if ($(this).data("col-id") != this.value) {
                        params = self._prepareSubmitAnswerMatrixCustom(params, $matrixTable.data("name"), $(this).data("rowId"), $(this).data("col-id"), this.value);
                    }
                }
            });
            $matrixTable.find(".sh_textarea").each(function () {
                if (this.type != "file") {
                    if ($(this).data("col-id") == this.value && $(this).prop("checked") == true) {
                        params = self._prepareSubmitAnswerMatrix(params, $matrixTable.data("name"), $(this).data("rowId"), this.value);
                    } else if ($(this).data("col-id") != this.value) {
                        params = self._prepareSubmitAnswerMatrixCustom(params, $matrixTable.data("name"), $(this).data("rowId"), $(this).data("col-id"), this.value);
                    }
                }
            });
			
            params = self._prepareSubmitComment(params, $matrixTable.closest(".js_question-wrapper"), $matrixTable.data("name"), true);
            return params;
        },

        _prepareSubmitAnswerMatrix: function (params, questionId, rowId, colId, isComment) {
            var value = questionId in params ? params[questionId] : {};
			
            if (isComment) {
                value["comment"] = colId;
            } else {
                if (rowId in value) {
                    value[rowId].push(colId);
                } else {
                    value[rowId] = [colId];
                }
            }
            params[questionId] = value;
            return params;
        },
        _prepareSubmitAnswerMatrixCustom: function (params, questionId, rowId, colId, data, isComment) {
            var value = questionId in params ? params[questionId] : {};
			if (isComment) {
                value["comment"] = colId;
            } else if (colId != data) {
                if (rowId in value) {
                    value[rowId + "_" + colId].push(data);
                } else {
                    value[rowId + "_" + colId] = [data];
                }
            } else {
                if (rowId in value) {
                    value[rowId].push(data);
                } else {
                    value[rowId] = [data];
                }
            }
            params[questionId] = value;
            return params;
        },
    });
});
