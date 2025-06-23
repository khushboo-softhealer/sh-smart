odoo.define('sh_website_helpdesk.helpdesk_ticket_create_page', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    // CODE BY KISHAN GHELNAI 
    const { ReCaptcha } = require('google_recaptcha.ReCaptchaV3'); 

    publicWidget.registry.HelpdeskTicketPage = publicWidget.Widget.extend({
        selector: '.sh_website_helpdesk_form',
        events: {
            'change #file': '_onChangeFile',
            'change #edition': '_onChangeEdition',
            'change #invoice_file': '_onChangeInvoiceFile',
            'change #category': '_onChangeCategory',
            'change #ticket_type': '_onChangeTicketType',
            'click #submit_ticket': '_onClickSubmitTicket',
        },


        /**
        * @ code by kishan ghelani
        */
        init() {
            this._super(...arguments);
            this._recaptcha = new ReCaptcha();
        },
      


        /**
        * @override
        *   * @ code by kishan ghelani
        */
        willStart() {
            this._recaptcha.loadLibs();
            return this._super(...arguments);
        },
      


        /**
         * @override
         */
        start: function () {
            var params = {}
            this._rpc({ route: '/ticket-data', params })
                .then(result => {
                    const datas = JSON.parse(result);
                    if (datas.login_user == "1" && (datas.name || datas.email || datas.mobile)) {
                        if (datas.name) {
                            $("#contact_name").val(datas.name);
                        }
                        if (datas.email) {
                            $("#email").val(datas.email);
                        }
                        if (datas.mobile) {
                            $("#mobile").val(datas.mobile);
                        }
                        $('#loading').hide();
                    } else if (datas.login_user == "0") {
                        $("#contact_name").val("");
                        $("#email").val("");
                        $("#mobile").val("");
                        $('#loading').hide();
                    }
                });

            var queryString = window.location.search;
            var params = {};
            if (queryString) {
                queryString = queryString.substring(1); // Remove the leading '?'
                var paramPairs = queryString.split('&');
                paramPairs.forEach(function(pair) {
                    var parts = pair.split('=');
                    var value = decodeURIComponent(parts[1]);
                    if(value == "technical_support" || value == "demo_request" || value == "new_customization"){
                        $('#ticket_type').trigger('change');
                    }

                });
            }
            
            return this._super.apply(this, arguments);
        },
        

        // MAKE TOTAL OF ALL FILES SIZE AND CHECK WITH ATTACHMENT SIZE LIMIT
        _onChangeFile: function (ev) {

            // // CONVERT FILE TO BASE64 CODE
            // const toBase64 = file => new Promise((resolve, reject) => {
            //     const reader = new FileReader();
            //     reader.readAsDataURL(file);
            //     reader.onload = () => resolve(reader.result);
            //     reader.onerror = error => reject(error);
            // });

            // var files_base_64_codes = []
            // for (let index = 0; index < ev.currentTarget.files.length; index++) {
            //     const file = ev.currentTarget.files[index];
            //     files_base_64_codes.push(await toBase64(file))
            // }

            var all_attachment_size = 0.0
            for (let index = 0; index < ev.currentTarget.files.length; index++) {
                const element = ev.currentTarget.files[index];
                all_attachment_size = all_attachment_size + element.size
            }
            var file_size_limit = $('#file').attr('data-attachment-size')
            if (all_attachment_size / 1000 > parseInt(file_size_limit)) {
                alert("The maximum file size you may attach is " + file_size_limit + "KB")
                $('#file').val('')
                return false
            }
        },


        // CREATE DYNAMIC ODOO HOST OPTIONS BASED ON EDITIONS
        _onChangeEdition: function (ev) {
            let editionId = $(ev.target).val();

            // Empty the 'hosted' element
            $('#hosted').empty();

            // Make an RPC call with the edition ID as a parameter
            this._rpc({
                route: '/odoo-hosted-on',
                params: { edition_id: editionId }
            }).then((result) => {
                // Parse the result from the RPC call
                let datas = JSON.parse(result);

                // Initialize an empty string to hold the options for the 'hosted' element
                let optionsStr = '';

                // If there are hosted IDs in the result
                if (datas.hosted_ids) {
                    // Iterate through each hosted ID
                    datas.hosted_ids.forEach((element) => {
                        // Add an option to the options string with the ID and name of the hosted element
                        optionsStr += `<option value=${element.id}>${element.name}</option>`;
                    });

                    // Append the options to the 'hosted' element
                    $('#hosted').append(`<option value='odoo_hosted_on'>Select Odoo Hosted On</option>`);
                    $('#hosted').append(optionsStr);

                    // Remove any options from the 'hosted' element that have an empty value or text
                    $('#hosted option')
                        .filter(function () {
                            return !this.value || $.trim(this.value).length == 0 || $.trim(this.text).length == 0;
                        }).remove();
                }
                // If there are no hosted IDs in the result
                else {
                    // Empty the 'hosted' element
                    $('#hosted').empty();
                }
            });
        },

        _onChangeInvoiceFile: function (ev) {
            if ($(ev.target).val() != '') {
                $('#error_invoice').hide();
                $('#error_invoice').css('margin-top:0px');
            }
        },

        // GET PRODUCTS BASE ON CATEGORY AND VISIBLE INVOICE FILE DIV
        _onChangeCategory: function (ev) {
            
            const categoryId = $(ev.target).val();
            this._showLoading();
            this._rpc({ route: '/product-data', params: { category_id: categoryId } })
                .then((result) => {
                    const { status, products } = JSON.parse(result);
                    
                    if (status) {
                        $('#sh_multiple_products').remove();
                        $('#products_div').html(products);
                        $('#sh_multiple_products').select2({ placeholder: 'Select Product' });
                    } else {
                        $('#ticket_type').val('type');
                        $('#products_div').addClass('o_hidden');
                        $('#invoice_div').addClass('o_hidden');
                    }
                })
                .finally(() => this._hideLoading());
        },
        _showLoading() {
            $('#loading').show();
        },
        _hideLoading() {
            $('#loading').hide();
        },

        // CHECK TICKET TYPE REQUIRED PRODUCTS AND INVOICE PROOF OR NOT.
        _onChangeTicketType: function (ev) {
            var self = this;
            self._showLoading();
            const typeId = $(ev.target).val();
            const params = { type_id: typeId };

            this._rpc({ route: '/ticket-type', params })
                .then(result => {
                    const { invoice, product } = JSON.parse(result);
                    self._hideLoading();
                    $('#invoice_div').toggleClass('o_hidden', !invoice);
                    $('#products_div').toggleClass('o_hidden', !product);
                });
        },


        _onClickSubmitTicket: async function (ev) {
            var self = this;
            ev.preventDefault();

            // ReCAPTCHA validation
            // code by kishan ghelani
            const tokenCaptcha = await self._recaptcha.getToken("sh_recaptcha_demo_form");
            if (tokenCaptcha.error) {
                self.displayNotification({
                type: "danger",
                title: _t("Error"),
                message: tokenCaptcha.error,
                sticky: true
                });
                return false;
            }

            var sh_token = tokenCaptcha.token;
            $(self.$target).find('input[name="recaptcha_token_response"]').val("");

            var products = '';
            $.each($("input[name='sh_multiple_products']:checked"), function () {
                if (products == '') {
                    products = $(this).val();
                }
                else {
                    products = products + ',' + $(this).val();
                }
            });

            var has_captcha = '';
            if ($(document).find(".g-recaptcha").length) {
                has_captcha = grecaptcha.getResponse();
            }

            this._rpc({
                route: '/check-validation',
                params: {
                    'version': $('#version').val(),
                    'products': $('#sh_multiple_products').val(),
                    'contact_name': $('#contact_name').val(),
                    'email': $('#email').val(),
                    'mobile': $('#mobile').val(),
                    'category': $('#category').val(),
                    'ticket_type': $('#ticket_type').val(),
                    'edition': $('#edition').val(),
                    'files': $('#invoice_file').val(),
                    'g-recaptcha-response': has_captcha,
                    'odoo_hosted': $('#hosted').val(),
                    // code by kishan ghelani
                    // 'recaptcha_token_response': tokenCaptcha.token, 
                },
            }).then(function (result) {
                var datas = JSON.parse(result);
                if (datas.exist == false) {
                    alert("Selected version is invalid.");
                    return false;
                }
                else {
                    if (datas.name_msg) {
                        $('#error_name').show();
                        $('#error_name').html(datas.name_msg);
                        $('#error_name').css('margin-top:10px');
                        $('#error_email').hide();
                        $('#error_mobile').hide();
                        $('#error_category').hide();
                        $('#error_type').hide();
                        $('#error_edition').hide();
                        $('#error_version').hide();
                        $('#error_products').hide();
                        $('#error_invoice').hide();
                        $('#error_captcha').hide();
                        $('#error_hosted').hide();
                        return false;
                    }
                    if (datas.email_msg) {
                        $('#error_name').hide();
                        $('#error_mobile').hide();
                        $('#error_email').show();
                        $('#error_email').html(datas.email_msg);
                        $('#error_email').css('margin-top:10px');
                        $('#error_category').hide();
                        $('#error_type').hide();
                        $('#error_edition').hide();
                        $('#error_version').hide();
                        $('#error_products').hide();
                        $('#error_invoice').hide();
                        $('#error_captcha').hide();
                        $('#error_hosted').hide();
                        return false;
                    }
                    if (datas.mobile_msg) {
                        $('#error_name').hide();
                        $('#error_email').hide();
                        $('#error_mobile').show();
                        $('#error_mobile').html(datas.mobile_msg);
                        $('#error_mobile').css('margin-top:10px');
                        $('#error_category').hide();
                        $('#error_type').hide();
                        $('#error_edition').hide();
                        $('#error_version').hide();
                        $('#error_products').hide();
                        $('#error_invoice').hide();
                        $('#error_captcha').hide();
                        $('#error_hosted').hide();
                        return false;
                    }
                    if (datas.category_msg) {
                        $('#error_name').hide();
                        $('#error_email').hide();
                        $('#error_mobile').hide();
                        $('#error_category').show();
                        $('#error_category').html(datas.category_msg);
                        $('#error_category').css('margin-top:10px');
                        $('#error_type').hide();
                        $('#error_edition').hide();
                        $('#error_version').hide();
                        $('#error_products').hide();
                        $('#error_invoice').hide();
                        $('#error_captcha').hide();
                        $('#error_hosted').hide();
                        return false;
                    }
                    if (datas.type_msg) {
                        $('#error_name').hide();
                        $('#error_email').hide();
                        $('#error_mobile').hide();
                        $('#error_category').hide();
                        $('#error_type').show();
                        $('#error_type').html(datas.type_msg);
                        $('#error_type').css('margin-top:10px');
                        $('#error_edition').hide();
                        $('#error_version').hide();
                        $('#error_products').hide();
                        $('#error_invoice').hide();
                        $('#error_captcha').hide();
                        $('#error_hosted').hide();
                        return false;
                    }
                    if (datas.products_msg) {
                        $('#error_name').hide();
                        $('#error_email').hide();
                        $('#error_mobile').hide();
                        $('#error_category').hide();
                        $('#error_type').hide();
                        $('#error_edition').hide();
                        $('#error_version').hide();
                        $('#error_captcha').hide();
                        $('#error_products').show();
                        $('#error_products').html(datas.products_msg);
                        $('#error_products').css('margin-top:10px');
                        $('#error_invoice').hide();
                        $('#error_hosted').hide();
                        return false;
                    }
                    if (datas.invoice_msg) {
                        $('#error_name').hide();
                        $('#error_email').hide();
                        $('#error_mobile').hide();
                        $('#error_category').hide();
                        $('#error_type').hide();
                        $('#error_edition').hide();
                        $('#error_version').hide();
                        $('#error_products').hide();
                        $('#error_captcha').hide();
                        $('#error_invoice').show();
                        $('#error_invoice').html(datas.invoice_msg);
                        $('#error_invoice').css('margin-top:10px');
                        $('#error_hosted').hide();
                        return false;
                    }
                    if (datas.edition_msg) {
                        $('#error_edition').show();
                        $('#error_edition').html(datas.edition_msg);
                        $('#error_edition').css('margin-top:10px');
                        $('#error_name').hide();
                        $('#error_email').hide();
                        $('#error_mobile').hide();
                        $('#error_category').hide();
                        $('#error_type').hide();
                        $('#error_version').hide();
                        $('#error_products').hide();
                        $('#error_invoice').hide();
                        $('#error_captcha').hide();
                        $('#error_hosted').hide();
                        return false;
                    }
                    if (datas.error_hosted_msg) {
                        $('#error_hosted').show();
                        $('#error_hosted').html(datas.error_hosted_msg);
                        $('#error_hosted').css('margin-top:10px');
                        $('#error_name').hide();
                        $('#error_email').hide();
                        $('#error_mobile').hide();
                        $('#error_category').hide();
                        $('#error_type').hide();
                        $('#error_version').hide();
                        $('#error_products').hide();
                        $('#error_invoice').hide();
                        $('#error_captcha').hide();
                        $('#error_edition').hide();
                        return false;
                    }
                    if (datas.version_msg) {
                        $('#error_version').show();
                        $('#error_version').html(datas.version_msg);
                        $('#error_version').css('margin-top:10px');
                        $('#error_name').hide();
                        $('#error_email').hide();
                        $('#error_mobile').hide();
                        $('#error_category').hide();
                        $('#error_type').hide();
                        $('#error_edition').hide();
                        $('#error_products').hide();
                        $('#error_invoice').hide();
                        $('#error_captcha').hide();
                        $('#error_hosted').hide();
                        return false;
                    }
                    // code by kishan ghelani
                    // if (datas.google_captcha_msg) {
                    //     $('#error_captcha').show();
                    //     $('#error_captcha').html(datas.google_captcha_msg);
                    //     $('#error_captcha').css('margin-top:10px');
                    //     $('#error_version').hide();
                    //     $('#error_name').hide();
                    //     $('#error_email').hide();
                    //     $('#error_mobile').hide();
                    //     $('#error_category').hide();
                    //     $('#error_type').hide();
                    //     $('#error_edition').hide();
                    //     $('#error_products').hide();
                    //     $('#error_invoice').hide();
                    //     $('#error_hosted').hide();
                    //     return false;
                    // }
                    return $(self.$target).submit();
                }
                
            });
        },
    })
})