/** @odoo-module **/
import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListController } from "@web/views/list/list_controller";
import ajax from "web.ajax";
import { useService } from "@web/core/utils/hooks";
import { session } from "@web/session";
const {Component,onMounted, onWillStart,onRendered, onWillRender, onWillUpdateProps,useState,useRef } = owl;
import { BrEmojisDropdown,BrChildEmojisDropdown } from "@sh_br_engaging/js/emojis_dropdown";
import { HighFiveDescPanel } from './br_high_five_description';
import { ListRenderer } from '@web/views/list/list_renderer';


export class HighFivesController extends ListController {
  setup() {
    super.setup();
    // Realtime Update Code 
    this.busService = this.env.services.bus_service;
    this.showingList = false;

    // CUSTOM CODE 
    // ==============================
    this.state = useState({
      infos: {
        'sh_all_high_five_data':[],
        'group_by_high_five_list_data':[],
        'final_group_by_dict':{},
        'is_group_by_enable':false,
      },
    });

    onWillStart(this.willStart);
    onWillUpdateProps(this.willUpdate);

    this.user_id = session.uid;
    onMounted(this.onMounted);

    // onWillRender(() => {

    // });

    // onRendered(() => {

    // });

  }

  async willStart() {
     var self = this;
     await self.renderData(this)
  }

  willUpdate(nextProps) {
    this.state.infos.domain = nextProps.domain
    this.renderData(nextProps)
  }

  async renderData(nextProps) {
       var self = this
      // ---------------------- Realtime Update Code -----------------
      this.busService.addEventListener(
        "notification",
        ({ detail: notifications }) => {
          for (var i = 0; i < notifications.length; i++) {
            var channel = notifications[i]["type"];
            if (channel == "new.high_five") {
              if ($('.sh_high_five_custom_class').length) {
                this.actionService.switchView("list");
              }
              else{
                console.log("\n New High Five Created");
              }
            }
          }
        }
      );
      // -------------------------- Realtime Update Code ------------------------------- 
      let result = await ajax.jsonRpc("/get/high_five/data", "call",{
        'domain':  nextProps.domain,
        'groupBy':  nextProps.groupBy
      });

      // testing
      this.state.infos.sh_all_high_five_data = result["all_high_five_records"];
      this.state.infos.group_by_high_five_list_data = result["group_by_high_five_list"];
      this.state.infos.is_group_by_enable = result["is_group_by_enable"];
      this.state.infos.final_group_by_dict = result["final_group_by_dict"];


      // testing
      // this.all_high_fives = result["all_high_five_records"];
      this.login_user_id = result["login_user_id"];
      this.login_user_name = result["login_user_name"];
      this.today_date_in_string_format = result["today_date_in_string_format"];
      this.sh_given_high_five_count = result["given_high_five_count"];
      this.total_points_of_given_high_five = result["total_points_of_given_high_five"];
      this.sh_received_high_five_count = result["received_high_five_count"];
      this.total_points_of_received_high_five = result["total_points_of_received_high_five"];
      this.total_points = result["sum_of_given_received_high_five_points"];
      this.badge_all_list = result["badge_all_list"];
      // ** Top Users Details **
      // ** First ** 
      this.first_top_user_id = result["first_top_high_fiver_id"];
      this.first_top_user = result["first_top_high_fiver_name"];
      this.first_top_counts = result["top_first_high_fiver_count"];
      // ** Second ** 
      this.second_top_user_id = result["second_top_high_fiver_id"];
      this.second_top_user = result["second_top_high_fiver_name"];
      this.second_top_counts = result["top_second_high_fiver_count"];
      // ** Third ** 
      this.third_top_user_id = result["third_top_high_fiver_id"];
      this.third_top_user = result["third_top_high_fiver_name"];
      this.third_top_counts = result["top_third_high_fiver_count"];
      // ** Fourth ** 
      this.fourth_top_user_id = result["fourth_top_high_fiver_id"];
      this.fourth_top_user = result["fourth_top_high_fiver_name"];
      this.fourth_top_counts = result["top_fourth_high_fiver_count"];
      // ** Fifth ** 
      this.fifth_top_user_id = result["fifth_top_high_fiver_id"];
      this.fifth_top_user = result["fifth_top_high_fiver_name"];
      this.fifth_top_counts = result["top_fifth_high_fiver_count"];
      // ** Group By Date Functionality **
      // this.group_by_high_five_list = result["group_by_high_five_list"];

      this.user_id = session.uid;

  }

  // onMounted() {
  //   // CODE TO HIGHLIGHT BADGES
  //   $('p.massage_reply_user_extra_text_name.mb-0').each(function() {
  //     // Get the text content of the paragraph
  //     var text = $(this).text();
    
  //     // Check if the text contains a hashtag
  //     if (text.includes('#')) {
  //       // Use a regular expression to find and highlight the badge
  //       var highlightedText = text.replace(/(#\S+)/g, '<span style="color: red;">$1</span>');
    
  //       // Replace the original text with the highlighted version
  //       console.log("\n\n\n\n\n\n highlightedText", highlightedText);
  //       $(this).html(highlightedText);
  //     }


  //   // CODE TO BOLD EMPLOYEE
  //    // Find The Closest P Tag Code
  //    var sh_received_emp_name = $(this).closest(".massage_reply_user_extra_text").find(".sh_bold_parent_employee").text();
  //    console.log("\n\n\n\n\n\n sh_received_emp_name", highlightedText);

  //    if (text.includes(sh_received_emp_name)) {
  //     var boldEmployeeName = text.replace(sh_received_emp_name, '<span style="font-weight: bold;">'+sh_received_emp_name+'</span>');
  //     $(this).html(boldEmployeeName);
      
  //    } 
  //   });
  // }

  onMounted() {
    // CODE TO HIGHLIGHT BADGES AND BOLD EMPLOYEE

    // $('p.massage_reply_user_extra_text_name.mb-0').each(function() {
    //   // Get the text content of the paragraph
    //   var text = $(this).text();
  
    //   // Initialize a variable to store the modified text
    //   var modifiedText = text;
  
    //   // Check if the text contains a hashtag
    //   if (text.includes('#')) {
    //     // Use a regular expression to find and highlight the badge
    //     modifiedText = modifiedText.replace(/(#\S+)/g, '<span style="color: red;">$1</span>');
    //   }
  
    //   // Find the employee name
    //   var sh_received_emp_name = $(this).closest(".massage_reply_user_extra_text").find(".sh_bold_parent_employee").text();
  
    //   // Check if the text contains the employee name
    //   if (text.includes(sh_received_emp_name)) {
    //     // Use a regular expression to find and bold the employee name
    //     modifiedText = modifiedText.replace(new RegExp(sh_received_emp_name, 'g'), '<span style="font-weight: bold;">'+sh_received_emp_name+'</span>');
    //   }
  
    //   // Apply the modified text
    //   $(this).html(modifiedText);
    // });


    // CODE TO HIGHLIGHT BADGES AND BOLD EMPLOYEE OF CHILD
    $('p.child_massage_reply_user_extra_text_name').each(function() {
      // Get the text content of the paragraph
      var text = $(this).text();  
      // Find the employee name
      var sh_child_received_emp_name = $(this).closest(".massage_replay_text").find(".sh_bold_child_employee").text();
  
      // Check if the text contains the employee name
      if (text.includes(sh_child_received_emp_name)) {
        // Use a regular expression to find and bold the employee name
        var modifiedText = text.replace(new RegExp(sh_child_received_emp_name, 'g'), '<span style="font-weight: bold;">'+sh_child_received_emp_name+'</span>');
      }
  
      // Apply the modified text
      $(this).html(modifiedText);
    });
  }

  onClickHighFive() {
    var high_five_value = $(".sh_hive_five_input").val();
    var to_user_id = $(".sh_hive_five_input").attr("id")
    var sh_manage_badge_id = $(".sh_hive_five_input").attr("badge_id")
    ajax.jsonRpc("/post/high_five/data", "call", {
      high_five_text: high_five_value,
      to_user_id: to_user_id,
      sh_manage_badge_id: sh_manage_badge_id,
    });
    this.actionService.switchView("list");
  }

  
  CreateReplyHighFi(highfi_id, ev){
    const inputText = $("#reply_input_id_"+highfi_id).val();
    if (!inputText){
      $('.comment_validation').removeClass('d-none');

    }
    else{

    // == Code to find the private comment value 
    let closestPrivateCmtBoolean = $(ev.target).closest(".massage_item").find(".sh_private_cmt_boolean")
    var private_cmt_boolean_value = closestPrivateCmtBoolean.prop('checked')
    // === 
    var reply_input_id = '#reply_input_id_' + highfi_id;
    var high_five_reply = $(reply_input_id).val();

    var user_id=0
    if ($('.sh_hive_five_child_input').attr('user_id')){
      user_id = $('.sh_hive_five_child_input').attr('user_id')

    }

    ajax.jsonRpc("/post/high_five/comments", "call", {
      high_five_reply_id: highfi_id,
      high_five_reply: high_five_reply,
      private_cmt_boolean_value: private_cmt_boolean_value,
      third_person_id: user_id,
    });
    this.actionService.switchView("list");
  }

  }


  fetchBadgeList(search) {

    // console.log('========> fetchBadgeList')
      
    ajax.jsonRpc("/get/badge/list", "call",{
      limit:8,
      search:search,
    })
    .then(badge_list => {
      const badgelist = $("#badge_list");
      badgelist.empty()

    //   for (var i = 0; i < badge_list.length; i++) {
    //     const listItem = $("<li>").text(badge_list[1]);
    //     listItem.addClass("badge-item dropdown-item d-flex w-100 py-2 px-4");
    //     if (i==0){
    //       listItem.addClass("active bg-300");
    //     }
    //     console.log('listItem ==>',listItem)
    //     badgelist.append(listItem);
    // }

      var firstKey;
      for (var key in badge_list) {
        if (badge_list.hasOwnProperty(key)) {
          var value = badge_list[key];
          const listItem = $("<li>").text(value);
          listItem.addClass("badge-item dropdown-item d-flex w-100 py-2 px-4");
          listItem.attr('badge_id', key);

          if (!firstKey) {
            firstKey = key;
            listItem.addClass("active bg-300");
          }
          badgelist.append(listItem);
        }
      }

      // ADD SEARCH MORE OPTION TO SHOW ALL BADGES
      // =========================================
      const searchMoreItem = $("<li>").text("Search More...");
      searchMoreItem.addClass("badge-item-search-more badge-item dropdown-item text-primary d-flex w-100 py-2 px-4");
      searchMoreItem.on("click", () => this.onSearchMoreClick());
      badgelist.append(searchMoreItem);
      // =========================================
      

      // Add event listeners for click and hover
      $(".badge-item").on("click", (event) => this.handleItemClick(event,"badge-item"));
      $(".badge-item").hover(
          (event) => this.handleItemHover(event,"badge-item"),
          () => this.handleItemHoverOut("badge-item")
      );
  })
  }

  fetchUserList(search) {
    ajax.jsonRpc("/get/user/list", "call",{
      limit:8,
      search:search,
    })
    .then(users_name_list => {
      const employeeList = $("#employee_list");
      employeeList.empty()
      for (var i in users_name_list) {
        const listItem = $("<li>").text(users_name_list[i].name);

        listItem.addClass("user-item dropdown-item d-flex w-100 py-2 px-4");  
        listItem.attr("id", users_name_list[i].id);
        if (i==0){
          listItem.addClass("active bg-300");
        }
        employeeList.append(listItem);
        
      }
      

       // Add event listeners for click and hover FOR HIFI ONLY
       $(".user-item").on("click", (event) => this.handleItemClick(event,"user-item"));
       $(".user-item").hover(
           (event) => this.handleItemHover(event,"user-item"),
           () => this.handleItemHoverOut("user-item")
       );
      // FOR REPLY COMEENT USER LIST
      // ==========================
      
      // const employeeListReply = $("#employee_list_reply");
      // employeeListReply.empty()
      // for (var i in users_name_list) {
      //   const listItem = $("<li>").text(users_name_list[i].name);

      //   listItem.addClass("user-item-reply");  
      //   listItem.attr("id", users_name_list[i].id);
      //   if (i==0){
      //     listItem.addClass("active");
      //   }
      //   employeeListReply.append(listItem);

      // }
      // $(".user-item-reply").hover(
      //   (event) => this.handleItemHover(event,"user-item-reply"),
      //   () => this.handleItemHoverOut("user-item-reply")
      // );
      // $(".user-item-reply").on("click", (event) => this.handleItemClickReply(event,"user-item"));

      // =================================


     
  })
  }

// FOR OPEN ALL BADGES SELECTION MODEL
// ===================================
onSearchMoreClick(badge_all_list){
  $("#SelectBadgesModel").modal("show");
}


// FROM SEARCH MORE BADGE SELECTION CLICK EVENT
// ============================================
SelectFromAllBadges(event,badge_id){
  const inputText = $(".sh_hive_five_input").val();
  const symbolIndex = inputText.lastIndexOf('#');
  const userInputBeforeAt = inputText.substring(0, symbolIndex + 1);
  $(".sh_hive_five_input").val(userInputBeforeAt + this.badge_all_list[badge_id] + ' ');

  $(".sh_hive_five_input").attr("badge_id",badge_id);

  $("#SelectBadgesModel").modal("hide");
  this.hideList('badge-item');
}


handleItemClick(event,itemClass) {

    event.preventDefault();
    const selectedItem = $(event.currentTarget).text();
    const inputText = $(".sh_hive_five_input").val();


    // HIGH FIVE BUTTON DISABLED CODE HERE
    // ====================================
    const hasHashSymbol = inputText.includes('#');
    const hasUserSymbol = inputText.includes('@');
    $('.sh_high_five_btn').addClass('disabled');
    if (hasHashSymbol && hasUserSymbol) {
        $('.sh_high_five_btn').removeClass('disabled');
    }
    else{
      $('.sh_high_five_btn').addClass('disabled');

    }
    // =====================================


    const symbol = itemClass === "user-item" ? "@" : "#";
    const symbolIndex = inputText.lastIndexOf(symbol);
    const userInputBeforeAt = inputText.substring(0, symbolIndex + 1);
    $(".sh_hive_five_input").val(userInputBeforeAt + selectedItem + ' ');
    $(".sh_hive_five_input").focus();
    $(".sh_hive_five_input").attr("id",$(event.currentTarget).attr("id"));
    
    if (itemClass=='badge-item'){
      $(".sh_hive_five_input").attr("badge_id",$(event.currentTarget).attr("badge_id"));
    }
    this.hideList(itemClass);
}


handleItemHoverOut(itemClass) {
    $(`.${itemClass}`).removeClass("hovered");
}

handleItemHover(event, itemClass) {
  $(event.currentTarget).addClass("hovered");
}


hideList(itemClass) {

    // for hide main UL 
    $(`.${itemClass+'-ul'}`).addClass("d-none");

    // for hide li items
    $(`.${itemClass}`).addClass("d-none");

    if(itemClass=='badge-item'){
      this.showingBadgeList = false;
      this.hashtagTyped = false;

    }

    if(itemClass=='user-item'){
      this.showingList = false;
      this.atTyped = false;

    }
}

highFiveKeyPress(event) {

    const inputText = $(".sh_hive_five_input").val();
    const employeeList = $("#employee_list");
    const badgelist = $("#badge_list");

    
    // HIGH FIVE BUTTON DISABLED CODE HERE
    // ====================================
    const hasHashSymbol = inputText.includes('#');
    const hasUserSymbol = inputText.includes('@');

    $('.sh_high_five_btn').addClass('disabled');
    if (hasHashSymbol && hasUserSymbol) {
        $('.sh_high_five_btn').removeClass('disabled');
    }
    else{
      $('.sh_high_five_btn').addClass('disabled');

    }
    // =====================================


    // for hide user list when remove @ in text box
    // =============================================
    var  atCount = (inputText.match(/@/g) || []).length;
    var  HashCount = (inputText.match(/#/g) || []).length;

    if (event.key === "Backspace" && inputText.endsWith('@') && atCount >=1) {
      this.showingList = false;
      employeeList.addClass("d-none");
      this.atTyped = false;
    }
    // =============================================


    if (event.key === "Backspace" && inputText=='@') {
        this.showingList = false;
        employeeList.addClass("d-none");
        this.atTyped = false;

    }

    if (event.key === "@") {

        const atIndex = $(".sh_hive_five_input").val().lastIndexOf('@');
        const spaceAfterAt = atIndex !== -1 && $(".sh_hive_five_input").val()[atIndex + 1] === ' ';

        if (!this.atTyped && (atIndex === -1 || spaceAfterAt) && atCount==0){
        // if (!this.atTyped && (atIndex === -1 || spaceAfterAt)){
            employeeList.removeClass("d-none");
            this.showingList = true;
            this.atTyped = true;
            this.fetchUserList(false)

          // Hide the badge list if '#' was typed just before '@'
          if (this.hashTyped) {
            badgelist.addClass("d-none");
            this.showingBadgeList = false;
            }

        } else if (this.atTyped && event.key === "@") {
          // Hide the user list if '@' is typed again
          employeeList.addClass("d-none");
          this.showingList = false;
          this.atTyped = false;
      }


    } else if (event.key === "#") {

        const atIndex = inputText.lastIndexOf('#');
        const spaceAfterHash = atIndex !== -1 && inputText[atIndex + 1] === ' ';

        if ((!this.hashtagTyped || spaceAfterHash || atIndex === -1) && HashCount==0) {
          // if (!this.hashtagTyped || spaceAfterHash) {
          // if (!this.hashtagTyped && (atIndex === -1 || spaceAfterHash)) {
            badgelist.removeClass("d-none");
            this.showingBadgeList = true;
            this.hashtagTyped = true;
            this.fetchBadgeList(false);

            // Hide the badge list if '@' was typed just before '#'
            if (this.atTyped) {
              employeeList.addClass("d-none");
              this.showingList = false;
          }

        }
        
        if (event.key === "Backspace") {
          this.hashtagTyped = false;
        }
        
    } else if (this.showingList) {

        // issue is here
        if (event.key != "ArrowUp" &&  event.key != "ArrowDown" && event.key !='Enter'){

          // for search from user name
          const atIndex = inputText.lastIndexOf('@');
          const searchQuery = atIndex !== -1 ? inputText.slice(atIndex + 1) : "";
          // ===========================

          // this.fetchUserList(inputText.replace("@", ""))
          this.fetchUserList(searchQuery)
        }

        if (event.key === "Shift") {
            event.preventDefault();
        }
        else if (event.key === "Enter" || inputText.length === 0) {

          this.handleEnterKeyPress("user-item");

        } else if (event.key === "ArrowUp") {
          this.handleArrowUpKeyPress("user-item");
        } else if (event.key === "ArrowDown") {

            this.handleArrowDownKeyPress("user-item");

        } else {

          const atIndex = inputText.lastIndexOf('@');
          const spaceAfterAt = atIndex !== -1 && inputText[atIndex + 1] === ' ';
  
          if (spaceAfterAt) {
              const searchQuery = inputText.slice(atIndex + 2);
              this.fetchUserList(searchQuery)

          }
      }
    }

    else if (this.showingBadgeList) {

      // console.log('======== TARGET HERE ')

      if (event.key === "Backspace" && inputText.length === 1) {
        this.hideList("badge-item");
        this.hashtagTyped = false; // Reset the hashtagTyped flag when Backspace is pressed
      }
      
      else if (event.key != "ArrowUp" && event.key != "ArrowDown" && event.key !='Enter'){
        // this.fetchBadgeList(inputText.replace("#", ""));
        const hashtagIndex = inputText.lastIndexOf('#');
        if (hashtagIndex !== -1) {
            const searchQuery = inputText.slice(hashtagIndex + 1);
            this.fetchBadgeList(searchQuery);
        }

      }
      else if (event.key === "Shift") {
          event.preventDefault();
      } else if (event.key === "Enter" || inputText.length === 0) {
          this.handleEnterKeyPress("badge-item");

      } else if (event.key === "ArrowUp") {
        this.handleArrowUpKeyPress("badge-item");
      } else if (event.key === "ArrowDown") {
          this.handleArrowDownKeyPress("badge-item");
      } else {

        // console.log('==== elseeee')
          // Handle other key events specific to badge list if needed

        const atIndex = inputText.lastIndexOf('#');
        const spaceAfterAt = atIndex !== -1 && inputText[atIndex + 1] === ' ';

        if (spaceAfterAt) {
            const searchQuery = inputText.slice(atIndex + 2);
            this.fetchBadgeList(searchQuery)

        }
      }
  }
}

handleEnterKeyPress(itemClass) {
  const activeSelection = $(`.${itemClass}.active`);

  // FOR OPEN SEARCH MORE MODEL IF SEARCH MORE BY DOWN UP KEY
  // ========================================================
  if (activeSelection.hasClass('badge-item-search-more')){
    $("#SelectBadgesModel").modal("show");
  }

  else if (activeSelection.length > 0) {
        const symbol = itemClass === "user-item" ? "@" : "#";
        const atIndex = $(".sh_hive_five_input").val().lastIndexOf(symbol);
        const userInputBeforeSymbol = $(".sh_hive_five_input").val().substring(0, atIndex + 1);

        $(".sh_hive_five_input").val(userInputBeforeSymbol + activeSelection.text() + ' ');
        // to add active user id in input text
        $(".sh_hive_five_input").attr("id",activeSelection.attr('id'));

        // for enter badge id to store badge id in high five
        if (itemClass=='badge-item'){
          $(".sh_hive_five_input").attr("badge_id",activeSelection.attr('badge_id'));
        }


        activeSelection.removeClass("active");
    }
    this.hideList(itemClass);
}

handleArrowUpKeyPress(itemClass) {
  const currentSelection = $(`.${itemClass}.active`);
  const allItems = $(`.${itemClass}`);

  if (currentSelection.length > 0) {
      const prevSelection = currentSelection.prev(`.${itemClass}`);
      if (prevSelection.length > 0) {
            currentSelection.removeClass("active bg-300");
            prevSelection.addClass("active bg-300");
        }
        else {
          // If the current selection is the first item, select the last item
          currentSelection.removeClass("active bg-300");
          allItems.last().addClass("active bg-300");
        }
  } else {
      // $(`.${itemClass}:last`).addClass("active bg-300");
      allItems.last().addClass("active bg-300");
  }

  }

handleArrowDownKeyPress(itemClass) {
  const currentSelection = $(`.${itemClass}.active`);
  const allItems = $(`.${itemClass}`);

  if (currentSelection.length > 0) {
      const nextSelection = currentSelection.next(`.${itemClass}`);
      if (nextSelection.length > 0) {
          currentSelection.removeClass("active bg-300");
          nextSelection.addClass("active bg-300");
      }
      else {
        // If the current selection is the last item, select the first item
        currentSelection.removeClass("active bg-300");
        allItems.first().addClass("active bg-300");
      }
  } else {
      // $(`.${itemClass}:first`).addClass("active bg-300");
      allItems.first().addClass("active bg-300");
  }

}


// required 
highFiveKeyUp(event) {

    const employeeList = $("#employee_list");
    const inputText = $(".sh_hive_five_input").val();

    var  atCount = (inputText.match(/@/g) || []).length;
    if (event.key === "Backspace" && inputText.endsWith('@') && atCount<=1){
      this.showingList = true;
      this.atTyped = true;
      this.fetchUserList(false)
      employeeList.removeClass("d-none");
    }

}

// CommentCurrentHifi(reply_id){

//   // add this line to first hide all sub reply box to fix show multiple reply boxes
//   $('.message_sub_replay_box').addClass('d-none')

//   var dynamicIdSelector = '#reply_id_' + reply_id;
//   // ** Find The Child Input And Add Focus ** 
//   var child_input = $(dynamicIdSelector).find('.sh_hive_five_child_input');
//   $(dynamicIdSelector).removeClass('d-none')
//   child_input.focus();
// }

CommentCurrentHifi(reply_id) {
  // Find the dynamicIdSelector
  var dynamicIdSelector = '#reply_id_' + reply_id;

  // Check if the element is currently visible
  var isVisible = $(dynamicIdSelector).is(':visible');

  // Hide all sub reply boxes
  $('.message_sub_replay_box').addClass('d-none');

  // Toggle the visibility of the dynamicIdSelector element
  if (!isVisible) {
      // If it's not visible, show it and set focus
      $(dynamicIdSelector).removeClass('d-none');
      $(dynamicIdSelector).find('.sh_hive_five_child_input').focus();
  } else {
      // If it's visible, hide it
      $(dynamicIdSelector).addClass('d-none');
  }
}



// =============================================================
// ****** COMMENT REPLY EMPLOYEE SELECTION CODE HERE ********
// =============================================================


fetchUserListReply(search,reply_input_id) {

  ajax.jsonRpc("/get/user/list", "call",{
    limit:8,
    search:search,
  })
  .then(users_name_list => {

    // FOR REPLY COMEENT USER LIST
    // ==========================

    const employeeListReply = $(".select_employee_list_ul#"+reply_input_id);

    employeeListReply.empty()
    for (var i in users_name_list) {
      const listItem = $("<li>").text(users_name_list[i].name);

      listItem.addClass("user-item-reply dropdown-item d-flex w-100 py-2 px-4 ");  
      listItem.attr("id", users_name_list[i].id);
      if (i==0){
        listItem.addClass("active bg-300");
      }
      employeeListReply.append(listItem);

    }
    $(".user-item-reply").hover(
      (event) => this.handleItemHover(event,"user-item-reply"),
      () => this.handleItemHoverOut("user-item-reply")
    );
    $(".user-item-reply").on("click", (event) => this.handleItemClickReply(event,"user-item"));

    // =================================

})
}

handleEnterKeyPressReply(event){
  const activeSelection = $(`.user-item-reply.active`);
  const selectedItem = $(event.currentTarget);


  if (activeSelection.length > 0) {
      selectedItem.val('@' + activeSelection.text().trim());
      activeSelection.removeClass("active");
  }
  this.hideList('user-item-reply');

  // add user id
  $(".sh_hive_five_child_input").attr("user_id",activeSelection.attr('id'));

}


handleItemClickReply(event,itemClass) {

  event.preventDefault();
  const selectedItem = $(event.currentTarget);
  let id = selectedItem.attr('id')
  let neww = selectedItem.closest('.message_sub_replay_main')
  let current_input = neww.find('.sh_hive_five_child_input')

  const atIndex = current_input.val().lastIndexOf('@');
  const userInputBeforeSymbol = current_input.val().substring(0, atIndex + 1);
  current_input.val(userInputBeforeSymbol + selectedItem.text().trim() + ' ');

  // add user id
  $(".sh_hive_five_child_input").attr("user_id",selectedItem.attr('id'));
  this.hideList('user-item-reply');

}

highFiveKeyUpReply(id,event) {
  const inputText = $("#"+id).val();

    // COMMENT BUTTON DISABLED CODE HERE
    // ====================================
    
    // $('.comment_validation').addClass('d-none');

    // if (inputText) {
    //   $('.comment_validation').addClass('d-none');
    // }
    // else{
    //   $('.comment_validation').removeClass('d-none');
    // }
    // =====================================
}

highFiveKeyPressReply(id,event){

  const inputText = $("#"+id).val();
  const employeeListReply = $(".select_employee_list_ul#"+id);

  if (event.key === "Backspace" && inputText=='@') {
    this.showingReplyList = false;
    employeeListReply.addClass("d-none");
    this.atREplyTyped = false;

  }
  if (event.key === "@") {
      const atIndex = inputText.lastIndexOf('@');
      const spaceAfterAt = atIndex !== -1 && inputText[atIndex + 1] === ' ';
      if (!this.atREplyTyped){
      // if (!this.atREplyTyped && (atIndex === -1 || spaceAfterAt)){
        employeeListReply.removeClass("d-none");
          this.showingReplyList = true;
          this.atREplyTyped = true;
          this.fetchUserListReply(false,id)
    } 
  }
  else if (this.showingReplyList) {

    // issue is here
    if (event.key != "ArrowUp" && event.key != "ArrowDown" && event.key !='Enter'){
      this.fetchUserListReply(inputText.replace("@", ""),id)
    }

    if (event.key === "Shift") {
        event.preventDefault();
    }
    else if (event.key === "Enter" || inputText.length === 0) {

      this.handleEnterKeyPressReply(event);

    } else if (event.key === "ArrowUp") {
      this.handleArrowUpKeyPress("user-item-reply");
    } else if (event.key === "ArrowDown") {

      this.handleArrowDownKeyPress("user-item-reply");
        

    } else {

      const atIndex = inputText.lastIndexOf('@');
      const spaceAfterAt = atIndex !== -1 && inputText[atIndex + 1] === ' ';

      if (spaceAfterAt) {
          const searchQuery = inputText.slice(atIndex + 2);
          this.fetchUserListReply(searchQuery,id)
      }
  }
}


}



// ==============================
// *** PARENT METHODS ***  
// ==============================

onClickLikeButton(ev) {
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
  ajax.jsonRpc("/post/like_btn/data", "call", {
    record_id: record_id,
  });
  current_element.addClass("d-none")
}

onClickUnlikeButton(ev) {
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
  ajax.jsonRpc("/post/unlike_btn/data", "call", {
    record_id: record_id,
  });
  find_current_element.addClass("d-none")
}

onClickDeleteButton(ev) {
  // == Find the record Id == 
  var closest_main_div = $(ev.target).closest('.massage_item')
  closest_main_div.addClass("d-none")
  var record_id = closest_main_div.data('id')
  ajax.jsonRpc("/post/delete_btn/data", "call", {
    record_id: record_id,
  });
}

// ==============================
// *** CHILD METHODS ***  
// ==============================

onClickChildLikeButton(ev) {
  var closestUnlike = $(ev.target).closest(".child_kanban_user_item").find("#child_unlike_button")
  var current_element = $(ev.target).closest(".child_kanban_user_item").find("#child_like_button")
  var count_element = $(ev.target).closest(".child_kanban_user_item").find("#child_like_count");
  var like_counts = count_element.text()
  var convert_into_int = parseInt(like_counts)
  var updated_likes_count = convert_into_int+1
  count_element.text(updated_likes_count)

  closestUnlike.removeClass("d-none")
  var closest_main_div = $(ev.target).closest('.child_kanban_user_item')
  var record_id = closest_main_div.data('id')
  ajax.jsonRpc("/post/like/child/data", "call", {
    record_id: record_id,
  });
  current_element.addClass("d-none")
}

onClickChildUnlikeButton(ev) {
  var count_element = $(ev.target).closest(".child_kanban_user_item").find("#child_like_count");
  var like_counts = count_element.text()
  var convert_into_int = parseInt(like_counts)
  var updated_likes_count = convert_into_int-1
  count_element.text(updated_likes_count)

  var closestUnlike = $(ev.target).closest(".child_kanban_user_item").find("#child_like_button")
  var find_current_element = $(ev.target).closest(".child_kanban_user_item").find("#child_unlike_button")
  closestUnlike.removeClass("d-none")
  var closest_main_div = $(ev.target).closest('.child_kanban_user_item')
  var record_id = closest_main_div.data('id')
  ajax.jsonRpc("/post/unlike/child/data", "call", {
    record_id: record_id,
  });
  find_current_element.addClass("d-none")
}

OnChildDelete(ev) {
  // == Find the id of child record == 
  var closest_main_child_div = $(ev.target).closest('.child_kanban_user_item')
  var child_record_id = closest_main_child_div.data('id')
  closest_main_child_div.addClass("d-none")
  ajax.jsonRpc("/post/delete_btn/data", "call", {
    record_id: child_record_id,
  });

}


OnClickChildEdit(ev) {
  // === Find the Text That Already Written In Record ===
  var old_ans_element = $(ev.target).closest('.child_kanban_user_item').find(".child_massage_reply_user_extra_text_name")
  var vaue_of_p = old_ans_element.text();
  old_ans_element.addClass("d-none")
  // === Find Input Element For Edit === 
  var main_input_div = $(ev.target).closest('.child_kanban_user_item').find(".sh_high_five_dynamic_nested_kanban_text");
  main_input_div.removeClass("d-none")
  var child_input_element = $(ev.target).closest('.child_kanban_user_item').find(".sh_high_five_edit_input");
  child_input_element.focus();
  child_input_element.val(vaue_of_p)
  // === Hide Current Element ===
  $(ev.target).hide();
}


onClickHighfivePost(ev) {
  // == Find The Input Element And Value Of Input ==
  var child_input_element = $(ev.target).closest('.child_kanban_user_item').find(".sh_high_five_edit_input");
  // var input_element_value = child_input_element.val();
  // == Find The Id Of Current Child Record ==
  var closest_main_child_div = $(ev.target).closest('.child_kanban_user_item')
  var child_record_id = closest_main_child_div.data('id')

  // == Find The P Element And Update The Value Of That Element == 
  var old_ans_element = $(ev.target).closest('.child_kanban_user_item').find(".child_massage_reply_user_extra_text_name")
  old_ans_element.text(child_input_element.val())
  old_ans_element.removeClass("d-none")

  // == Hide Input And Post Button ==  
  var main_input_div = $(ev.target).closest('.child_kanban_user_item').find(".sh_high_five_dynamic_nested_kanban_text");
  main_input_div.addClass("d-none")

  // == Find The Pencil Icon And Show Pencil Icon == 
  var pencil_icon = $(ev.target).closest('.child_kanban_user_item').find(".sh_pencil_icon");
  pencil_icon.show();

  // == Pass The Data Into Controller == 
  ajax.jsonRpc("/edit/child/high_five/post", "call", {
    record_id: child_record_id,
    record_value : child_input_element.val(),
  });
}

}

HighFivesController.template = "sh_high_five_template";
// HighFivesController.components = { BrEmojisDropdown };
HighFivesController.components = {
  ...HighFivesController.components,
  HighFiveDescPanel,
  BrEmojisDropdown,BrChildEmojisDropdown,
};

export const BrHighFives = {
  ...listView,
  Controller: HighFivesController,
};

registry.category("views").add("br_engage_high_five_class", BrHighFives);
