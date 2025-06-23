odoo.define('softhealer_website_base.custom_website_form', function (require) {
    'use strict';
    var Dialog = require("web.Dialog");
    const { ReCaptcha } = require('google_recaptcha.ReCaptchaV3');
    const { _t, qweb } = require('web.core');
    const { loadJS, loadCSS } = require('@web/core/assets');

    var rpc = require("web.rpc");

    var QWeb = qweb;
    var publicWidget = require("web.public.widget");

    publicWidget.registry.HelpdeskTicketSolutionPage = publicWidget.Widget.extend({
        selector: '#wrapwrap',
        events: {
            'click #sh_create_ticket_from_solution_pages': '_onClickSubmitTicket',
            'click #sh_custom_create_ticket_contact_us_form': '_onClickContactUsSubmitTicket',},

        /**
         * @constructor
         */
        init() {
            this._super(...arguments);
            this._recaptcha = new ReCaptcha();
        },

        /**
         * @override
        */
       async willStart() {
            // Load Libs
            try {
                this.countryCode = await this.getCountryCode();
                // this.countryCode = '' || 'US';
                
                // this.countryCode = '';

                await loadJS('/softhealer_website_base/static/src/lib/intl-tel-input/intl-tel-input.js');
                await loadCSS('/softhealer_website_base/static/src/lib/intl-tel-input/intl-tel-input.css');
            } catch (error) {
                console.error('Error:', error);
            }

           return this._recaptcha.loadLibs();
        },
        async start() {
            this._super(...arguments);
            // this._open_country_selection()
            const template = document.createElement('template');
            template.innerHTML = qweb.render("google_recaptcha.recaptcha_legal_terms");
            this.$target.find('#sh_recaptcha_legal_terms').append(template.content.firstElementChild);

            // For Static Form
            const countryInput = document.querySelector("#sh_custom_contact_us_form_contact_no");
            if (countryInput){
                
                this.iti = window.intlTelInput(countryInput, {
                    initialCountry: this.countryCode.toLowerCase() || 'US',
                    loadUtils: () => import("https://cdn.jsdelivr.net/npm/intl-tel-input@25.3.1/build/js/utils.js"),
                });
                this.errorMap = ["Invalid number", "Invalid country code", "Too short", "Too long", "Invalid number"];
            } 
        },

        async getCountryCode() {
            const apiUrls = [
                'http://ip-api.com/json/',
                'https://ipapi.co/json',
                'https://ipwhois.app/json/'
            ];

            for (let url of apiUrls) {
                try {
                    // Fetch response from the API
                    let response = await fetch(url);
                    
                    // If the response is OK, parse the JSON and check if the country code is available
                    if (response.ok) {
                        let data = await response.json();
                        if (data.countryCode || data.country_code) {
                            console.log('log ==>> data ==',data);
                            console.log('log ==>> url ==',url);
                            return data.countryCode || data.country_code; // Return the country code if found
                        }
                    }
                } catch (error) {
                    // If there is an error (e.g., network issue), it will proceed to the next API
                    console.log(`Error with ${url}: ${error.message}`);
                }
            }

            return 'US';
        },

        get_query_params(ev){
            var query_params = new URLSearchParams(window.location.search);
            var current_target = $(ev.currentTarget)
            // console.log("--------------> 44",current_target);
            // console.log("--------------> 44 window.location.search",window.location.search);
            // console.log("--------------> 45 query_params",query_params);
            // console.log("--------------> 46 query_params.utm_campaign",query_params.utm_campaign);
            // console.log("--------------> 47 query_params.utm_medium",query_params.utm_medium);
            // console.log("--------------> 48 query_params.utm_source",query_params.utm_source);
            // console.log("--------------> 49 current_target.data('utm_medium')",current_target.data('utm_medium'));
            // console.log("--------------> 50 current_target.data('utm_campaign')",current_target.data('utm_campaign'));
            // console.log("--------------> 51 current_target.data('utm_source')",current_target.data('utm_source'));
            // console.log("--------------> 53 query_params.get('utm_medium')",query_params.get('utm_medium'));
            // console.log("--------------> 54 query_params.get('utm_campaign')",query_params.get('utm_campaign'));
            // console.log("--------------> 55 query_params.get('utm_source')",query_params.get('utm_source'));

            return {'medium_name': query_params.get('utm_medium') || current_target.data('utm_medium'),
                    'campaign_name' : query_params.get('utm_campaign') || current_target.data('utm_campaign'),
                        'source_name' : query_params.get('utm_source') || current_target.data('utm_source')
                             
            }
        },
        _onClickSubmitTicket: async function (ev) {
            var query_params = this.get_query_params(ev)
            var self = this;
            ev.preventDefault();    
            const errorMap = ["Invalid number", "Invalid country code", "Too short", "Too long", "Invalid number"];

            var buttonText = $(ev.currentTarget).find('.prim_text').clone().children().remove().end().text().trim();
            var content = QWeb.render("softhealer_website_base.sh_create_ticket_from_website_pages");
           
            var dialog = new Dialog(this, {
                size: "medium",
                // title: _t("Let's connect..!"),
                title: buttonText || _t("Let's connect..!"), 
                $content: content,
                buttons: [
                    {
                        text: 'Submit',
                        classes: 'btn-primar btn rippler rippler-default',
                        click: async function (ev) {
                            ev.preventDefault();
                            var $button = $(ev.currentTarget);
                            $button.prop("disabled", true);
                            // Get form values
                            var partnerName = $('#solution_page_custom_website_form_partner_name').val();
                            var email = $('#solution_page_custom_website_form_email').val();
                            var company = $('#solution_page_custom_website_form_company').val();
                            var country = self.iti_pop_up.s.iso2.toUpperCase() || self.countryCode.toUpperCase();
                            // var country = self.countryCode || ;
                            var contact_no = $('#solution_page_custom_website_form_contact_no').val();
                            var description = $('#solution_page_custom_website_form_description').val();
                            var utm_source = query_params.source_name;
                            var utm_medium = query_params.medium_name;
                            var utm_campaign = query_params.campaign_name;

                            // Reset styles and error messages
                            resetFormStylesAndMessages();

                            // Client-side validation
                            if (!validateField(partnerName, '#solution_page_custom_website_form_partner_name', "Please enter your name.") ||
                                !validateField(company, '#solution_page_custom_website_form_company', "Please enter your company name.") ||
                                !validateEmail(email) ||
                                !validateField(country, '#solution_page_custom_website_form_contact_no', "Please select your Country.") ||
                                !validateContactNo(contact_no) ||
                                !validateField(description, '#solution_page_custom_website_form_description', "Please enter Requirements.")) {
                                $button.prop("disabled", false);
                                return false;
                            }

                            // ReCAPTCHA validation
                            const tokenCaptcha = await self._recaptcha.getToken("sh_recaptcha_demo_form");
                            console.log('log ==>> tokenCaptcha 1111',tokenCaptcha);
                            if (tokenCaptcha.error) {
                                self.displayNotification({
                                    type: "danger",
                                    title: _t("Error"),
                                    message: tokenCaptcha.error,
                                    sticky: true
                                });
                                return false;
                            }
                            // Submit form data via RPC
                            this._rpc({
                                route: '/softhealer_website_base/website_create_ticket_page',
                                params: {
                                    'recaptcha_token_response': tokenCaptcha.token,
                                    'solution_page_custom_website_form_partner_name': partnerName,
                                    'solution_page_custom_website_form_company': company,
                                    'solution_page_custom_website_form_email': email,
                                    'solution_page_custom_website_form_country': country,
                                    'solution_page_custom_website_form_contact_no':contact_no,
                                    'solution_page_custom_website_form_description': description,
                                    'custom_form_check_url': window.location.href,
                                    'custom_form_utm_campaign':utm_campaign,
                                    'custom_form_utm_source' : utm_source,
                                    'custom_form_utm_medium' : utm_medium,
                                },
                            }).then(function (result) {
                                console.log('\n\n log ==>> result',result);
                                handleResponse(result, dialog);
                            });
                        },
                    }
                ],
            }).open();

            
            dialog.opened().then(function () {
                    dialog.$modal.addClass("sh_create_ticket_from_solution_design");

                    const countryInput = dialog.$el.find("#solution_page_custom_website_form_contact_no");
                    if(countryInput){
                       self.iti_pop_up = window.intlTelInput(countryInput[0], {
                            initialCountry: self.countryCode.toLowerCase(),
                            loadUtils: () => import("https://cdn.jsdelivr.net/npm/intl-tel-input@25.3.1/build/js/utils.js"),
                        });
                    }
                });

            // Function to reset form fields styles and error messages
            function resetFormStylesAndMessages() {
                $('#error_message').hide();
                $('#solution_page_custom_website_form_partner_name, #solution_page_custom_website_form_email, #solution_page_custom_website_form_company, #solution_page_custom_website_form_contact_no, #solution_page_custom_website_form_description').removeAttr('style');
            }

            // Function to validate fields
            function validateField(value, fieldId, errorMessage) {
                if (!value || value.trim() === '') {
                    displayErrorMessage(errorMessage, fieldId);
                    return false;
                }
                return true;
            }

            // Function to validate email
            function validateEmail(email) {
                if (!email || email.trim() === '') {
                    displayErrorMessage("Please enter your email address.", '#solution_page_custom_website_form_email');
                    return false;
                } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
                    displayErrorMessage("Please enter a valid email address.", '#solution_page_custom_website_form_email');
                    return false;
                }
                return true;
            }

            function validateContactNo(contact_no){
                if (!contact_no || contact_no.trim() === '') {
                    displayErrorMessage("Please enter your contact no.", '#solution_page_custom_website_form_contact_no');
                    return false;
                // } else if (!/^\d+$/.test(contact_no)) {
                } else if (! self.iti_pop_up.isValidNumber()) {
                    const errorCode = self.iti_pop_up.getValidationError();
                    const msg = "Please check contact number : " + errorMap[errorCode] || "Invalid number";
                    displayErrorMessage(msg, '#solution_page_custom_website_form_contact_no');
                    return false;
                }
                return true;
            }

            // Function to display error messages
            function displayErrorMessage(message, fieldId) {
                $('#error_message').show().html(message).css('margin-top', '10px');
                $(fieldId).css('border', '1px solid red');
                $("footer button").prop("disabled", false);
            }

            // Function to handle RPC response
            function handleResponse(result, dialog) {
                var datas = JSON.parse(result);
                
                if (datas.error || datas.recaptch_msg || datas.name_msg || datas.email_msg || datas.company_msg || datas.country_msg || datas.contact_no_msg || datas.description_msg) {
                    displayErrorMessage(datas.error || datas.error_msg, datas.name_msg ? '#solution_page_custom_website_form_partner_name' :
                    datas.error ? '#error_message' :
                        datas.recaptch_msg ? '#error_message':
                            datas.email_msg ? '#solution_page_custom_website_form_email' :
                                datas.company_msg ? '#solution_page_custom_website_form_company' :
                                    datas.country_msg ? '#solution_page_custom_website_form_contact_no':
                                        datas.contact_no_msg ? '#solution_page_custom_website_form_contact_no':

                                '#solution_page_custom_website_form_description');
                    return false;
                }

                // Close current dialog and show "Thank You" message
                dialog.close();
                var dialog = new Dialog(self, {
                    size: "medium",
                    title: _t("Thank You"),
                    $content: $('<div/>', {
                        html: `<p>Your ticket has been created successfully.</p>
                               <p><strong>Ticket No:</strong> ${datas.ticket}</p>`
                    }),
                    buttons: [],
                    renderFooter : false,
                }).open();
                dialog.opened().then(function () {
                    dialog.$modal.addClass("sh_create_ticket_from_solution_design");
                    // dialog.$footer.addClass("d-none");
                });

                return $(self.$target).submit();
            }
        },

        _onClickContactUsSubmitTicket: async function (ev) {
            var self = this;
            ev.preventDefault();
            console.log('log ==>> INLINE FORM countryCode =======',this.countryCode);
            var query_params = this.get_query_params(ev)
            var $button = $("#sh_custom_create_ticket_contact_us_form");
            $button.prop("disabled", true);

            // Get form values
            var partnerName = $('#sh_custom_contact_us_form_partner_name').val();
            var email = $('#sh_custom_contact_us_form_email').val();
            var company = $('#sh_custom_contact_us_form_company').val();
            var country = self.iti.s.iso2.toUpperCase() || self.countryCode.toUpperCase();
            var contact_no = $('#sh_custom_contact_us_form_contact_no').val();
            var description = $('#sh_custom_contact_us_form_description').val();
            var utm_source = query_params.source_name;
            var utm_medium = query_params.medium_name;
            var utm_campaign = query_params.campaign_name;

            // Reset styles and error messages
            resetFormStylesAndMessages();
        
            // Client-side validation
            if (!validateField(partnerName, '#sh_custom_contact_us_form_partner_name', "Please enter your name.") ||
                !validateField(company, '#sh_custom_contact_us_form_company', "Please enter your company name.") ||
                !validateEmail(email) ||
                !validateField(country, '#sh_custom_contact_us_form_contact_no', "Please select your Country.") ||
                !validateContactNo(contact_no) ||
                !validateField(description, '#sh_custom_contact_us_form_description', "Please enter your requirements.")) {
                
            $button.prop("disabled", false);

                return false;
            }
        
            // ReCAPTCHA validation
            const tokenCaptcha = await self._recaptcha.getToken("sh_recaptcha_demo_form");
            console.log('log ==>> tokenCaptcha',tokenCaptcha);
            if (tokenCaptcha.error) {
                self.displayNotification({
                    type: "danger",
                    title: _t("Error"),
                    message: tokenCaptcha.error,
                    sticky: true
                });
            }
        
            // Submit form data via RPC
            this._rpc({
                route: '/softhealer_website_base/website_create_ticket_page',
                params: {
                    'recaptcha_token_response': tokenCaptcha.token,
                    'solution_page_custom_website_form_partner_name': partnerName,
                    'solution_page_custom_website_form_company': company,
                    'solution_page_custom_website_form_email': email,
                    'solution_page_custom_website_form_country': country,
                    'solution_page_custom_website_form_contact_no': contact_no,
                    'solution_page_custom_website_form_description': description,
                    'custom_form_check_url': window.location.href,
                    'custom_form_utm_campaign':utm_campaign,
                    'custom_form_utm_source' : utm_source,
                    'custom_form_utm_medium' : utm_medium,
                },
            }).then(function (result) {
                handleResponse(result);
            });
        
        
            function resetFormStylesAndMessages() {
                $('#error_message').hide();
                $('#sh_custom_contact_us_form_partner_name, #sh_custom_contact_us_form_email, #sh_custom_contact_us_form_company, #sh_custom_contact_us_form_contact_no, #sh_custom_contact_us_form_description').removeAttr('style');
            }
        
            function validateField(value, fieldId, errorMessage) {
                if (!value || value.trim() === '') {
                    displayErrorMessage(errorMessage, fieldId);
                    return false;
                }
                return true;
            }
        
            function validateEmail(email) {
                if (!email || email.trim() === '') {
                    displayErrorMessage("Please enter your email address.", '#sh_custom_contact_us_form_email');
                    return false;
                } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
                    displayErrorMessage("Please enter a valid email address.", '#sh_custom_contact_us_form_email');
                    return false;
                }
                return true;
            }
        
            function validateContactNo(contact_no) {
                if (!contact_no || contact_no.trim() === '') {
                    displayErrorMessage("Please enter your contact no.", '#sh_custom_contact_us_form_contact_no');
                    return false;
                } else if (! self.iti.isValidNumber()) {
                    const errorCode = self.iti.getValidationError();
                    const msg = "Please check contact number : " + self.errorMap[errorCode] || "Invalid number";

                    // displayErrorMessage("Please enter a valid contact no.", '#sh_custom_contact_error_div');
                    displayErrorMessage(msg, '#sh_custom_contact_us_form_contact_no');

                    return false;
                }
                return true;
            }
        
            function displayErrorMessage(message, fieldId) {
                $('#error_message_contact_us').show().html(message).css('margin-top', '10px');
                $(fieldId).css('border', '1px solid red');
            }
        
            function handleResponse(result) {
                var datas = JSON.parse(result);
                if (datas.error || datas.recaptch_msg || datas.name_msg || datas.email_msg || datas.company_msg || datas.country_msg || datas.contact_no_msg || datas.description_msg) {
                    displayErrorMessage(datas.error || datas.error_msg, datas.name_msg ? '#sh_custom_contact_us_form_partner_name' :    
                    datas.error ? '#error_message' :
                        datas.recaptch_msg  ? '#error_message' :
                            datas.email_msg ? '#sh_custom_contact_us_form_email' :
                                datas.company_msg ? '#sh_custom_contact_us_form_company' :
                                    datas.country_msg ? '#sh_custom_contact_us_form_contact_no' :
                                        datas.contact_no_msg ? '#sh_custom_contact_us_form_contact_no' :
                                    '#sh_custom_contact_us_form_description');
                $button.prop("disabled", false);
                    
                    return false;
                }
                var thankYouDialog = new Dialog(self, {
                    size: "medium",
                    title: _t("Thank You"),
                    $content: $('<div/>', {
                        html: `<p>Your ticket has been created successfully.</p><p><strong>Ticket No:</strong> ${datas.ticket}</p>`
                    }),
                    buttons: [],
                    renderFooter : false,
                }).open();
        
                thankYouDialog.opened().then(function () {
                    thankYouDialog.$modal.addClass("sh_create_ticket_from_solution_design");
                    // thankYouDialog.$footer.addClass("d-none");
                    clearFormValues();
                });
        
                function clearFormValues() {
                    $('#sh_custom_contact_us_form_partner_name, #sh_custom_contact_us_form_email, #sh_custom_contact_us_form_company, #sh_custom_contact_us_form_contact_no, #sh_custom_contact_us_form_description').val('');
                    $('#error_message_contact_us').hide();
                    $('#solution_page_custom_website_form_partner_name, #solution_page_custom_website_form_email, #solution_page_custom_website_form_company, #sh_custom_contact_us_form_contact_no, #solution_page_custom_website_form_description').removeAttr('style');
                    $button.prop("disabled", false);
                }
                return $(self.$target).submit();
            }
        },


    })
});
