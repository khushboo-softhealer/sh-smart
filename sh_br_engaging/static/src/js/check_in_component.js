/** @odoo-module **/
import { registry } from "@web/core/registry";
import { formView } from "@web/views/form/form_view";
import { FormController } from "@web/views/form/form_controller";
import ajax from "web.ajax";
import { useService } from "@web/core/utils/hooks";
import { session } from "@web/session";
const { onMounted, onWillStart } = owl;

export class BrFormController extends FormController {
  setup() {
    super.setup();
    onWillStart(async () => {
        let result = await ajax.jsonRpc("/get/check_in/data", "call", {res_id: this.props.resId});
        this.non_rating_questions = result['non_rating_questions'];
        this.rating_questions = result['rating_questions'];
        this.login_user_name = result['login_user_name'];
        this.answers_records = result['ans_records_for_submited_model'];
        this.is_record_submitted = result['sh_is_record_submited'];
        this.rating_questions_answer_record = result['rating_ans_for_submited_model'];
        this.name = result['name'];
        this.smart_button_1_on_1s_data = result['smart_button_1_on_1s_data'];
        var used_object_in_history = result['check_in_model_id_name_dict'];
        this.sh_how_feel_question_id = result['sh_how_feel_question_id'];
        this.stage = result['stage']
        this.id_name_dict = [];
        this.store_history_records_id = [];

        for (var key in used_object_in_history) {
            if (used_object_in_history.hasOwnProperty(key)) {
              this.id_name_dict.push({ 'id': key, 'name': used_object_in_history[key] });
              this.store_history_records_id.push(key)
            }
        }
    })
    this.user_id = session.uid;
    this.list_of_rating_questions_answer = []
    this.list_of_why_answers_in_rating_questions = []
    this.action = useService("action");
    onMounted(this.onMounted);
  }

  onMounted() {
    // console.log("\n\n\n\n\n\n\n\n From rating_questions", this.rating_questions);
    // console.log("\n\n\n\n\n\n\n\n From non_rating_questions", this.non_rating_questions);
    var rating_questions_dict = this.rating_questions;
    var non_rating_questions_dict = this.non_rating_questions;

    // Code for Rating Questions with Saved Records
    rating_questions_dict.forEach(function (dictionary) {
        if (dictionary.answer_text) {
            var questionId = dictionary.question_id;
            var answerText = parseInt(dictionary.answer_text);

            // Find the div with the corresponding data-id attribute
            var ProgressbarDiv = $('.steps_div[data-id="' + questionId + '"]');

            // Check if answerText is within the expected range (1 to 5)
            if (answerText >= 1 && answerText <= 5) {
                var rating_div = ProgressbarDiv.find('.step_box[id="' + answerText + '"]');

                // Check if the rating_div element was found
                if (rating_div.length > 0) {
                    rating_div.click();
                } else {
                    // console.log("Element with answer_text " + answerText + " not found for question " + questionId);
                }
            } else {
                // console.log("Invalid answer_text: " + answerText + " for question " + questionId);
            }
        }
        // *** Code To Fill The Low Reason Input (Code As Upper Format) ***
        if (dictionary.low_rating_reason) {
          var questionId = dictionary.question_id;
          var answerText = parseInt(dictionary.answer_text);

          // Find the div with the corresponding data-id attribute
          var ProgressbarDiv = $('.steps_div[data-id="' + questionId + '"]');
          // console.log("\n\n\n\n\n ProgressbarDiv", ProgressbarDiv);
          let find_low_reason_input = ProgressbarDiv.closest('.progress_bar_main').find('.why_funct_input_element')
          // console.log("\n\n\n\n\n find_low_reason_input", find_low_reason_input);

          find_low_reason_input.val(dictionary.low_rating_reason)
      }
    });


    // Code Of Non Rating Questions On Save Method 
    non_rating_questions_dict.forEach(function (dictionary) {
      $(".sh_save_checkIn_btn").addClass("d-none")
      $(".sh_discard_checkIn_btn").addClass("d-none")
      if(dictionary.answer_text) {
        var questionId = dictionary.question_id;
        var answerText = dictionary.answer_text;
  
        // Find the div with the corresponding data-id attribute
        var $targetDiv = $('.quations_ideas[data-id="' + questionId + '"]');
  
        // Check if the div was found
        if ($targetDiv.length > 0) {
            // Update the input field within the div with the answer text
            $targetDiv.find('.sh_answers').val(answerText);
        }
      }
    });
    // Code For Submit Method 
    if (this.answers_records && this.is_record_submitted) {
      var answer_values = this.answers_records 
      var inputElements = $('input.form-control.sh_answers');
      inputElements.each(function(index, element) {
        // Set the value of each input element
        $(element).val(answer_values[index]);
        $(element).prop('readonly', true);
        $(element).css({'background-color':'white', 'border': 'none',
        'outline': 'none',
        'box-shadow': 'none'});
        $('.sh_submit_btn').hide();
    });

    if (this.rating_questions_answer_record) {
      var rating_questions_answer_record = this.rating_questions_answer_record
      $('.step_box_starting_text').addClass('d-none');
      $('.step_box_text_amazing').addClass('d-none');
      $('.count_text').addClass('d-none');
      $(".step_box").each(function (index, element) {
        $(element).addClass('d-none');
      });

      $(".rating_questions_answer_element").each(function (index, element) {
        $(element).removeClass('d-none');
        $(element).html("Your Rating Is "+rating_questions_answer_record[index]+" Out Of 5");
      });
      
    }

    // === Hide Low Rating Reason Input After Submit ===
    $(".why_functionality_section").each(function () {
      $(this).hide();
    });
    }
  }

  ViewHistory() {
    this.action.doAction({
      name: this.env._t("Check-In History"),
      res_model: "sh.check.in",
      type: "ir.actions.act_window",
      view_mode: 'list,form',
      views: [[false, 'list'], [false, 'form']],
      target: "current",
      domain: [['id', 'in', this.store_history_records_id]],
      context: {
        "delete": false,
    }
    });
  }


  SmartButtonEvents(SmartButtonData){

    if (SmartButtonData){

      var res_ids=SmartButtonData.event_ids
      this.action.doAction({
        name: this.env._t("Check-In History"),
        res_model: "calendar.event",
        type: "ir.actions.act_window",
        view_mode: 'list,form',
        views: [[false, 'list'], [false, 'form']],
        target: "current",
        domain: [['id', 'in', res_ids]],
        context: {
          "delete": false,
      }
      });


    }

  }



  async validateAnswers() {

    if(this.non_rating_questions.length && this.rating_questions.length) {
      var rating_questions_boolean = false
      const nonRatingAnswers = document.querySelectorAll('input.form-control.sh_answers');
      const areNonRatingAnswersEmpty = Array.from(nonRatingAnswers).some(input => !input.value);
      if (this.list_of_rating_questions_answer.length != this.rating_questions.length) {
        rating_questions_boolean = false
      }
      else {
        rating_questions_boolean = true
      }

      // *** Add New Functionality Low Rating Questions Reason Validation ***
      // ===
      const low_rating_reason_input = document.querySelectorAll('input.why_funct_input_element');
      // *** Filter out inputs whose parent div does not have the class 'd-none' ***
      const filteredInputs = Array.from(low_rating_reason_input).filter(input => {
        const parentDiv = input.closest('.why_functionality_section');
        return parentDiv && !parentDiv.classList.contains('d-none');
      });

      const are_low_rating_input_empty = Array.from(filteredInputs).some(input => !input.value);
      // ===

      return !areNonRatingAnswersEmpty && rating_questions_boolean && !are_low_rating_input_empty;
    }
    else if (this.non_rating_questions.length) {
      const nonRatingAnswers = document.querySelectorAll('input.form-control.sh_answers');
      const areNonRatingAnswersEmpty = Array.from(nonRatingAnswers).some(input => !input.value);
      return !areNonRatingAnswersEmpty;
    }
    else if (this.rating_questions.length) {

      // *** Add New Functionality Low Rating Questions Reason Validation ***
      // ===
      const low_rating_reason_input = document.querySelectorAll('input.why_funct_input_element');
      // *** Filter out inputs whose parent div does not have the class 'd-none' ***
      const filteredInputs = Array.from(low_rating_reason_input).filter(input => {
        const parentDiv = input.closest('.why_functionality_section');
        return parentDiv && !parentDiv.classList.contains('d-none');
      });

      const are_low_rating_input_empty = Array.from(filteredInputs).some(input => !input.value);
      // ===

      if (this.list_of_rating_questions_answer.length != this.rating_questions.length || are_low_rating_input_empty == true) {
          return false
      }
      else {
        return true
      }
    }
  }

  async SubmitCheckIn(ev) {
    var self = this;
    const isValid = await this.validateAnswers();
    if (isValid) {
        var internal_rating_question_list = this.list_of_rating_questions_answer
        var answer_records_for_one2many = [];
        $(".sh_answers").each(function () {
          answer_records_for_one2many.push($(this).val());
        });


        // === Code To Get The Value Of Low Reason Input ===
        let submit_low_rating_questions_reason_list = []
        $(".why_funct_input_element").each(function () {
          // console.log("\n\n\n\n\n Dollar Thisssss", $(this).val());
          var closest_main_div = $(this).closest('.progress_bar_main').find('.steps_div')
          var reason_inputId = closest_main_div.data('id')
          var answer_values = $(this).val()
          submit_low_rating_questions_reason_list.push({ reason_inputId, answer_values });
        });
        // console.log("\n\n\n\n\n\n\n low_rating_questions_reason_list", submit_low_rating_questions_reason_list);
    
    
        ajax
          .jsonRpc("/submit/data", "call", {
            res_id: this.props.resId,
            non_rating_answers_records: answer_records_for_one2many,
            rating_answers_records: internal_rating_question_list,
            submit_low_rating_questions_reason_list: submit_low_rating_questions_reason_list,
          })
          .then(function (rpc_reponce) {
            // ** REDIRECT TO THE 1ONS'S FORM VIEW IF LESS RATING             
            if (rpc_reponce) {
                self.action.doAction({
                  name: "1ons View",
                  res_model: "sh.talking.points",
                  type: "ir.actions.act_window",
                  view_mode: 'form',
                  views: [[false, 'form']], // Use the custom tree view
                  target: "current",
                  res_id: rpc_reponce
                  
              });
            }
            else {
              location.reload()
            }
            
          });
    } else {
      // Display an alert or message to indicate validation failure
      // console.log("\n\n\n\n\n validation P Tag", $(".validation_element"));
      $(".validation_element").removeClass("d-none");
    }
  }


onClickProgressBar(ev) {
  $(".sh_save_checkIn_btn").removeClass('d-none');
  $(".sh_discard_checkIn_btn").removeClass('d-none');
  var $currentProgressBar = $(ev.target).closest('.steps_div');
  var closest_why_section = $(ev.target).closest('.progress_bar_main').find('.why_functionality_section');
  // console.log("\n\n\n\n\n closest_why_section", closest_why_section);
  var selectedRating = ev.target.id;
  // Get the ID of the current progress bar
  var progressBarId = $currentProgressBar.data('id');
  // == Code To Change Text Based On Ratings === 
  var check_in_text_element = $(ev.target).closest(".checkin_work_panel").find(".count_text")
  var convert_rating_to_int = parseInt(selectedRating)  
  // === This code is only for how you feel question functionality ===
  if (progressBarId == this.sh_how_feel_question_id) {
    if (convert_rating_to_int == 1) {
      check_in_text_element.text("Sometimes It happens with all. How can I help?")
    }
    if (convert_rating_to_int == 2) {
      check_in_text_element.text("Are there any roadblocks you'd like to discuss?")
    }
    if (convert_rating_to_int == 3) {
      check_in_text_element.text("Is there something else you'd like to bring up?")
    }
    if (convert_rating_to_int == 4) {
      check_in_text_element.text("Everything's going well so far")
    }
    if (convert_rating_to_int == 5) {
      check_in_text_element.text("Excellent! we are glad to know that you had a great experience!")
    }
  }

  // === Need to write Same upper conditional code to manage Why Functionality ===
  if (convert_rating_to_int == 1) {
    closest_why_section.removeClass("d-none")
  }
  
  if (convert_rating_to_int == 2) {
    closest_why_section.removeClass("d-none")
  }
  if (convert_rating_to_int == 3) {
    closest_why_section.removeClass("d-none")
  }
  if (convert_rating_to_int == 4) {
    closest_why_section.addClass("d-none")
  }
  if (convert_rating_to_int == 5) {
    closest_why_section.addClass("d-none")
  }
  
  // Remove the previous rating for this progress bar, if it exists
  this.list_of_rating_questions_answer = this.list_of_rating_questions_answer.filter(item => item.progressBarId !== progressBarId);
  
  // Add the current rating to the list
  this.list_of_rating_questions_answer.push({ progressBarId, selectedRating });

  
  
  // Remove "active" class from the current progress bar's elements
  $currentProgressBar.find('.step_box').removeClass('active');
  
  // Add "active" class to the clicked element and previous elements
  $(ev.target).addClass('active');
  $currentProgressBar.find('.step_box:lt(' + (parseInt(selectedRating)) + ')').addClass('active');
  // console.log("\n\n\n\n\n  this.list_of_rating_questions_answer",  this.list_of_rating_questions_answer);

}

SaveCheckIn(ev) {
  $(".sh_save_checkIn_btn").addClass('d-none');
  $(".sh_discard_checkIn_btn").addClass("d-none");
  var internal_rating_question_list_for_save = this.list_of_rating_questions_answer
    var answer_records_for_one2many = [];
    // Create Dictionary Of Questions Id And Answers Of Question 
    $(".sh_answers").each(function () {
      var closest_main_div = $(this).closest('.quations_ideas')
      var InputId = closest_main_div.data('id')
      var answer_values = $(this).val()
      answer_records_for_one2many.push({ InputId, answer_values });
    });

    // === Code To Get The Value Of Why Input ===
    let low_rating_questions_reason_list = []
    $(".why_funct_input_element").each(function () {
      // console.log("\n\n\n\n\n Dollar Thisssss", $(this).val());
      var closest_main_div = $(this).closest('.progress_bar_main').find('.steps_div')
      var reason_inputId = closest_main_div.data('id')
      var answer_values = $(this).val()
      low_rating_questions_reason_list.push({ reason_inputId, answer_values });
    });
    // console.log("\n\n\n\n\n\n\n low_rating_questions_reason_list", low_rating_questions_reason_list);



    ajax
      .jsonRpc("/save/data", "call", {
        res_id: this.props.resId,
        non_rating_answers_records: answer_records_for_one2many,
        rating_answers_records: internal_rating_question_list_for_save,
        low_rating_questions_records: low_rating_questions_reason_list,
      })
      .then(function (rpc_reponce) {
      });
}

DiscardCheckIn() {
  this.action.switchView('form');
}

handleKeyDown(ev) {
  $(".sh_save_checkIn_btn").removeClass('d-none');
  $(".sh_discard_checkIn_btn").removeClass('d-none');
}

handleKeyLowReasonInput() {
  $(".sh_save_checkIn_btn").removeClass('d-none');
  $(".sh_discard_checkIn_btn").removeClass('d-none');
}

// onClickHistoryRecords(ev) {
//   var currentElement = $(ev.target).closest('.history_main_div');
//   this.action.doAction({
//     type: 'ir.actions.act_window',
//     res_model: 'sh.check.in',
//     res_id: currentElement.data('id'),
//     views: [[false, "form"]],
//     view_mode: "form",
//     target: "current",
// });

// }
}

BrFormController.template = "br_check_in_templates";
export const BrFormView = {
  ...formView,
  Controller: BrFormController,
};

registry.category("views").add("br_engage_check_in", BrFormView);
