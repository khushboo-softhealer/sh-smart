/** @odoo-module **/
import { registry } from "@web/core/registry";
import { listView } from '@web/views/list/list_view';
import { ListController } from "@web/views/list/list_controller";
import ajax from "web.ajax";
import { useService } from "@web/core/utils/hooks";
import { session } from "@web/session";
const { onMounted, onWillStart } = owl;

export class RealtimeFeedbackController extends ListController {
  setup() {
    super.setup();
    // Realtime Update Code 
    this.busService = this.env.services.bus_service;
    // this.env.services['bus_service'].addEventListener('notification', this.Jatin);
    onWillStart(async () => {
      // ---------------------- Realtime Update Code -----------------
      this.busService.addEventListener(
        "notification",
        ({ detail: notifications }) => {
          for (var i = 0; i < notifications.length; i++) {
            var channel = notifications[i]["type"];
            if (channel == "new.feedback") {
              if ($('.sh_realtime_feedback_custom_class').length) {
                this.actionService.switchView("list");
              }

              // this.actionService.switchView("list");
            }
          }
        }
      );
      // -------------------------- Realtime Update Code ------------------------------- 
        let result = await ajax.jsonRpc("/get/realtime_feedback/data", "call");
        this.all_feedbacks = result['all_feedbacks']
        this.login_user_name = result['login_user_name'];
        this.today_date_in_string_format = result['today_date_in_string_format'];
        this.pending_feedback_requests = result['pending_feedback_requests'];
        this.pending_request_records_length = result['pending_request_records_length'];
        this.group_by_feedback_list = result['group_by_feedback_list'];
    })

    this.user_id = session.uid;
    onMounted(this.onMounted);
  }


  onMounted() {
    // =========== CODE TO HIDE THE DATE FROM BLANK ELEMENTS ==============

    var feedbackItems = $('.feedback_items');
    // Filter out the empty elements
    var emptyFeedbackItems = feedbackItems.filter(function () {
      // Check if the current element has no child elements
      return $(this).children().length === 0;
    });

    // Perform For Loop And Hide Find The Closest Parent Element
    emptyFeedbackItems.each(function () {
      // FInd The Parent Element And Hide Them
      $(this).closest(".massage_panel_box").addClass("d-none")
    });
    // =========== CODE TO HIDE THE DATE FROM BLANK ELEMENTS ============== 

    $("body").removeClass("sh_givefeedback");
    $("body").removeClass("sh_requestfeedback");
    $("#expandallbtn").prop("disabled", true);
  }

  onClickReplyBtn(ev) {
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

onClickPostBtn(ev) {
  var nearestInput = $(ev.target).closest('.dynamic_nested_kanban_text').find('.sh_request_feedback_input');
  var warning_element = $(ev.target).closest('.dynamic_nested_kanban_text').find('.sh_reply_feedback_required_warning');
  var nearestInputValue = nearestInput.val();
  var self = this;
  // $(nearestInput).prop('readonly', true);
  // $(nearestInput).css({'background-color':'white', 'border': 'none',
  // 'outline': 'none',
  // 'box-shadow': 'none'});
  // === ADD REPLY INPUT REQUIRED VALIDATION == 
  if (nearestInputValue) {
    $(ev.target).hide();
    var parent_record_id = $(ev.target).attr("id")
  
    ajax.jsonRpc("/post/realtime_feedback/data", "call", {
      feedback_text : nearestInputValue,
      date_of_feedback_record: this.today_date_in_string_format,
      parent_record_id : parent_record_id,
    })
    .then(function (rpc_reponce) {
    self.actionService.switchView('list');
    });
    // this.actionService.switchView('list');
  }
  else {
    warning_element.removeClass("d-none")
  }
 
}


onClickExpanAllBtn(ev) {
  $("#collapsallbtn").prop("disabled", false);
  $("#expandallbtn").prop("disabled", true);
  $(".dynamic_conditional_child_kanban").removeClass("d-none");
  // $(".dynamic_nested_kanban:not(.d-none)").toggle();
  $(".sh_showresponcebtn").addClass("d-none");
  // $(".dynamic_nested_kanban").toggle();
  
}
onClickCollapseAllBtn(ev) {
  $("#expandallbtn").prop("disabled", false);
  $("#collapsallbtn").prop("disabled", true);
  $(".dynamic_conditional_child_kanban").addClass("d-none");
  // $(".dynamic_nested_kanban:not(.d-none)").toggle();
  $(".sh_showresponcebtn").removeClass("d-none");
  // $(".sh_showresponcebtn").toggle();
  // $(".dynamic_nested_kanban").toggle();
}
onClickViewResponce(ev) {
  $(ev.target).addClass("d-none");
  var nearestConditionalKanban = $(ev.target).closest('.feedback_item').find('.dynamic_conditional_child_kanban');

  nearestConditionalKanban.removeClass("d-none");
  nearestConditionalKanban.css("display", "block");
  // $(ev.target).closest('.dynamic_conditional_child_kanban').removeClass("d-none");

}

onClickPendingRequest(recordId) {
  var feedbackItem = $('#feedback_item_' + recordId);
    if (feedbackItem.length > 0) {
        feedbackItem[0].scrollIntoView({ behavior: 'smooth' });
        feedbackItem.addClass("sh_feedback_highlight")
    }
    setTimeout(function () {
      $(".feedback_item").removeClass("sh_feedback_highlight");
  }, 10000);
}


}

RealtimeFeedbackController.template = "br_relatime_feedback_template";
export const BrRealtimeFeedback = {
  ...listView,
  Controller: RealtimeFeedbackController,
};

registry.category("views").add("br_engage_realtime_feedback", BrRealtimeFeedback);
