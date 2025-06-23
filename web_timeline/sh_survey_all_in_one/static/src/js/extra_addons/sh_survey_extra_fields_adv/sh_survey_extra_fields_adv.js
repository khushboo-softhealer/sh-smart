var sh_survey_extra_fields_adv_stream_ref = null;

function sh_survey_extra_fields_adv_release() {
    var tracks = sh_survey_extra_fields_adv_stream_ref && sh_survey_extra_fields_adv_stream_ref.getVideoTracks();
    if (tracks && tracks.length) {
        tracks[0].stop();
    }
    sh_survey_extra_fields_adv_stream_ref = null;
    $(".btn").removeAttr("disabled");
}

function start_sh_survey_extra_fields_adv() {
    //var video = document.createElement("video");
    var video = document.getElementById("js_id_sh_survey_extra_fields_adv_video");
    var canvasElement = document.getElementById("js_id_sh_survey_extra_fields_adv_canvas");
    var canvas = canvasElement.getContext("2d");
    var loadingMessage = document.getElementById("js_id_sh_survey_extra_fields_adv_loading_msg");
    var outputContainer = document.getElementById("js_id_sh_survey_extra_fields_adv_output");
    var outputMessage = document.getElementById("js_id_sh_survey_extra_fields_adv_output_msg");
    var outputData = document.getElementById("js_id_sh_survey_extra_fields_adv_output_data");

    function drawLine(begin, end, color) {
        canvas.beginPath();
        canvas.moveTo(begin.x, begin.y);
        canvas.lineTo(end.x, end.y);
        canvas.lineWidth = 4;
        canvas.strokeStyle = color;
        canvas.stroke();
    }

    // Use facingMode: environment to attemt to get the front camera on phones
    navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } }).then(function (stream) {
        sh_survey_extra_fields_adv_stream_ref = stream;
        video.srcObject = stream;
        video.setAttribute("playsinline", true); // required to tell iOS safari we don't want fullscreen
        video.play();
        requestAnimationFrame(tick);
    });

    function tick() {
        loadingMessage.innerText = "⌛ Loading video...";
        if (video.readyState === video.HAVE_ENOUGH_DATA) {
            loadingMessage.hidden = true;
            canvasElement.hidden = false;
            outputContainer.hidden = false;

            canvasElement.height = video.videoHeight;
            canvasElement.width = video.videoWidth;
            canvas.drawImage(video, 0, 0, canvasElement.width, canvasElement.height);
            var imageData = canvas.getImageData(0, 0, canvasElement.width, canvasElement.height);
            var code = jsQR(imageData.data, imageData.width, imageData.height, {
                inversionAttempts: "dontInvert",
            });
            if (code) {
                drawLine(code.location.topLeftCorner, code.location.topRightCorner, "#FF3B58");
                drawLine(code.location.topRightCorner, code.location.bottomRightCorner, "#FF3B58");
                drawLine(code.location.bottomRightCorner, code.location.bottomLeftCorner, "#FF3B58");
                drawLine(code.location.bottomLeftCorner, code.location.topLeftCorner, "#FF3B58");
                outputMessage.hidden = true;
                outputData.parentElement.hidden = false;
                outputData.innerText = code.data;
                //SH CODE START HERE
                $('input[name="sh_survey_extra_fields_adv"]').val(code.data);
                $('input[name="sh_survey_extra_fields_adv"]').change();

                var target_textbox_name = $("#js_id_sh_survey_extra_fields_adv_output_data").attr("name");
                $('input[name="' + target_textbox_name + '"]').val(code.data);
                $("#js_id_sh_survey_extra_fields_adv_qrs_modal").modal("hide");

                //SH CODE ENDS HERE
            } else {
                outputMessage.hidden = false;
                outputData.parentElement.hidden = true;
            }
        }
        requestAnimationFrame(tick);
    }
}

/*
 * ============================================================
 * Open camera and start QR scanning when open modal Start
 * ============================================================
 */

$("#js_id_sh_survey_extra_fields_adv_qrs_modal").on("shown.bs.modal", function (ev) {
    $('input[name="sh_survey_extra_fields_adv"]').val("");
    $('input[name="sh_survey_extra_fields_adv"]').change();
    start_sh_survey_extra_fields_adv();
});

/*
 * ============================================================
 * Open camera and start QR scanning when open modal End
 * ============================================================
 */

/* ============================================================
 * Stop QR Scanner in any case, when the modal is closed
 * ============================================================
 */

$("#js_id_sh_survey_extra_fields_adv_qrs_modal").on("hide.bs.modal", function () {
    //stop camera here
    sh_survey_extra_fields_adv_release();
});

$(document).on("click", ".js_cls_sh_event_qrs_close_modal_btn", function () {
    //stop camera here
    sh_survey_extra_fields_adv_release();
});

/*
 * ============================================================
 * Stop QR Scanner in any case, when the modal is closed
 * ============================================================
 */

/*
 * ============================================================
 * Location JS
 * ============================================================
 */

$(document).ready(function () {
    var is_survey_fill = window.location.href.indexOf("/survey/fill/");
    if ($(".js_cls_tmpl_sh_location").length) {
        getLocation();
    }

    function getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(showPosition, errorCallback);
        } else {
            // x.innerHTML = "Geolocation is not supported by this browser.";
        }
    }
    function errorCallback(error) {
    }

    function showPosition(position) {
        var sh_loc = position.coords.latitude + "&" + position.coords.longitude;
        $(".js_cls_tmpl_sh_location").val(sh_loc);
    }
});

/*
 * ============================================================
 * Location JS
 * ============================================================
 */
