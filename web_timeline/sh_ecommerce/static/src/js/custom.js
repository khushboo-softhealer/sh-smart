odoo.define('sh_ecommerce.website_sale_detail_page', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var Dialog = require('web.Dialog');
    var core = require('web.core');
    var _t = core._t;
    var ajax = require("web.ajax");
    const { qweb } = require('web.core');
    require('website_sale.website_sale');


    publicWidget.registry.WebsiteSale.include({

        events: _.extend({}, publicWidget.registry.WebsiteSale.prototype.events, {
            'click .cls_open_pop_form':'_onClickOpenSupportDialoagBox',
        }),

        toBase64: async function(sh_file){
            return new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.readAsDataURL(sh_file);
                reader.onload = () => resolve(reader.result);
                reader.onerror = error => reject(sh_file);
            });
        },

        _onClickOpenSupportDialoagBox: async function(ev){
            var self = this;
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

            var user_public = $(ev.currentTarget).data('user_public') || ''
            var user_name = $(ev.currentTarget).data('user_name') || ''
            var product_name = $(ev.currentTarget).data('product_name') || ''
            var version = $('input.js_variant_change:checked').attr('data-value_name');
            var mobile = $(ev.currentTarget).data('mobile') || ''
            var email = $(ev.currentTarget).data('email') || ''
            var partner_id = $(ev.currentTarget).data('user_partner_id') || ''
            
            var dialog = new Dialog(this, {
                title: this.box_title,
                size:'medium',
                $content: qweb.render('sh_ecommerce.shEcommerceSupportTemplate', {
                    btn_origin: btn_origin,
                    product_name:product_name,
                    user_name:user_name,
                    version:version,
                    mobile:mobile,
                    email:email,
                    user_public:user_public,
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
                        var text_area_msg = $('.sh_support_button_custom_dialoag_wrapper textarea[name="input_message_name"]').val();
                        var user_name = $('.sh_support_button_custom_dialoag_wrapper input[name="input_firstname"]').val();
                        var email =  $('.sh_support_button_custom_dialoag_wrapper input[name="input_email"]').val();
                        var contact =  $('.sh_support_button_custom_dialoag_wrapper input[name="input_contactno"]').val();
                        var version =  $('.sh_support_button_custom_dialoag_wrapper input[name="input_version"]').val();
                        var email_regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z]{2,4})+$/;
                        var email_warning = _t('Please add valid email address.')
                        var product_id = $('.js_main_product').find('input[name="product_id"]').val()

                        $('textarea[name="input_message_name"]').css("border", "1px solid #CED4DA");
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

                        if (!text_area_msg){
                            $('textarea[name="input_message_name"]').css("border", "1px red solid");
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

                        // DIALOAG AND WARNING CLOSER AND STORE RECORD
                        if(user_name && text_area_msg && !this.files && email && email_regex.test(email)){

                            $warning_html.html('')
                            await ajax.jsonRpc('/helpdesk/helpdesk_create_ticket', 'call',{
                                'btn_origin': btn_origin,
                                'contact_no': contact,
                                'user_email': email,
                                'message': text_area_msg ,
                                'name':user_name,
                                'version':version,
                                'product_id':product_id,
                                'partner_id':partner_id,
                                'attachment_base64_list':attachment_base64_list || [],
                                'sh_ecommerce_website_sale_ticket_url' : window.location.href,
                            }).then(function (result) {
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
                dialog.$footer.removeClass('justify-content-sm-start');
                dialog.$footer.removeClass('justify-content-around');
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