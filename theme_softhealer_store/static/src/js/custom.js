odoo.define('theme_softhealer_store.website_sale_detail_page', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var Dialog = require('web.Dialog');
    var core = require('web.core');
    var _t = core._t;
    var ajax = require("web.ajax");
    const { qweb } = require('web.core');
    require('website_sale.website_sale');
    var wSaleUtils = require('website_sale.utils');
    const { loadJS, loadCSS } = require('@web/core/assets');
    const { ReCaptcha } = require('google_recaptcha.ReCaptchaV3');

    
    publicWidget.registry.WebsiteSale.include({

        events: _.extend({}, publicWidget.registry.WebsiteSale.prototype.events, {
            'click .cls_open_pop_form':'_onClickOpenSupportDialoagBox',
            'click .js_cls_custom_shop_filter_dropdown a.dropdown-item':'_onChangeFilterDropdown',
        }),

        /**
         * @constructor
         */
        init() {
            this._super(...arguments);
            this._recaptcha = new ReCaptcha();
        },

        async willStart() {
            // Load Libs
            try {
                this.countryCode = await this.getCountryCode();
                // this.countryCode = '' || 'US';
                
                // this.countryCode = '';

                await loadJS('/theme_softhealer_store/static/src/lib/intl-tel-input/intl-tel-input.js');
                await loadCSS('/theme_softhealer_store/static/src/lib/intl-tel-input/intl-tel-input.css');
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
                            return data.countryCode || data.country_code; // Return the country code if found
                        }
                    }
                } catch (error) {
                    // If there is an error (e.g., network issue), it will proceed to the next API
                }
            }

            return 'US';
        },

        /**
         * The method override for checking whether user remove depends product(module) or not.
         * 
         * @override
         * @param {Event} ev 
         */
        _onChangeCartQuantity:function(ev){
            var self = this;
            var $input = $(ev.currentTarget);
            if ($input.data('update_change')) {
                return;
            }
            var value = parseInt($input.val() || 0, 10);
            if (isNaN(value)) {
                value = 1;
            }
            var $dom = $input.closest('tr');
            // var default_price = parseFloat($dom.find('.text-danger > span.oe_currency_value').text());
            var $dom_optional = $dom.nextUntil(':not(.optional_product.info)');
            var line_id = parseInt($input.data('line-id'), 10);
            var productIDs = [parseInt($input.data('product-id'), 10)];

            if (value === 0){
                this._rpc({
                    route:"/theme_softhealer_store/check_is_depends_product_deleting",params:{line_id:line_id,product_id:parseInt($input.data('product-id'), 10)}}).then(function (result) {
                    if(result && typeof result === "object"){
                        if(result.show_waring){
    
                            var dialog = new Dialog(self, {
                                title: _t("Deleting product can be risky!"),
                                $content:_t(result.message),
                                buttons: [{text: _t("Confirm"),
                                            classes: 'btn-primary',
                                            click: function() {
                                                self._changeCartQuantity($input, value, $dom_optional, line_id, productIDs);
                                            },
                                            close: true,
                                        },
                                        {text: _t("Discard"),
                                        close: true,
                                        click: function(){
                                            if (result.line_qty)
                                            {
                                                    $input.val(result.line_qty);
                                                }
                                            },
                                        },
                                    ]
                                });
                            dialog.open();
                        }else{
                            self._changeCartQuantity($input, value, $dom_optional, line_id, productIDs);
                        }
                    }
                })
            }else{
                this._changeCartQuantity($input, value, $dom_optional, line_id, productIDs);
            }
        },

        /**
         * @private
         */
        _addToCartInPage(params) {
            var self = this
            params.force_create = true;
            return this._rpc({
                route: "/shop/cart/update_json",
                params: params,
            }).then(async data => {
                self.sh_blog_post_not_exists = true
                self.war_text = ''
                if (data.sh_blog_post_not_exists){
                    var ContactUsBtn = $("#btn_contact_us_product_model_id");
                    if (ContactUsBtn){
                        self.war_text = "Note : Apologies for any inconvenience. This app is currently in the development phase for "+data.product_varsion+ ". If you need it for an earlier version, please don't hesitate to contact us."
                        ContactUsBtn.click()
                    }
                }
                if (!data.sh_blog_post_not_exists){
                    sessionStorage.setItem('website_sale_cart_quantity', data.cart_quantity);
                    if (data.cart_quantity && (data.cart_quantity !== parseInt($(".my_cart_quantity").text()))) {
                        // No animation if the product's page images are hidden
                        if ($('div[data-image_width]').data('image_width') !== 'none') {
                            await wSaleUtils.animateClone($('header .o_wsale_my_cart').first(), this.$itemImgContainer, 25, 40);
                        }
                        wSaleUtils.updateCartNavBar(data);
                    }
                }
            });
        },

        toBase64: async function(sh_file){
            return new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.readAsDataURL(sh_file);
                reader.onload = () => resolve(reader.result);
                reader.onerror = error => reject(sh_file);
            });
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

        _onChangeFilterDropdown:function (ev){
            ev.preventDefault();
            var filter = $(ev.currentTarget).attr('value')
            var name = $(ev.currentTarget).text()
            if (filter){
                $(ev.currentTarget).parents('.js_attributes').find('.css_attribute_select option[value="'+filter+'"]').prop('selected', true)
            }
            else{
                $(ev.currentTarget).parents('.js_attributes').find('.css_attribute_select option[value=""]').prop('selected', true)
            }
            $(ev.currentTarget).parents('.js_attributes').find('.css_attribute_select').trigger('change');
        },

        _onClickOpenSupportDialoagBox: async function(ev){
            var self = this;
            var query_params = this.get_query_params(ev)
            const errorMap = ["Invalid number", "Invalid country code", "Too short", "Too long", "Invalid number"];
            
            var btn_origin = $(ev.currentTarget).data('button')
            var product_id = $('input[name="product_id"]').val()
            this.box_title = '' 
            
            if (btn_origin == 'technical_support'){
                this.box_title = 'Technical Support'
            }
            else if (btn_origin == 'demo_support'){
                this.box_title = 'Demo Support'
            }
            else if (btn_origin == 'new_customization'){
                this.box_title = 'New Customization'
            }

            else if (btn_origin == 'sh_contact_us'){
                this.box_title = 'Contact Us'
            }

            var user_public = $(ev.currentTarget).data('user_public') || ''
            var sh_editions = $(ev.currentTarget).data('sh_edition') || ''
            var user_name = $(ev.currentTarget).data('user_name') || ''
            var product_name = $(ev.currentTarget).data('product_name') || ''
            // var version = $('input.js_variant_change:checked').attr('data-value_name');
            var version = $('select.js_variant_change option:selected').attr('data-value_name');
            var mobile = $(ev.currentTarget).data('mobile') || ''
            var email = $(ev.currentTarget).data('email') || ''
            var partner_id = $(ev.currentTarget).data('user_partner_id') || ''
            self.sh_edition_info_data = ''

            await this._rpc({
                route: "/get_sh_edition_details",
                params: {sh_editions:sh_editions},
            }).then(function (data) {
                if (data['sh_edition_info_details']){
                    self.sh_edition_info_data = data['sh_edition_info_details'];
                }
                else{
                    self.sh_edition_info_data = ''
                }
            });
            var dialog = new Dialog(this, {
                title: this.box_title,
                size:'medium',
                $content: qweb.render('theme_softhealer_store.shEcommerceSupportTemplate', {
                    btn_origin: btn_origin,
                    product_name:product_name,
                    user_name:user_name,
                    version:version,
                    mobile:mobile,
                    email:email,
                    user_public:user_public,
                    sh_edition_info:self.sh_edition_info_data,
                    sh_blog_post_not_exists:self.sh_blog_post_not_exists,
                    war_text:self.war_text

                }),
                buttons: [{
                    text: _t("Send"),
                    classes: "btn-primary",
                    click: async function () {

                        // Fields Mandatory
                        var attachment_size = $(ev.currentTarget).data('attachment_size') || 0
                        var $warning_html = $('.sh_support_button_custom_dialoag_wrapper .sh_support_wrapper_warning')
                        $warning_html.html('')
                        var warning = _t('Please Filled All Required Fields.')
                        var sh_edition = $('.sh_support_button_custom_dialoag_wrapper select[name="sh_edition_id"]').val();
                        var text_area_msg = $('.sh_support_button_custom_dialoag_wrapper textarea[name="input_message_name"]').val();
                        var user_name = $('.sh_support_button_custom_dialoag_wrapper input[name="input_firstname"]').val();
                        var email =  $('.sh_support_button_custom_dialoag_wrapper input[name="input_email"]').val();
                        var company_name =  $('.sh_support_button_custom_dialoag_wrapper input[name="input_company"]').val();
                        var contact =  $('.sh_support_button_custom_dialoag_wrapper input[name="input_contactno"]').val();
                        var version =  $('.sh_support_button_custom_dialoag_wrapper input[name="input_version"]').val();
                        var email_regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z]{2,4})+$/;
                        var email_warning = _t('Please add valid email address.')
                        var product_id = $('.js_main_product').find('input[name="product_id"]').val()
                        var migration_notify_me = $('.sh_support_button_custom_dialoag_wrapper input[name="input_migration_notify_me"]:checked').val()
                        var product_url = document.location.href
                        var country = self.iti_pop_up.s.iso2.toUpperCase() || self.countryCode.toUpperCase();
                        var check_contact = true

                        $('textarea[name="input_message_name"]').css("border", "1px solid #CED4DA");
                        $('select[name="sh_edition_id"]').css("border", "1px solid #CED4DA");
                        $('.sh_support_button_custom_dialoag_wrapper input[name="input_firstname"]').css("border", "1px #CED4DA solid");
                        $('.sh_support_button_custom_dialoag_wrapper input[name="input_email"]').css("border", "1px #CED4DA solid");

                        if(!user_name){
                            $('.sh_support_button_custom_dialoag_wrapper input[name="input_firstname"]').css("border", "1px red solid");
                            $warning_html.html('<p class="alert alert-warning">' + warning + '</p>')
                        }

                        if(email && !email_regex.test(email)){
                            $('.sh_support_button_custom_dialoag_wrapper input[name="input_email"]').css("border", "1px red solid");
                            $warning_html.html('<p class="alert alert-warning">' + email_warning + '</p>')
                        }
                        if(!email){
                            $('.sh_support_button_custom_dialoag_wrapper input[name="input_email"]').css("border", "1px red solid");
                            $warning_html.html('<p class="alert alert-warning">' + warning + '</p>')
                        }

                        if (!contact || contact.trim() === '') {
                            $('.sh_support_button_custom_dialoag_wrapper input[name="input_contactno"]').css("border", "1px red solid");
                            $warning_html.html('<p class="alert alert-warning">' + warning + '</p>')
                        } else if (! self.iti_pop_up.isValidNumber()) {
                            const errorCode = self.iti_pop_up.getValidationError();
                            const msg = "Please check contact number : " + errorMap[errorCode] || "Invalid number";
                            $('.sh_support_button_custom_dialoag_wrapper input[name="input_contactno"]').css("border", "1px red solid");
                            $warning_html.html('<p class="alert alert-warning">' + msg + '</p>')
                            check_contact = false
                        }

                        if (!text_area_msg){
                            $('textarea[name="input_message_name"]').css("border", "1px red solid");
                            $warning_html.html('<p class="alert alert-warning">' + warning + '</p>')
                        }

                        if (!sh_edition){
                            $('.sh_support_button_custom_dialoag_wrapper select[name="sh_edition_id"]').css("border", "1px red solid");
                            $warning_html.html('<p class="alert alert-warning">' + warning + '</p>')
                        }
                        
                        
                        

                        if($('.file_box').length != 0){
                            $('input#ticket_attachment').css("border", "1px solid #CED4DA");

                            if( document.getElementById("ticket_attachment").files.length == 0 ){
                                $('input#ticket_attachment').css("border", "1px red solid");
                                $warning_html.html('<p class="alert alert-warning">' + warning + '</p>')
                            }

                            if( document.getElementById("ticket_attachment").files.length != 0 ){
                                var all_attachment_size = 0.0
                                for (let index = 0; index < document.getElementById("ticket_attachment").files.length; index++) {
                                    all_attachment_size = all_attachment_size + document.getElementById("ticket_attachment").files[index].size                    
                                }
                                if (all_attachment_size / 1000 > parseInt(attachment_size)) {
                                    $warning_html.html("<p class='alert alert-warning'> You can only attach file less than "+ attachment_size + " KB </p>")
                                    $('#ticket_attachment').val('')
                                    return false
                                }
                                else{
                                    var attachment_base64_list = []
                                    for (let index = 0; index < document.getElementById("ticket_attachment").files.length; index++) {
                                        const sh_file = document.getElementById("ticket_attachment").files[index];
                                        attachment_base64_list.push(await self.toBase64(sh_file))
                                    }
                                }
                            }
                        }

                        // check files input available and filled 
                        this.files = false 
                        if ($('.file_box').length != 0 && document.getElementById("ticket_attachment").files.length == 0){
                            this.files = true
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

                        console.log("--------------> 297 tokenCaptcha.token",tokenCaptcha.token);

                        // DIALOAG AND WARNING CLOSER AND STORE RECORD
                        if(user_name && text_area_msg && !this.files && email && email_regex.test(email) && sh_edition && contact && check_contact && tokenCaptcha){

                            $warning_html.html('')
                            await ajax.jsonRpc('/helpdesk/helpdesk_create_ticket', 'call',{
                                'recaptcha_token_response': tokenCaptcha.token,
                                'btn_origin': btn_origin,
                                'company_name' : company_name,
                                'contact_no': contact,
                                'user_email': email,
                                'message': text_area_msg ,
                                'name':user_name,
                                'version':version,
                                'product_id':product_id,
                                'partner_id':partner_id,
                                'attachment_base64_list':attachment_base64_list || [],
                                'sh_edition':sh_edition,
                                'migration_notify_me':migration_notify_me,
                                'product_url':product_url,
                                'theme_softhealer_store_website_sale_ticket_url' : window.location.href,
                                'utm_source' : query_params.source_name,
                                'utm_medium' : query_params.medium_name,
                                'utm_campaign' : query_params.campaign_name,
                                'country' : country
                            }).then(function (result) {
                                if (result.recaptcha_msg) {
                                    $warning_html.html('<p class="alert alert-danger">' + result.recaptcha_msg + '</p>')
                                }
                                if (result.email_validation == 'email_not_valid') {
                                    $('.sh_support_button_custom_dialoag_wrapper input[name="input_email"]').css("border", "1px red solid");
                                    $warning_html.html('<p class="alert alert-warning">' + email_warning + '</p>')
                                }
                                if (result.ticket_success == 'ticket_success' && result.ticket_name) {
                                    var success_msg = _t('Your Ticket Successfully Submitted , Please note Ticket number is')
                                    $warning_html.html('<p class="alert alert-success"> ' + success_msg + ' ' + result.ticket_name + '</p>')
                                    
                                    dialog.$modal.find('.modal-body ').html('<p class="alert alert-success"> ' + success_msg + ' ' + result.ticket_name + '</p>')
                                    dialog.$footer.empty()
                                    dialog.$footer.removeClass('model-footer')
                                }
                            })
                                
                        }
                    },
                }],
            });

            dialog.open();
            dialog.opened().then(function () {
                self.sh_blog_post_not_exists = false
                dialog.$footer.removeClass('justify-content-sm-start');
                dialog.$footer.removeClass('justify-content-around');

                dialog.$modal.addClass("sh_create_ticket_from_solution_design");

                const countryInput = dialog.$el.find("#input_contactno");
                if(countryInput){
                   self.iti_pop_up = window.intlTelInput(countryInput[0], {
                        initialCountry: self.countryCode.toLowerCase(),
                        loadUtils: () => import("https://cdn.jsdelivr.net/npm/intl-tel-input@25.3.1/build/js/utils.js"),
                    });
                }
            });
            
            
        },

        

        _onChangeCombination: function (ev, $parent, combination) {
            
            this._super.apply(this, arguments);

            /* Product Blog Display*/
            var body = "<div class='alert alert-info' role='alert'> Nothing to display</div>"
            if (combination.product_variant_desc) {
                $('#sh_custom_tab_blog_details').html(combination.product_variant_desc)
            }
            else {
                $('#sh_custom_tab_blog_details').html(body)
            }
            /* Product Blog Display*/
            
            /* Change Log*/
            var body = "<div class='alert alert-info' role='alert'> Nothing to display</div>"
            if (combination.change_log_html) {
                $('#sh_custom_tab_change_log_details').html(combination.change_log_html)
            }
            else {
                $('#sh_custom_tab_change_log_details').html(body)
            }
            /* Change Log*/


            /* Module Information*/
            if (combination.module_info_html) {
                $('#sh_custom_tab_module_information').html(combination.module_info_html)
            }
            /* Module Information*/
        }
    });

});