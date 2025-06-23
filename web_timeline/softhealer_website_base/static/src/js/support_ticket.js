odoo.define('softhealer_website_base.helpdesk_ticket_create_page_so_portal', function (require) {
    'use strict';

    const { ReCaptcha } = require('google_recaptcha.ReCaptchaV3');
    const { _t, qweb } = require('web.core');
    var publicWidget = require('web.public.widget');
    publicWidget.registry.SOHelpdeskTicketPage = publicWidget.Widget.extend({
        selector: '.tick_create',
        events: {
            'click #help_create':'_onClickHelp',
            'click .btn_add_ticket': '_onClickSubmitTicket',
            'change #edition': '_onchangeEdition',
            'change #files': '_onChangeFile',
        },
        /**
         * @override
         */
        start: function () {  

            this._super(...arguments);
            // this._open_country_selection()
            const template = document.createElement('template');
            template.innerHTML = qweb.render("google_recaptcha.recaptcha_legal_terms");
            this.$target.find('#sh_portal_ticket_reCaptcha_legal_terms').append(template.content.firstElementChild);

            $('#host').empty();
            return this._super.apply(this, arguments);
        },


        async willStart() {
           return this._recaptcha.loadLibs();
        },

        init() {
            this._super(...arguments);
            this._recaptcha = new ReCaptcha();
        },
        
        _onClickHelp: function (ev) {            
            $('#Ticketmodal').modal('show');
            $('#pr_id').val($(ev.currentTarget).data('pr-id'));
            $('#ref').val($(ev.currentTarget).data('ref'));
            $('#categ_id').val($(ev.currentTarget).data('categ-id'));
            $('#current').val($(ev.currentTarget).data('current'));
            $('#error_ticket_message').addClass('o_hidden');
            $('#success_ticket_message').addClass('o_hidden');
            $('#email_subject').val('');
            $('#tick_type').val('tick_type');
            $('#edition').val('tick_edition');
            $('#host').val('host_on');
            $('#description').val('');
        },
        _onchangeEdition: function (ev) {
            let editionId = $(ev.target).val();

            // Empty the 'hosted' element
            $('#host').empty();

            // Make an RPC call with the edition ID as a parameter
            this._rpc({
                route: '/odoo-hosted-on-portal',
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
                    $('#host').append(`<option value='host_on'>Select Odoo Hosted On</option>`);
                    $('#host').append(optionsStr);

                    // Remove any options from the 'hosted' element that have an empty value or text
                    $('#host option')
                        .filter(function () {
                            return !this.value || $.trim(this.value).length == 0 || $.trim(this.text).length == 0;
                        }).remove();
                }
                // If there are no hosted IDs in the result
                else {
                    // Empty the 'hosted' element
                    $('#host').empty();
                }
            });
        },
        getFileAsText:function (file) {
            return new Promise((resolve, reject) => {
                if (!file) {
                    reject();
                } else {
                    const reader = new FileReader();
                    reader.addEventListener('load', function () {
                        resolve(reader.result);
                    });
                    reader.addEventListener('abort', reject);
                    reader.addEventListener('error', reject);
                    reader.readAsDataURL(file);
                }
            });
        },
        _onChangeFile: function (ev) {
            var all_attachment_size = 0.0
            for (let index = 0; index < ev.currentTarget.files.length; index++) {
                const element = ev.currentTarget.files[index];
                all_attachment_size = all_attachment_size + element.size
            }
            var file_size_limit = $('#files').attr('data-attachment-size')
            if (all_attachment_size / 1000 > parseInt(file_size_limit)) {
                alert("The maximum file size you may attach is " + file_size_limit + "KB")
                $('#files').val('')
                return false
            }
        },
        _onClickSubmitTicket: async function (ev) {
            var self = this;
            ev.preventDefault();
            $(".sh_so_portal_loader").removeClass('o_hidden');
            let formData = [];
            var files = $('#files')[0].files;
            for (var i = 0; i < files.length; i++) {
                var bin_str = await this.getFileAsText(files[i]);
                formData.push({'filename':files[i].name,'type':files[i].type,'data':bin_str.split(',')[1]})
            }

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



            this._rpc({
                route: '/support_ticket',
                params: {
                    'recaptcha_token_response': tokenCaptcha.token,
                    'subject': $('#email_subject').val(),
                    'ticket_type': $('#tick_type').val(),
                    'edition': $('#edition').val(),
                    'host': $('#host').val(),
                    'description': $('#description').val(),
                    'product':$('#pr_id').val(),
                    'ref':$('#ref').val(),
                    'category':$("#categ_id").val(),
                    'order_id':$('#current').val(),
                    'formData':formData,
                    'custom_form_check_url': window.location.href
                },
            }).then(function (result) {
                var datas = JSON.parse(result);
                if (datas.success == false){
                    $(".sh_so_portal_loader").addClass('o_hidden');
                    $('#error_ticket_message').html(datas.error_message);
                    $('#error_ticket_message').removeClass('o_hidden');
                    $('#success_ticket_message').addClass('o_hidden');
                }
                else if(datas.success == true){
                    $(".sh_so_portal_loader").addClass('o_hidden');
                    $('#success_ticket_message').html(datas.success_message);
                    $('#success_ticket_message').removeClass('o_hidden');
                    $('#error_ticket_message').addClass('o_hidden');
                    $('#email_subject').val('');
                    $('#tick_type').val('tick_type');
                    $('#edition').val('tick_edition');
                    $('#host').val('host_on');
                    $('#description').val('');
                    $('#files').val('');
                }
            });
        }
    })
})