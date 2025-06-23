/** @odoo-module **/

import { _t } from 'web.core';
import { qweb as QWeb } from 'web.core';
import { SlideCoursePage } from '@website_slides/js/slides_course_page';


SlideCoursePage.include({
    /**
     * Greens up the bullet when the slide is completed
     *
     * @public
     * @param {Object} slide
     * @param {Boolean} completed
     */

    toggleCompletionButton: function (slide, completed = true) {
        const $button = this.$(`.o_wslides_sidebar_done_button[data-id="${slide.id}"]`);

        if (!$button.length) {
            return;
        }

        const newButton = QWeb.render('website.slides.sidebar.done.button', {
            slideId: slide.id,
            slideCompleted: completed,
            canSelfMarkUncompleted: slide.canSelfMarkUncompleted,
            canSelfMarkCompleted: slide.canSelfMarkCompleted,
            isMember: slide.isMember,
            isTincan:slide.is_tincan,
            category: slide.category,
            isTimer: slide.isTimer,
            isSequential: slide.isSequential,
            hasNext : 1
        });
        $button.replaceWith(newButton);
        var slide_normal = this.$('.o_wslides_lesson_aside_list_link .o_wslides_sidebar_done_button');
        if (slide_normal.length != 0){
            if (completed == false && slide.is_timer){
                this.$('.o_wslides_lesson_aside_list_link.active .o_wslides_button_complete').addClass('disabled');
            }
        }
    },

    /*When view is normal and slide category is scorm and tincan type
    *To check if passed/failed and then complete the slide, increase the progress bar
    *else, send warning
    */ 
    _onClickComplete: function (ev) {
        ev.stopPropagation();
        ev.preventDefault();
        const $normal_view = $(ev.currentTarget).closest('.o_wslides_lesson_aside_list_link .o_wslides_sidebar_done_button');
        const $button_pro = $(ev.currentTarget).closest('.o_wslides_sidebar_done_button');
        const slide = $button_pro.data();
        const isCompleted = Boolean(slide.completed);
        if ($normal_view.length != 0){
            if(slide.category == 'scorm' && slide.is_tincan){ 
                if (!isCompleted){
                    this.ScormComplete({'slideId':slide.id});
                    // if (!(slide.completed)){
                    //     this._alertShow('slide_tincan_incomplete');
                    // }
                }
                if (isCompleted){
                    if (slide.is_timer && isCompleted){
                        if (!window.timer){
                            window.timer = new WebsiteSlidesCourseTimer();
                        }
                        window.timer.start();
                        } else{
                            if (window.timer){
                                clearTimeout(window.timer.timeout);
                                document.getElementById("hours").innerHTML = ""
                                document.getElementById("mins").innerHTML = ""
                                document.getElementById("secs").innerHTML = ""
                            }
                    }
                    this._super.apply(this, arguments);
                    this.$('.o_wslides_lesson_aside_list_link.active .o_wslides_button_complete').addClass('disabled');
                }
            }
            else {
                if (isCompleted && slide.is_timer) {
                    if (slide.is_timer && isCompleted){
                        if (!window.timer){
                            window.timer = new WebsiteSlidesCourseTimer();
                        }
                        window.timer.start();
                        } else{
                            if (window.timer){
                                clearTimeout(window.timer.timeout);
                                document.getElementById("hours").innerHTML = ""
                                document.getElementById("mins").innerHTML = ""
                                document.getElementById("secs").innerHTML = ""
                            }
                    }
                    if (slide.is_sequential){
                        this.$('.o_wslides_nav_button.btn.btn-light.border').addClass('disabled');
                    }
                    this._super.apply(this, arguments);
                    this.$('.o_wslides_lesson_aside_list_link.active .o_wslides_button_complete').addClass('disabled');
                }
                else {
                    if(!isCompleted && slide.is_timer && slide.is_sequential){
                        this.$('.o_wslides_nav_button.btn.btn-light.disabled').removeClass('disabled');
                    }
                    this._super.apply(this, arguments);
                }
            }
        }
        else {
            this._super.apply(this, arguments);
        }
    },

    _alertShow: function (alertCode) {
        var message = _t('There was an error validating this slide.');
        if (alertCode === 'slide_tincan_incomplete') {
            message = _t('You need to attempt current content to the end to mark it as done!');
        } else {
            message = _t('This slide is already completed');
        }
        this.displayNotification({
            type: 'warning',
            message: message,
            sticky: true
        });
    },

    /**
         * This method is called when slide type is scorm and scorm type is tincan
         * to complete the content based on result-passed/failed on fullscreen
         * @private
         * @param {Integer} slideId: the id of slide to set as completed
        */
    ScormComplete: function(slideId){
        var parent_this = this;
        const $slide = this.$(`.o_wslides_sidebar_done_button[data-id="${slideId.slideId}"]`);
        parent_this.slide = $slide.data();
        this._rpc({
            route: '/slides/slide/scorm_set_completed',
            params: {
                slide_id: slideId.slideId
            }
        })
        .then(function (data){
            if (data.result_passed || data.result_failed){
                parent_this._toggleSlideCompleted(parent_this.slide);
            }
            else{
                parent_this._alertShow('slide_tincan_incomplete');
            }
        });
    }
}); 