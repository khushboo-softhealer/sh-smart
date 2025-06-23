/** @odoo-module **/
import { registry } from "@web/core/registry";
import { formView } from "@web/views/form/form_view";
import { FormController } from "@web/views/form/form_controller";
import ajax from "web.ajax";
import { useService } from "@web/core/utils/hooks";
import { session } from "@web/session";
import { FormViewDialog } from '@web/views/view_dialogs/form_view_dialog';

const { onMounted, onWillStart } = owl;

export class BrTalkinPointFormController extends FormController {
  setup() {
    this.rpc = useService("rpc");
    super.setup();
    onWillStart(async () => {
        let result = await ajax.jsonRpc("/get/talking_point/data", "call", {res_id: this.props.resId});
        this.even_id = result['even_id'];
        this.list_of_agenda_dict = result['list_of_agenda_dict'];
        this.takling_point_employee_name = result['takling_point_employee_name'];
        this.answers_value_dict = result['answers_value_dict'];
        this.previous_talking_points_value_dict = result['previous_talking_points_value_dict'];
        this.current_scheduled_event = result['current_scheduled_event'];
        this.previous_scheduled_event_list = result['previous_scheduled_event_list'];
        this.is_submitted=result['is_submitted']
        this.date_information=result['date_information']
        this.is_allow_delete_meeting_agenda=result['is_allow_delete_meeting_agenda']
        this.allow_to_end_one_on_one=result['allow_to_end_one_on_one']

    })

    this.action = useService("action");
    this.dialog = useService('dialog');

    // this.user_id = session.uid;
    // this.list_of_rating_questions_answer = []
    // onMounted(this.onMounted);
  }

  UpdateAgendaList(){
    var context = ({
      'default_sh_talking_point_id': this.props.resId,
    })
    this.action.doAction({
      name: this.env._t("Update Agenda"),
      res_model: "sh.update.agenda.wizard",
      type: "ir.actions.act_window",
      view_mode: "form",
      views: [[false, "form"]],
      target: "new",
      context:context
    });
  }

  ScheduleOneonOnes(){
    $(".o_web_client").addClass("sh_talking_point_popups")
    var context = ({
      'default_sh_talking_point_id': this.props.resId,
      'default_partner_ids': this.takling_point_employee_name.related_partner_ids,
    })
    // this.action.doAction({
    //   name: this.env._t("Schedule 1-on-1s"),
    //   res_model: "calendar.event",
    //   type: "ir.actions.act_window",
    //   view_mode: "form",
    //   views: [[false, "form"]],
    //   target: "new",
    //   context:context

    // });

    this.openFormViewDialog({
      context,
      title: this.env._t('New 1-on-1s'),
      resModel: 'calendar.event',
      onRecordSaved: async () => {
          await this.LoadOneOnOnes();
      },
    },
    { onClose: () => $(".o_web_client").removeClass("sh_talking_point_popups") }
    );


  }


  DiscardOneOnOnes(){
    // this.action.switchView('form');
    // this.setup()
    location.reload()

  }

  handleCheckboxChange(ev) {
    $(".sh_save_oneonone_btn").removeClass('d-none');
    $(".sh_discard_oneonone_btn").removeClass('d-none');
    var current_checkbox = $(ev.target)
    var checked = current_checkbox.prop('checked');
    var temp_text_area_element = current_checkbox.closest(".checkbox_item").find("#sh_temp_js_textarea")
    var sh_backend_data_textarea = current_checkbox.closest(".checkbox_item").find("#sh_main_backend_data_description")
    if(checked == true) {
      temp_text_area_element.removeClass("d-none")
    }
    else {
      temp_text_area_element.addClass("d-none")
      sh_backend_data_textarea.addClass("d-none")
    }

  }

  handleKeyDown(){
    if(!this.is_submitted){
      $(".sh_save_oneonone_btn").removeClass('d-none');
      $(".sh_discard_oneonone_btn").removeClass('d-none');
    }
  }

  OpenExistEvent(event_id){
    var context = ({
      'create': false,
      'edit': false,
    })
    this.action.doAction({
      name: this.env._t("Schedule 1-on-1s"),
      res_model: "calendar.event",
      type: "ir.actions.act_window",
      view_mode: "form",
      views: [[false, "form"]],
      target: "new",
      res_id:event_id,
      context:context,
    });

  }

  async LoadOneOnOnes() {
    // on save button code here
    location.reload()
}

  async ReScheduleOneonOnes(){
    $(".o_web_client").addClass("sh_talking_point_popups")
    const isValid = await this.SaveOneonOnes("IsFromReschedule");

    if (isValid) {
      var context = ({
        'default_sh_talking_point_id': this.props.resId,
        'default_sh_is_rescheduled':true,
        'default_partner_ids': this.takling_point_employee_name.related_partner_ids,

        is_modal:true,

      })
      
      // this.action.doAction({
      //   name: this.env._t("Schedule 1-on-1s"),
      //   res_model: "calendar.event",
      //   type: "ir.actions.act_window",
      //   view_mode: "form",
      //   views: [[false, "form"]],
      //   target: "new",
      //   context:context,
      // });

      this.openFormViewDialog({
        context,
        title: this.env._t('New 1-on-1s'),
        resModel: 'calendar.event',
        onRecordSaved: async () => {
            await this.LoadOneOnOnes();
        },
      },
      { onClose: () => $(".o_web_client").removeClass("sh_talking_point_popups") }
      );

    }
  }

  // standard openformviewDialog method
  async openFormViewDialog(params, options = {}) {
    this.dialog.add(FormViewDialog, params, options);
  }


  async EndOneonOnes() {

        // MAKE THE ALL ELEMENTS READONLY 
        $(".sh_one_ones_textarea").each(function(){
          $(this).prop("readonly", true)
        })
        $(".sh_checked_ageda").prop('disabled', true);
        $(".your_notes").prop("readonly", true)
        $(".employee_notes").prop("readonly", true)
        $(".private_note").prop("readonly", true)
        $(".checkbox_item_delete").each(function(){
          $(this).addClass("d-none")
        })


        // var your_notes = []
        // var employee_notes = []
        var talking_point_answers = {}
        // var sharedNoteIdElement = $('#shared_note_id');

        if ($(".your_notes").val()){
          // $(".validation_your_notes").addClass("d-none");
          talking_point_answers['your_notes']=$(".your_notes").val()
        }
        if ($(".employee_notes").val()){
          // $(".validation_employee_notes").addClass("d-none");
          talking_point_answers['employee_notes']=$(".employee_notes").val()

        }

        // if(your_notes.length && employee_notes.length){

            // final code after validation of every fields
            // ===========================================

          // for checked agenda list update in backend
          // ====================================================
          // ==== CODE FOR DESCRIPTION AND BOOLEAN FALSE ====
          // ====================================================
          var checked_agenda_records = [];
          $(".sh_checked_ageda").each(function(index, element) {
              var checked = $(element).prop('checked');
              // === DEFINE THE VARIABLE FOR DESCRIPTION VALUE, GET THE VALUE FROM DIFFERENT TEXTARES ===
              // ===========================================================================
              var value_of_description = ''; 
              // ===========================================================================
              // FIND THE TEMP ELEMENT AND GET THE VALUE OF DESCRIPTION FROM TEXTAREA 
              // =============================================================================
              var temp_js_description_element = $(element).closest(".checkbox_item").find("#sh_temp_js_textarea")
              var temp_textarea_element = temp_js_description_element.children()
              // =============================================================================
              // FIND THE MAIN BACKEND ELEMENT AND GET THE VALUE OF DESCRIPTION FROM TEXTAREA 
              // =============================================================================
              var main_backend_data_element = $(element).closest(".checkbox_item").find("#sh_main_backend_data_description")
              if (main_backend_data_element){
                var main_data_textarea = main_backend_data_element.children()
              }
              // =============================================================================
              // ADD CONDITION IF WE FIND THE VALUE OF OUR MAIN BACKEND INPUT SO WE USE THAT ELSE WE USE OUR TEMP INPUT VALUE AS DESCRIPTION  
              // =============================================================================
              if (main_data_textarea.val()) {
                  checked_agenda_records.push({
                    id: $(element).attr("id"),
                    checked: checked,
                    description : main_data_textarea.val()
                });
              }
              else {
                  checked_agenda_records.push({
                    id: $(element).attr("id"),
                    checked: checked,
                    description : temp_textarea_element.val()
                }); 
              }
            
          });
          // ====================================================
          // ====================================================

          if ($('.private_note').val()){

            talking_point_answers['private_note']=$(".private_note").val()

          }
          if ($('.user_note').val()){
            talking_point_answers['user_note']=$(".user_note").val()

          }

          // submitted code here
          this.is_submitted=true

          $(".sh_save_one_btn").addClass('d-none')
          $(".sh_ent_one_btn").addClass('d-none')
          $(".sh_schedule_btn").addClass('d-none')
          $(".sh_reschedule_btn").addClass('d-none')
          $(".plus_icon").addClass('d-none')

          ajax
            .jsonRpc("/end/1-on-1s", "call", {
              res_id: this.props.resId,
              checked_agenda_records: checked_agenda_records,
              talking_point_answers: talking_point_answers,
              is_submitted: true,
            })
            // .then(function (rpc_reponce) {
            //     location.reload()
            // });
          
          return true


        // }
        // else if (!your_notes.length && !employee_notes.length) {
        //   $(".validation_your_notes").removeClass("d-none");
        //   $(".validation_employee_notes").removeClass("d-none");
        //   if (sharedNoteIdElement.length > 0) {
        //     sharedNoteIdElement[0].scrollIntoView({ behavior: 'smooth' });
        //   }
        // }else if (!your_notes.length) {
        //   $(".validation_your_notes").removeClass("d-none");
        //   if (sharedNoteIdElement.length > 0) {
        //     sharedNoteIdElement[0].scrollIntoView({ behavior: 'smooth' });
        //   }
        // }else if (!employee_notes.length) {
        //   $(".validation_employee_notes").removeClass("d-none");
        //   if (sharedNoteIdElement.length > 0) {
        //     sharedNoteIdElement[0].scrollIntoView({ behavior: 'smooth' });
        //   }
        // }

        }


  async SaveOneonOnes(IsFromReschedule) {

        $(".sh_save_oneonone_btn").addClass('d-none');
        $(".sh_discard_oneonone_btn").addClass('d-none');

        // var your_notes = []
        // var employee_notes = []
        var talking_point_answers = {}
        // var sharedNoteIdElement = $('#shared_note_id');

        if ($(".your_notes").val()){
          // $(".validation_your_notes").addClass("d-none");
          talking_point_answers['your_notes']=$(".your_notes").val()
        }


        if ($(".employee_notes").val()){
          // $(".validation_employee_notes").addClass("d-none");
          talking_point_answers['employee_notes']=$(".employee_notes").val()
        }


        if ($('.private_note').val()){
          talking_point_answers['private_note']=$('.private_note').val()
        }
        if ($('.user_note').val()){
          talking_point_answers['user_note']=$('.user_note').val()
        }

        var checked_agenda_records = [];
        $(".sh_checked_ageda").each(function(index, element) {
            var checked = $(element).prop('checked');
            // === DEFINE THE VARIABLE FOR DESCRIPTION VALUE, GET THE VALUE FROM DIFFERENT TEXTARES ===
            // ===========================================================================
            var value_of_description = ''; 
            // ===========================================================================
            // FIND THE TEMP ELEMENT AND GET THE VALUE OF DESCRIPTION FROM TEXTAREA 
            // =============================================================================
            var temp_js_description_element = $(element).closest(".checkbox_item").find("#sh_temp_js_textarea")
            var temp_textarea_element = temp_js_description_element.children()
            // =============================================================================
            // FIND THE MAIN BACKEND ELEMENT AND GET THE VALUE OF DESCRIPTION FROM TEXTAREA 
            // =============================================================================
            var main_backend_data_element = $(element).closest(".checkbox_item").find("#sh_main_backend_data_description")
            if (main_backend_data_element){
              var main_data_textarea = main_backend_data_element.children()
            }
            // =============================================================================
            // ADD CONDITION IF WE FIND THE VALUE OF OUR MAIN BACKEND INPUT SO WE USE THAT ELSE WE USE OUR TEMP INPUT VALUE AS DESCRIPTION  
            // =============================================================================
            if (main_data_textarea.val()) {
                checked_agenda_records.push({
                  id: $(element).attr("id"),
                  checked: checked,
                  description : main_data_textarea.val()
              });
            }
            else {
                checked_agenda_records.push({
                  id: $(element).attr("id"),
                  checked: checked,
                  description : temp_textarea_element.val()
              }); 
            }
           
        });



        // if (IsFromReschedule =='IsFromReschedule'){
        //   if(your_notes.length && employee_notes.length){
        //       ajax
        //         .jsonRpc("/end/1-on-1s", "call", {
        //           res_id: this.props.resId,
        //           checked_agenda_records: checked_agenda_records,
        //           talking_point_answers: talking_point_answers,
        //         })
        //       return true

        //   }
        //   else if (!your_notes.length && !employee_notes.length) {
        //     $(".validation_your_notes").removeClass("d-none");
        //     $(".validation_employee_notes").removeClass("d-none");
        //     if (sharedNoteIdElement.length > 0) {
        //       sharedNoteIdElement[0].scrollIntoView({ behavior: 'smooth' });
        //     }
        //   }else if (!your_notes.length) {
        //     $(".validation_your_notes").removeClass("d-none");
        //     if (sharedNoteIdElement.length > 0) {
        //       sharedNoteIdElement[0].scrollIntoView({ behavior: 'smooth' });
        //     }
        //   }else if (!employee_notes.length) {
        //     $(".validation_employee_notes").removeClass("d-none");
        //     if (sharedNoteIdElement.length > 0) {
        //       sharedNoteIdElement[0].scrollIntoView({ behavior: 'smooth' });
        //     }
        //   }


        // } else {


          ajax
          .jsonRpc("/end/1-on-1s", "call", {
            res_id: this.props.resId,
            checked_agenda_records: checked_agenda_records,
            talking_point_answers: talking_point_answers,
            is_submitted: false,
          })
          // .then(function (rpc_reponce) {
          //   if (IsFromReschedule !='IsFromReschedule'){
          //     location.reload()
          //   }
          //   });
        return true

        }


    EditEvent(event_id, ev){
        $(".o_web_client").addClass("sh_talking_point_popups")
        ev.preventDefault();
        ev.stopPropagation();
        var context = ({
          'create': false,
        })

        this.openFormViewDialog({
          context,
          title: this.env._t('New 1-on-1s'),
          resModel: 'calendar.event',
          resId :event_id,
          onRecordSaved: async () => {
              await this.LoadOneOnOnes();
          },
        },
        { onClose: () => $(".o_web_client").removeClass("sh_talking_point_popups") }
        );
        // this.action.doAction({
        //   name: this.env._t("Schedule 1-on-1s"),
        //   res_model: "calendar.event",
        //   type: "ir.actions.act_window",
        //   view_mode: "form",
        //   views: [[false, "form"]],
        //   target: "new",
        //   res_id:event_id,
        //   context:context,
        // });
    
      }
    
    onClickDeleteAgenda(agenda_id, ev) {
      var current_agenda_record = $(ev.target).closest(".checkbox_item")
      current_agenda_record.addClass("d-none")
      ajax.jsonRpc("/post/delete_agenda/record", "call", {res_id: agenda_id});
    }

    // === ADD THE HANDLE CHANGE EVENT IN BOTH NEW AGENDA TEXT BOXES ===

    handleTempJsTexatarea() {
      $(".sh_save_oneonone_btn").removeClass('d-none');
      $(".sh_discard_oneonone_btn").removeClass('d-none');
    }
    handleMainTexatarea() {
    $(".sh_save_oneonone_btn").removeClass('d-none');
    $(".sh_discard_oneonone_btn").removeClass('d-none');
    }

    ViewAgenda(talking_point_id){
      var self=this
      this.rpc("/web/dataset/call_kw/sh.talking.point.view.agenda/search_read", {
        model: 'sh.talking.point.view.agenda',
        method: 'search_read',
        args: [[['sh_view_agenda_talking_point_id', '=', talking_point_id]]],
        kwargs: {}
    }).then(function (result) {

      var agenda_point_ids=[]
      result.forEach(agenda => {
        agenda_point_ids.push(agenda.id)
      });

      self.action.doAction({
        // name: this.env._t("View Agendas"),
        res_model: "sh.view.talking.point.wizard",
        type: "ir.actions.act_window",
        view_mode: 'form',
        views: [[false, 'form']], // Use the custom tree view
        target: "new",
        context: {
            "default_sh_talking_point_view_agenda_ids": agenda_point_ids,
        }
    });
    })



  }
  
}

BrTalkinPointFormController.template = "one_on_ones_templates";
export const BrTalkinPointFormview = {
  ...formView,
  Controller: BrTalkinPointFormController,
};

registry.category("views").add("br_engage_one_on_ones", BrTalkinPointFormview);
