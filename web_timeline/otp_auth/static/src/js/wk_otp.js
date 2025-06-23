/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
odoo.define('otp_auth.wk_otp', function (require) {
    "use strict";
    
    var ajax = require('web.ajax');
    var core = require('web.core');
    const { session } = require('@web/session');
    const { loadJS } = require('@web/core/assets');
    var _t = core._t;
    var check=""

    $(document).ready(function() {
        var ValidUser = 0;
        if ($('#otpcounter').get(0)) {
            $("#otpcounter").html("<a class='btn btn-link pull-left wk_send' href='#'>" + _t("Send OTP") + "</a>");
            $(":submit").attr("disabled", true);
            $("#otp").css("display","none");
            $( ".oe_signup_form" ).wrapInner( "<div  id='wk_container'></div>");
        }
        
        $('.wk_send').on('click', function(e) {
            if($(this).closest('form').hasClass('oe_reset_password_form')){
                ValidUser = 1;
            }
            var email = $('#login').val();
            if (email) {
                if(validateEmail(email)) {
                    generateOtp(ValidUser);
                } else {
                    $('#wk_error').remove();
                    $(".field-confirm_password").after("<p id='wk_error' class='alert alert-danger'>Please enter a valid email address.</p>");
                }
            } else {
                $('#wk_error').remove();
                $(".field-confirm_password").after("<p id='wk_error' class='alert alert-danger'>Please enter an email address.</p>");
            }
        });
        $(this).on('click', '.wk_resend', function(e) {
            $(".wkcheck").remove();
            generateOtp(ValidUser);
        });
        verifyOtp();
    });

    function validateEmail(emailId) {
        var mailRegex = /^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/;
        return mailRegex.test(emailId);
    };

    function getInterval(otpTimeLimit) {
        var countDown = otpTimeLimit;
        $("#wkotp").show();
        var x = setInterval(function() {
            countDown = countDown - 1;
            $("#otpcounter").html("OTP will expire in " + countDown + " seconds.");            
            if (countDown < 0) {
                clearInterval(x);
                $(".wkcheck").remove()
                $("#otpcounter").html('<span><i class="fa fa-times-circle" style="font-size:15px;color:red"></i>Otp is expire.Please Click on resend button</span>');
                $("#otpcounter").append("<a class='btn btn-link pull-right wk_resend position-relative' href='#'>Resend OTP</a>");
                $(":submit").attr("disabled", true);
                check="invalid"
            }
            else{
                check=""
            }
        }, 1000);
    }
    // =================== CODE BY SAGAR 
    async function generateOtp(ValidUser) {
        const _publicKey = session.recaptcha_public_key;
    
        const email = $('#login').val();
        const mobile = $('#mobile').val();
        const userName = $('#name').val();
        const country_id = $('#country_id').val();
    
        $("#otp").val("");
        $("div#wk_loader").addClass('show');
        $('#wk_error, .alert.alert-danger').remove();
    
        try {
            console.log('log ==>> _publicKey',_publicKey);
            // Load reCAPTCHA 
            await loadJS(`https://www.recaptcha.net/recaptcha/api.js?render=${encodeURIComponent(_publicKey)}`);
    
            const token = await new Promise(resolve => {
                grecaptcha.ready(() => {
                    grecaptcha.execute(_publicKey, { action: 'generate_otp' }).then(resolve);
                });
            });
            console.log('log ==>> token',token);
            const data = await ajax.jsonRpc("/generate/otp", 'call', {
                email: email,
                userName: userName,
                mobile: mobile,
                country: country_id,
                validUser: ValidUser,
                g_recaptcha_response: token
            });
            console.log('log ==>> data',data);
    
            $("div#wk_loader").removeClass('show');
    
            if (data[0] === 1) {
                $('.wk_send').remove();
                getInterval(data[2]);
                $("#wkotp").after(`<p id='wk_error' class='alert alert-success'>${data[1]}</p>`);
                $("#otp").show().after($('#otpcounter'));
            } else {
                $(".field-confirm_password").after(`<p id='wk_error' class='alert alert-danger'>${data[1]}</p>`);
            }
        } catch (error) {
            console.error("OTP request failed:", error);
            $("div#wk_loader").removeClass('show');
            $(".field-confirm_password").after(`<p id='wk_error' class='alert alert-danger'>Something went wrong. Please try again.</p>`);
        }
    }
    
    // =================   COMMENTED BY SAGAR 
    // function generateOtp(ValidUser) {
    //     var email = $('#login').val();
    //     var mobile = $('#mobile').val();
    //     var userName = $('#name').val();
    //     var country_id = $('#country_id').val();
    //     check=""
    //     $("#otp").val("");
    //     $("div#wk_loader").addClass('show');
    //     $('#wk_error').remove();
    //     $('.alert.alert-danger').remove();

    //     ajax.jsonRpc("/generate/otp", 'call', {'email':email, 'userName':userName, 'mobile':mobile, 'country':country_id,'validUser':ValidUser})
    //     //ajax.jsonRpc("/sh_twitter_wall/get_tweet", 'call', {'email':email, 'userName':userName, 'mobile':mobile, 'country':country_id,'validUser':ValidUser})
    //         .then(function (data) {
    //             console.log('log ==>> GET RES FROM VALIDATION CODE ======');
    //             if (data[0] == 1 && check=="") {
    //                 $("div#wk_loader").removeClass('show');
    //                 $('.wk_send').remove();
    //                 getInterval(data[2]);
    //                 $("#wkotp").after("<p id='wk_error' class='alert alert-success'>" +data[1] + "</p>");
    //                 $("#otp").css("display","");
    //                 $('#otp').after($('#otpcounter'));
    //             } else {
    //                 $("div#wk_loader").removeClass('show');
    //                 $('#wk_error').remove();
    //                 $(".field-confirm_password").after("<p id='wk_error' class='alert alert-danger'>" +data[1] + "</p>");
    //             }
    //         });
    // }

    function verifyOtp() {
        $('#otp').bind('input propertychange', function() {
            if ($(this).val().length == 6) {
                var otp = $(this).val();
                var email = $('#login').val();
                // softhealer added email parameter here
                
                ajax.jsonRpc("/verify/otp", 'call', {'email':email,'otp':otp})
                    .then(function (data) {
                        if (data && check=="") {
                            $(".wkcheck").remove()
                            $('#otp').after("<i class='fa fa-check-circle wkcheck' aria-hidden='true'></i>");
                            $(".wkcheck").css("color","#3c763d");
                            $('#wkotp').removeClass("form-group has-error");
                            $('#wkotp').addClass("form-group has-success");
                            $(":submit").removeAttr("disabled").find('.fa-refresh').addClass('d-none');
                        } else {
                            $(":submit").attr("disabled", true);
                            $('#wkotp').removeClass("form-group has-success");
                            $('#wkotp').addClass("form-group has-error");
                        }
                    });
            } else {
                $(":submit").attr("disabled", true);
                $(".wkcheck").remove();
                $('#wkotp').removeClass("form-group has-success");
                $('#wkotp').removeClass("form-group has-error");
                $('#wkotp').addClass("form-group");
            }
        });
    }

})