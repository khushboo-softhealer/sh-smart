/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, onWillStart, onMounted, useState } from "@odoo/owl";
import ajax from "web.ajax";
import { useService } from "@web/core/utils/hooks";

export class BrDashboard extends Component {
  setup() {
    super.setup();
    onWillStart(async () => {
      let result = await ajax.jsonRpc("/get/br_engage_dashboard/data", "call");
      this.check_in_details = result['check_in_all_details']
      this.meeting_all_details = result['meeting_all_details']
      this.details_of_1on1_records = result['1on1s_all_details']
      this.login_user_name = result['login_user_name']
      this.login_user_id = result['login_user_id']
      this.today_date = result['todays_date']
      this.all_feedback_records = result['all_feedbacks']
      this.sh_all_high_five_dashboard_records = result['sh_high_five_records_list']
      //** WALL OF FAME DETAILS **
      // First Employee 
      this.first_top_high_fiver_employee_id = result['first_top_high_fiver_employee_id']
      this.first_top_high_fiver_employee_name = result['first_top_high_fiver_employee_name']
      this.sh_name_of_highest_badge = result['sh_name_of_highest_badge']
      this.top_first_high_fiver_received_counts = result['top_first_high_fiver_received_counts']
      this.first_post_record_update_date = result['first_post_record_update_date']
      // Second Employee 
      this.second_top_high_fiver_employee_id = result['second_top_high_fiver_employee_id']
      this.second_top_high_fiver_employee_name = result['second_top_high_fiver_employee_name']
      this.top_second_high_fiver_given_count = result['top_second_high_fiver_given_count']
      this.top_second_high_fiver_received_count = result['top_second_high_fiver_received_count']
      this.second_post_record_update_date = result['second_post_record_update_date']
      // Third Employee 
      this.third_top_high_fiver_employee_id = result['third_top_high_fiver_employee_id']
      this.third_top_high_fiver_employee_name = result['third_top_high_fiver_employee_name']
      this.top_third_high_fiver_given_count = result['top_third_high_fiver_given_count']
      this.top_third_high_fiver_received_count = result['top_third_high_fiver_received_count']
      this.third_post_record_update_date = result['third_post_record_update_date']

  })

  // this.user_id = session.uid;
  this.action = useService("action");
  onMounted(this.onMounted);
  }
  onMounted() {
    $(".o_action").addClass("sh_dashboard_custom_class")

    // CODE TO HIGHLIGHT BADGES AND BOLD EMPLOYEE
    $('p.massage_reply_user_extra_text_name.mb-0').each(function() {
      // Get the text content of the paragraph
      var text = $(this).text();
  
      // Initialize a variable to store the modified text
      var modifiedText = text;
  
      // Check if the text contains a hashtag
      if (text.includes('#')) {
        // Use a regular expression to find and highlight the badge
        modifiedText = modifiedText.replace(/(#\S+)/g, '<span style="color: red;">$1</span>');
      }
  
      // Find the employee name
      var sh_received_emp_name = $(this).closest(".massage_reply_user_extra_text").find(".sh_bold_dashboard_parent_employee").text();
  
      // Check if the text contains the employee name
      if (text.includes(sh_received_emp_name)) {
        // Use a regular expression to find and bold the employee name
        modifiedText = modifiedText.replace(new RegExp(sh_received_emp_name, 'g'), '<span style="font-weight: bold;">'+sh_received_emp_name+'</span>');
      }
  
      // Apply the modified text
      $(this).html(modifiedText);
    });
  }

  onClickLatestCheckIn(ev) {
    var current_checkin_id = $(".my_check_in_item").attr("id")
    this.action.doAction({
      name: this.env._t("Latest Check In"),
      res_model: "sh.check.in",
      type: "ir.actions.act_window",
      view_mode: "form",
      views: [[false, "form"]],
      target: "current",
      res_id:parseInt(current_checkin_id),
    });
  }

  onClickLatestMeeting(ev) {
    var current_meeting_id = $(".my_metting_item").attr("id")
    this.action.doAction({
      name: this.env._t("Meetings"),
      res_model: "calendar.event",
      type: "ir.actions.act_window",
      view_mode: "form",
      views: [[false, "form"]],
      target: "current",
      res_id:parseInt(current_meeting_id),
    });
  }

  onClickLatest1on1sRecord() {
    var list_of_ids = this.details_of_1on1_records[0]['multiple_ids_list_for_tree']
    this.action.doAction({
      name: this.env._t("List Of 1on1's"),
      res_model: "sh.talking.points",
      type: "ir.actions.act_window",
      view_mode: "kanban",
      views: [[false, 'kanban'], [false, 'form']],
      target: "current",
      context: {
        search_default_sh_employee_id_filter: 1,
      },
    });
  }

// ================================================
// *** COPY METHODS FROM HIGH FIVE COMPONENT ***  
// ================================================

onClickLikeButton(ev) {
  ev.preventDefault();
  ev.stopPropagation();

  var closestUnlike = $(ev.target).closest(".massage_item").find("#unlike_button")
  var current_element = $(ev.target).closest(".massage_item").find("#like_button")
  var count_element = $(ev.target).closest(".massage_item").find("#like_count");
  var like_counts = count_element.text()
  var convert_into_int = parseInt(like_counts)
  var updated_likes_count = convert_into_int+1
  count_element.text(updated_likes_count)

  closestUnlike.removeClass("d-none")
  var closest_main_div = $(ev.target).closest('.massage_item')
  var record_id = closest_main_div.data('id')
  ajax.jsonRpc("/post/dashboard/like_btn/data", "call", {
    record_id: record_id,
  });
  current_element.addClass("d-none")
}

onClickUnlikeButton(ev) {
  ev.preventDefault();
  ev.stopPropagation();

  var count_element = $(ev.target).closest(".massage_item").find("#like_count");
  var like_counts = count_element.text()
  var convert_into_int = parseInt(like_counts)
  var updated_likes_count = convert_into_int-1
  count_element.text(updated_likes_count)

  var closestUnlike = $(ev.target).closest(".massage_item").find("#like_button")
  var find_current_element = $(ev.target).closest(".massage_item").find("#unlike_button")
  closestUnlike.removeClass("d-none")
  var closest_main_div = $(ev.target).closest('.massage_item')
  var record_id = closest_main_div.data('id')
  ajax.jsonRpc("/post/dashboard/unlike_btn/data", "call", {
    record_id: record_id,
  });
  find_current_element.addClass("d-none")
}

onClickDeleteButton(ev) {
  ev.preventDefault();
  ev.stopPropagation();

  // == Find the record Id == 
  var closest_main_div = $(ev.target).closest('.massage_item')
  closest_main_div.addClass("d-none")
  var record_id = closest_main_div.data('id')
  ajax.jsonRpc("/post/dashboard/delete_btn/data", "call", {
    record_id: record_id,
  });
}

// === Navigate To Particular View After Click From Dashboard ===

onClickOpenFeedback(ev) {
  ev.preventDefault();
  ev.stopPropagation();
  // alert("006")
  this.action.doAction({
    name: this.env._t("Feedback View"),
    res_model: "sh.realtime.feedback",
    type: "ir.actions.act_window",
    view_mode: 'list',
    views: [[false, 'list']],
    target: "current",
    // domain: [['id', 'in', res_ids]],
  });
}

onClickOpenHighFive(ev) {
  ev.preventDefault();
  ev.stopPropagation();
  this.action.doAction({
    name: this.env._t("High Five View"),
    res_model: "sh.high.five",
    type: "ir.actions.act_window",
    view_mode: 'list',
    views: [[false, 'list']],
    target: "current",
    // domain: [['id', 'in', res_ids]],
  });
}

onClickDashboardReplyBtn(ev) {
  ev.preventDefault();
  ev.stopPropagation();
  $(ev.target).addClass("d-none")
    $('.pending_respnc_class').addClass("d-none")
    var targetId = ev.target.getAttribute('data-target');
    // Remove the d-none class from the corresponding element
    var dynamicKanban = $('.' + targetId);
    // Check if targetId and dynamicKanban are correctly set
    if (targetId && dynamicKanban) {
        dynamicKanban.removeClass('d-none');
    }
    // Get The Current Record Id From data-target Attribute 
    var match = targetId.match(/\d+/);
    var CurrentRecordId = parseInt(match[0], 10);
    var dynamic_class_of_current_input = "sh_request_feedback_input_dynamic"+CurrentRecordId
    $('.' + dynamic_class_of_current_input).focus();
}


onClickDashboardPostBtn(ev) {
  ev.preventDefault();
  ev.stopPropagation();
  alert("006")
}
}







BrDashboard.template = "sh_br_dashboard_template";


registry.category("actions").add("sh_br_engaging.br_engage_dashboard_component", BrDashboard);
