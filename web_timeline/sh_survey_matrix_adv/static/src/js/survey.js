odoo.define("sh_survey_matrix_adv.survey", function (require) {
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

            // IN ORDER TO FIX ONE COMMENT SUBMITED WITH TEXTAREAD INPUT 
            // IN HTML INSPECT VIEW FOUND THAT MULTIPLE TEXTAREA FIELD RENDERED WHEN CLICK ON 
            // TEXTAREA FIELD IN CUSTOM MATRIX SO BELOW IS A LITTLE HACK TO FIX IT.
            if ($matrixTable.find(".sh_textarea").length) {
                return params;
            }

            params = self._prepareSubmitComment(params, $matrixTable.closest(".js_question-wrapper"), $matrixTable.data("name"), true);
            return params;
        },

        /**
         * Will automatically focus on the first input to allow the user to complete directly the survey,
         * without having to manually get the focus (only if the input has the right type - can write something inside -)
         */
        _focusOnFirstInput: function () {
            this._super.apply(this, arguments);

            if (this.$("input[type='range']").length) {
                this.$("input[type='range']").trigger('input')
            }
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
