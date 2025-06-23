odoo.define('sh_helpdesk.CreateTicketPopup', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var ajax = require('web.ajax');

    publicWidget.registry.CreateTicketPopup = publicWidget.Widget.extend({
        selector: '#createticketModal',

        events: {
            'change #partner': '_onChangePartner',
            'change #portal_category': '_onPortalCategory',
            'change #portal_team': '_onPortalTeam',
        },

        /**
        * @override
        */
        start: async function () {
            const res = await this._super(...arguments);

            /**
                INITIALIZE CREATE TICKET POPUP SHOW ON CREATE BUTTON 
            */
            $('body').find('#new_request').on("click", this._onChangeOpenPopup.bind(self));

            ajax.jsonRpc('/portal-subcategory-data', 'call', { category_id: $("#portal_category").val() })
                .then(function (result) {
                    var datas = JSON.parse(result);
                    $("#portal_subcategory > option").remove();
                    $("#portal_subcategory").append('<option value="' + "sub_category" + '">' + "Select Sub Category" + "</option>");
                    _.each(datas.sub_categories, function (data) {
                        $("#portal_subcategory").append('<option value="' + data.id + '">' + data.name + "</option>");
                    });
                })

            ajax.jsonRpc('/portal-partner-data', 'call', {})
                .then(function (result) {
                    var datas = JSON.parse(result);
                    $("#partner_ids > option").remove();
                    _.each(datas.partners, function (data) {
                        $("#partner_ids").append('<option data-id="' + data.id + '" value="' + data.name + '">');
                    });
                })


            ajax.jsonRpc('/portal-user-data', 'call', { team_id: $("#portal_team").val() })
                .then(function (result) {
                    var datas = JSON.parse(result);
                    $("#portal_assign_user > option").remove();
                    $("#portal_assign_user").append('<option value="' + "user" + '">' + "Select Assign User" + "</option>");
                    $("#portal_assign_multi_user").multiselect('destroy');
                    $("#portal_assign_multi_user > option").remove();
                    $("#portal_assign_multi_user").append('<option value="' + "users" + '">' + "Select Multi Users" + "</option>");
                    _.each(datas.users, function (data) {
                        $("#portal_assign_user").append('<option value="' + data.id + '">' + data.name + "</option>");
                        $("#portal_assign_multi_user").append('<option value="' + data.id + '">' + data.name + "</option>");
                    });
                    $("#portal_assign_multi_user").multiselect();
                })

            return res
        },




        _onChangeOpenPopup: function (ev) {
            $("#createticketModal").modal("show");
        },


        _onChangePartner: function () {
            var option = $("#partner_ids").find("[value='" + $("#partner").val() + "']");
            var partner = option.data("id");
            $("#partner_id").val("");
            $("#partner_id").val(partner);


            if ($("#partner_id").val() != "") {
                ajax.jsonRpc('/selected-partner-data', 'call', { partner_id: $("#partner_id").val() })
                    .then(function (result) {
                        var datas = JSON.parse(result);
                        var datas = JSON.parse(result);
                        $("#portal_contact_name").val(datas.name);
                        $("#portal_email").val(datas.email);
                    })
            } else {
                $("#portal_contact_name").val("");
                $("#portal_email").val("");
            }
        },


        _onPortalCategory: function () {
            ajax.jsonRpc('/portal-subcategory-data', 'call', { category_id: $("#portal_category").val() })
                .then(function (result) {
                    var datas = JSON.parse(result);
                    $("#portal_subcategory > option").remove();
                    $("#portal_subcategory").append('<option value="' + "sub_category" + '">' + "Select Sub Category" + "</option>");
                    _.each(datas.sub_categories, function (data) {
                        $("#portal_subcategory").append('<option value="' + data.id + '">' + data.name + "</option>");
                    });
                })
        },


        _onPortalTeam: function () {
            ajax.jsonRpc('/portal-user-data', 'call', { team_id: $("#portal_team").val() })
                .then(function (result) {
                    var datas = JSON.parse(result);
                    $("#portal_assign_user > option").remove();
                    $("#portal_assign_multi_user").multiselect('destroy');
                    $("#portal_assign_multi_user > option").remove();
                    $("#portal_assign_user").append('<option value="' + "user" + '">' + "Select Assign User" + "</option>");
                    $("#portal_assign_multi_user").append('<option value="' + "users" + '">' + "Select Multi Users" + "</option>");
                    _.each(datas.users, function (data) {
                        $("#portal_assign_user").append('<option value="' + data.id + '">' + data.name + "</option>");
                        $("#portal_assign_multi_user").append('<option value="' + data.id + '">' + data.name + "</option>");
                    });
                    $("#portal_assign_multi_user").multiselect();
                })
        },
    })
})

// ------------------------------------------------------------------------------------------------------------------------------------------------

// $(document).ready(function (e) {
//     $(function () {
//         $('#portal_assign_multi_user').multiselect();
//     });
//     $("#new_request").click(function () {
//         $("#createticketModal").modal("show");
//     });
//     console.log("\n\n\n ----------- portal_category ------------>", $("#portal_category").val());
//     $.ajax({
//         url: "/portal-subcategory-data",
//         data: { category_id: $("#portal_category").val() },
//         type: "post",
//         cache: false,
//         success: function (result) {
//             var datas = JSON.parse(result);
//             $("#portal_subcategory > option").remove();
//             $("#portal_subcategory").append('<option value="' + "sub_category" + '">' + "Select Sub Category" + "</option>");
//             _.each(datas.sub_categories, function (data) {
//                 $("#portal_subcategory").append('<option value="' + data.id + '">' + data.name + "</option>");
//             });
//         },
//     });
//     $.ajax({
//         url: "/portal-partner-data",
//         data: {},
//         type: "post",
//         async: false,
//         cache: false,
//         success: function (result) {
//             var datas = JSON.parse(result);
//             $("#partner_ids > option").remove();
//             _.each(datas.partners, function (data) {
//                 $("#partner_ids").append('<option data-id="' + data.id + '" value="' + data.name + '">');
//             });
//         },
//     });

// $(document).on("change", "#partner", function (e) {
//     var option = $("#partner_ids").find("[value='" + $("#partner").val() + "']");
//     var partner = option.data("id");
//     $("#partner_id").val("");
//     $("#partner_id").val(partner);
//     if ($("#partner_id").val() != "") {
//         $.ajax({
//             url: "/selected-partner-data",
//             data: { partner_id: $("#partner_id").val() },
//             type: "post",
//             cache: false,
//             success: function (result) {
//                 var datas = JSON.parse(result);
//                 $("#portal_contact_name").val(datas.name);
//                 $("#portal_email").val(datas.email);
//             },
//         });
//     } else {
//         $("#portal_contact_name").val("");
//         $("#portal_email").val("");
//     }
// });

// $.ajax({
//     url: "/portal-user-data",
//     data: { team_id: $("#portal_team").val() },
//     type: "post",
//     cache: false,
//     success: function (result) {
//         var datas = JSON.parse(result);
//         $("#portal_assign_user > option").remove();
//         $("#portal_assign_user").append('<option value="' + "user" + '">' + "Select Assign User" + "</option>");
//         $("#portal_assign_multi_user").multiselect('destroy');
//         $("#portal_assign_multi_user > option").remove();
//         $("#portal_assign_multi_user").append('<option value="' + "users" + '">' + "Select Multi Users" + "</option>");
//         _.each(datas.users, function (data) {
//             $("#portal_assign_user").append('<option value="' + data.id + '">' + data.name + "</option>");
//             $("#portal_assign_multi_user").append('<option value="' + data.id + '">' + data.name + "</option>");
//         });
//         $("#portal_assign_multi_user").multiselect();
//     },
// });

// $(document).on("change", "#portal_category", function (e) {
//     $.ajax({
//         url: "/portal-subcategory-data",
//         data: { category_id: $("#portal_category").val() },
//         type: "post",
//         cache: false,
//         success: function (result) {
//             var datas = JSON.parse(result);
//             $("#portal_subcategory > option").remove();
//             $("#portal_subcategory").append('<option value="' + "sub_category" + '">' + "Select Sub Category" + "</option>");
//             _.each(datas.sub_categories, function (data) {
//                 $("#portal_subcategory").append('<option value="' + data.id + '">' + data.name + "</option>");
//             });
//         },
//     });
// });

// $(document).on("change", "#portal_team", function (e) {
//     $.ajax({
//         url: "/portal-user-data",
//         data: { team_id: $("#portal_team").val() },
//         type: "post",
//         cache: false,
//         success: function (result) {
//             var datas = JSON.parse(result);
//             $("#portal_assign_user > option").remove();
//             $("#portal_assign_multi_user").multiselect('destroy');
//             $("#portal_assign_multi_user > option").remove();
//             $("#portal_assign_user").append('<option value="' + "user" + '">' + "Select Assign User" + "</option>");
//             $("#portal_assign_multi_user").append('<option value="' + "users" + '">' + "Select Multi Users" + "</option>");
//             _.each(datas.users, function (data) {
//                 $("#portal_assign_user").append('<option value="' + data.id + '">' + data.name + "</option>");
//                 $("#portal_assign_multi_user").append('<option value="' + data.id + '">' + data.name + "</option>");
//             });
//             $("#portal_assign_multi_user").multiselect();
//         },
//     });
// });

// ------------------------------------------------------------------------------------------------------------------------------------------------

// });
