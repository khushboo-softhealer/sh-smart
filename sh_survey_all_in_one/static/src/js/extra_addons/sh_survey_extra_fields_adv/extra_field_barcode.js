$(document).ready(function () {
		
    function decodeOnce(codeReader, selectedDeviceId) {
        codeReader
            .decodeFromInputVideoDevice(selectedDeviceId, "video")
            .then((result) => {
                if ($("#js_id_sh_survey_barcode_mobile_result").attr("data-matrix-id")) {
                    var target_textbox_name = $("#js_id_sh_survey_barcode_mobile_result").attr("data-matrix-id");
                    var col_id = target_textbox_name.split("_")[1];
                    var row_id = target_textbox_name.split("_")[0];
                    $('input[data-col-id="' + col_id + '"][data-row-id="' + row_id + '"]').val(result.text);
                } else {
                    var target_textbox_name = $("#js_id_sh_survey_barcode_mobile_result").attr("name");
                    $('input[name="' + target_textbox_name + '"]').val(result.text);
                }

                //RESET READER
                codeReader.reset();

                //TODO: HIDE MODEL
                $("#js_id_sh_survey_extra_fields_adv_barcode_scan_modal").modal("hide");
            })
            .catch((err) => {
                console.error(err);
            });
    }

    let selectedDeviceId;

    const codeReader = new ZXing.BrowserMultiFormatReader();
    //const codeReader = new ZXing.BrowserBarcodeReader()

    codeReader
        .getVideoInputDevices()
        .then(function (result) {
            //THEN METHOD START HERE
            //const sourceSelect = $("#js_id_sh_survey_barcode_mobile_cam_select");
            const sourceSelect = document.getElementById("js_id_sh_survey_barcode_mobile_cam_select");

            _.each(result, function (item) {
                //self._add_filter(item.partner_id[0], item.partner_id[1], !active_partner, true);
                const sourceOption = document.createElement("option");
                sourceOption.text = item.label;
                sourceOption.value = item.deviceId;
                sourceSelect.appendChild(sourceOption);
            });

            //CUSTOM EVENT HANDLER START HERE

            /*
             * CUSTOM MODEL EVENT START HERE
             */

            /*
             * ============================================================
             * Open camera and start QR scanning when open modal Start
             * ============================================================
             */

            $("#js_id_sh_survey_extra_fields_adv_barcode_scan_modal").on("shown.bs.modal", function (ev) {
            	decodeOnce(codeReader, selectedDeviceId);
            });

            /*
             * ============================================================
             * Open camera and start QR scanning when open modal End
             * ============================================================
             */

            /* ============================================================
             * Stop Barcode Scanner in any case, when the modal is closed
             * ============================================================
             */

            $("#js_id_sh_survey_extra_fields_adv_barcode_scan_modal").on("hide.bs.modal", function () {
                //RESET READER
                codeReader.reset();
            });

            $(document).on("click", ".js_cls_sh_event_barcode_close_modal_btn", function () {
                //RESET READER
                codeReader.reset();
            });

            /*
             * ============================================================
             * Stop Barcode Scanner in any case, when the modal is closed
             * ============================================================
             */

            /*
             * CUSTOM MODEL EVENT ENDS HERE
             */

            /*
             * =============================
             * ONCHANGE SELECT CAMERA
             * =============================
             */

            $(document).on("change", "#js_id_sh_survey_barcode_mobile_cam_select", function () {
                // Does some stuff and logs the event to the console
                selectedDeviceId = sourceSelect.value;
                decodeOnce(codeReader, selectedDeviceId);
            });

            /*
             * ========================
             * WHEN CLICK START BUTTON.
             * ========================
             */
            $(document).on("click", ".js_cls_sh_survey_barcode_mobile_start_btn", function (event) {
            	if ($(event.currentTarget).parent().find("input").attr("data-col-id") && $(event.currentTarget).parent().find("input").attr("data-row-id")) {
                    var mtrix_id = $(event.currentTarget).parent().find("input").attr("data-row-id") + "_" + $(event.currentTarget).parent().find("input").attr("data-col-id");
                    $("#js_id_sh_survey_barcode_mobile_result").attr("data-matrix-id", mtrix_id);
                } else {
                    $("#js_id_sh_survey_barcode_mobile_result").attr("name", $(event.currentTarget).parent().find("input").attr("name"));
                    $("#js_id_sh_survey_barcode_mobile_result").removeAttr("data-matrix-id");
                }
            });
           
            //

            // CUSTOM ENENT HANDLER ENDS HERE

            // THEN METHOD ENDS HERE
        })
        .catch(function (reason) {});
});
