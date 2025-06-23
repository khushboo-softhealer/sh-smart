odoo.define('mx_elearning_pro.extended', function (require) {
    'use strict';

    var core = require('web.core');
    var config = require('web.config');
    var session =require('web.session');
    var _t = core._t;
    var QWeb = core.qweb;
    var rpc = require('web.rpc');
    var Fullscreen = require('@website_slides/js/slides_course_fullscreen_player')[Symbol.for("default")];
    var publicWidget = require('web.public.widget');

    var findSlide = function (slideList, matcher) {
        var slideMatch = _.matcher(matcher);
        return _.find(slideList, slideMatch);
    };

    /**
     * Returns a string representing a time value, from a float.  The idea is that
     * we sometimes want to display something like 1:45 instead of 1.75, or 0:15
     * instead of 0.25.
     *
     * @param {float} value
     * @param {Object} [field]
     *        a description of the field (note: this parameter is ignored)
     * @param {Object} [options]
     * @param {boolean} [options.noLeadingZeroHour] if true, format like 1:30
     *        otherwise, format like 01:30
     * @returns {string}
     */
    function formatFloatTime(value, field, options) {
        options = options || {};
        var pattern = options.noLeadingZeroHour ? '%1d:%02d' : '%02d:%02d';
        if (value < 0) {
            value = Math.abs(value);
            pattern = '-' + pattern;
        }
        var hour = Math.floor(value);
        var min = Math.round((value % 1) * 60);
        if (min === 60){
            min = 0;
            hour = hour + 1;
        }
        return _.str.sprintf(pattern, hour, min);
    }

    var WebsiteSlidesCourseTimer = publicWidget.Widget.extend({
        selector: '.o_wslides_js_course_timer',
        timeout: null,
        /**
         * @override
         * @param {Object} parent
         */
        //
        start: function () {
            var proms = [this._super.apply(this, arguments)];
            var sidebarItem = $('.o_wslides_fs_sidebar_list_item.active .o_wslides_fs_slide_name');
            if (sidebarItem.length == 0) {
                var sidebarItem = $('.o_wslides_lesson_aside_list_link.active');
            }
            var min_duration = sidebarItem.data().min_duration;
            if (min_duration){
                var time = min_duration;
            }else {
               var time = sidebarItem.data().duration
            }
            var duration = formatFloatTime(time);
            var hours = Number(duration.split(':')[0]);
            var min = Number(duration.split(':')[1]);
            var dt = new Date();
            dt.setHours(dt.getHours() + hours);
            dt.setMinutes(dt.getMinutes() + min);
            this.dt = dt;
            this.cdInterval;
            var self = this;
            var slide = $('.o_wslides_fs_sidebar_list_item.active .o_wslides_fs_slide_name');
            if (slide.length == 0){
                var slide = $('.o_wslides_lesson_aside_list_link.active');
            }
            this.slide = slide.data().slide
            // this.slide_type = slide.data().slide_type
            this.isQuiz = slide.data().isQuiz
            this.timeout = setTimeout(function(){
                self.startTimer();
            }, 1000)
            return Promise.all(proms);
        },
        startTimer: function(){
            var now = new Date().getTime();
            var timeleft = this.dt - now;
            // Calculating the days, hours, minutes and seconds left
            var hours = Math.floor((timeleft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            var minutes = Math.floor((timeleft % (1000 * 60 * 60)) / (1000 * 60));
            var seconds = Math.floor((timeleft % (1000 * 60)) / 1000);
            if (isNaN(hours)){
                document.getElementById("hours").innerHTML = ""
            }
            else {
                document.getElementById("hours").innerHTML = hours + "h "
            }
            if (isNaN(minutes)){
                document.getElementById("mins").innerHTML = ""
            }
            else if(minutes == undefined){
                document.getElementById("mins").innerHTML = ""
            }
            else {
                document.getElementById("mins").innerHTML = minutes + "m"
            }
            if (isNaN(seconds)){
                document.getElementById("secs").innerHTML = ""
            }
            else if (seconds == undefined){
                document.getElementById("secs").innerHTML = ""
            }
            else {
                
                document.getElementById("secs").innerHTML = seconds + "s "
            }
            var self = this;
            
            if (timeleft < 0) {
                $('.o_btn_wslides_set_done').removeClass('d-none')
                document.getElementById("hours").innerHTML = ""
                document.getElementById("mins").innerHTML = ""
                document.getElementById("secs").innerHTML = ""
                $('.o_wslides_lesson_aside_list_link.active .o_wslides_button_complete').removeAttr('disabled');
                $('.o_wslides_lesson_aside_list_link.active .o_wslides_button_complete').removeClass('disabled');
                var slide = $('.o_wslides_fs_sidebar_list_item.active');
                // if (slide.data().category == 'scorm' && slide.data().is_tincan){
                //     $('.o_wslides_fs_sidebar_list_item.active .o_wslides_button_complete').removeClass('disabled');
                //     $('.o_wslides_fs_sidebar_list_item.active .o_wslides_button_complete').removeAttr('disabled');
                // }
                if(slide.length != 0){
                    var hasQuestion = slide.data().hasQuestion;
                    var category = slide.data().category;
                    var hasNext = slide.data().hasNext;
                    var completed = slide.data().completed;
                    var is_tincan =  slide.data().is_tincan;
                }
                // if slide has no next slide
                if (!(hasNext)){
                    if (!(completed)){
                        // if (category == 'quiz' || (category == 'scorm' && is_tincan && !hasQuestion)){
                        if (category == 'quiz'){
                            $('.o_btn_set_done').addClass('d-none');
                            $('.o_btn_next_slide').addClass('d-none');
                        }
                        else if (hasQuestion){
                            $('.o_btn_set_done').addClass('d-none');
                            $('.o_btn_next_slide').removeClass('d-none');
                        }
                        else {
                            $('.o_btn_set_done').removeClass('d-none');
                            $('.o_btn_next_slide').addClass('d-none');
                        }
                    }
                    if (completed){
                        $('.o_btn_set_done').addClass('d-none');
                        $('.o_btn_next_slide').addClass('d-none');
                    }
                }
                else {
                    if (!completed){
                        // if ( hasQuestion || (category == 'scorm' && is_tincan && !hasQuestion)){
                        if (hasQuestion){
                            $('.o_btn_set_done').addClass('d-none');
                            $('.o_btn_next_slide').removeClass('d-none');
                        }
                        else if (category == 'quiz'){
                            $('.o_btn_set_done').addClass('d-none');
                            $('.o_btn_next_slide').addClass('d-none');
                        }
                        else {
                            $('.o_btn_set_done').removeClass('d-none');
                            $('.o_btn_next_slide').addClass('d-none');
                        }
                    }
                    if (completed){
                        if (category == 'quiz'){
                            $('.o_btn_set_done').addClass('d-none');
                            $('.o_btn_next_slide').addClass('d-none');
                        }
                        else{
                            $('.o_btn_set_done').addClass('d-none');
                            $('.o_btn_next_slide').removeClass('d-none');
                        }
                    }
                }
                var btn_done = $('.o_btn_done');
                if (category != 'quiz' && !self.isQuiz){
                    btn_done.removeClass('disabled');
                }
            }
            else{
                this.timeout = setTimeout(function(){
                    self.startTimer();
                }, 1000)
            }
        },
    });

    publicWidget.registry.websiteSlidesTimer = publicWidget.Widget.extend({
        selector: '.o_wslides_js_course_timer',
        start: function (){
            var self = this;
            var is_timer_tag = $('.o_wslides_lesson_aside_list_link.active ');
            var is_timer = false;
            if(is_timer_tag.length != 0){
                var is_timer = is_timer_tag.data().is_timer;
            }
            if (($('.o_wslides_lesson_aside_list_link.active .fa-check-circle').length == 0) && is_timer){
                if (!window.timer){
                    window.timer = new WebsiteSlidesCourseTimer();
                }
                window.timer.start();
            } else {
                if (window.timer){
                    clearTimeout(window.timer.timeout);
                    document.getElementById("hours").innerHTML = ""
                    document.getElementById("mins").innerHTML = ""
                    document.getElementById("secs").innerHTML = ""
                }
            }
        }
    });  

    Fullscreen.include({
        events: _.extend({}, Fullscreen.prototype.events, {
            'click .o_btn_set_done': '_onClickDone',
            'click .o_btn_next_slide': '_onClickCustomNext',
            'click .o_btn_comment_unable': '_onClickCommentUnable',
            'click .o_btn_comment_public': '_onClickCommentPublic',
            'click .o_btn_no_comment_karma': '_onClickNoCommentKarma',
            'click .o_btn_comment_karma': '_onClickCommentKarma',
        }),

        _onClickCommentUnable: function () {
            var message = ('Commenting is not enabled on this course.');
            this.displayNotification({
                type: 'warning',
                message: message,
                sticky: true
            });
        },

        _onClickCommentPublic: function () {
            var message = ('There are no comments for now. Join Course to be the first to leave a comment.');
            this.displayNotification({
                type: 'warning',
                message: message,
                sticky: true
            });
        },

        _onClickNoCommentKarma: function () {
            var message = ('There are no comments for now. Earn more Karma to be the first to leave a comment.');
            this.displayNotification({
                type: 'warning',
                message: message,
                sticky: true
            });
        },

        _onClickCommentKarma: function () {
            var message = ('Earn more Karma to leave a comment.');
            this.displayNotification({
                type: 'warning',
                message: message,
                sticky: true
            });
        },

        _renderSlide: function () {
            this._super.apply(this, arguments);
            var slide = this.get('slide');
            this._rpc({
                route: '/slides/slide/mx/like',
                params: {
                    slide_id: slide.id,
                },
            }).then(function (data) {
                if (! data.error) {
                    const $likesBtn = self.$('span.o_wslides_js_slide_like_up_mx');
                    const $likesIcon = $likesBtn.find('i.fa');
                    const $dislikesBtn = self.$('span.o_wslides_js_slide_like_down_mx');
                    const $dislikesIcon = $dislikesBtn.find('i.fa');
    
                    // update 'thumbs-up' button with latest state
                    $likesBtn.data('user-vote', data.user_vote);
                    $likesBtn.find('span').text(data.likes);
                    $likesIcon.toggleClass("fa-thumbs-up", data.user_vote === 1);
                    $likesIcon.toggleClass("fa-thumbs-o-up", data.user_vote !== 1);
                    // update 'thumbs-down' button with latest state
                    $dislikesBtn.data('user-vote', data.user_vote);
                    $dislikesBtn.find('span').text(data.dislikes);
                    $dislikesIcon.toggleClass("fa-thumbs-down", data.user_vote === -1);
                    $dislikesIcon.toggleClass("fa-thumbs-o-down", data.user_vote !== -1);
                    $('.o_wslides_js_slide_like_up_mx').data('slide-id', slide.id);
                    $('.o_wslides_js_slide_like_down_mx').data('slide-id', slide.id);
                    $('.o_wslides_js_slide_like_up_mx span').text(data.likes);
                    $('.o_wslides_js_slide_like_down_mx span').text(data.dislikes);
                }
            });
        },
        
        _onClickCustomNext: function() {
            var $slides = this.$('.o_wslides_fs_sidebar_list_item');
            var slideListdata = [];
            var slideList = []
            $slides.each(function () {
                var slideData = $(this).data();
                if (slideData.category == 'video' && slideData.videoSourceType !== 'vimeo' && !slideData.hasQuestion && !slideData.embedCode.includes('iframe')){
                    slideData.embedCode = '<iframe src=\"'+ slideData.embedCode + '\" allowFullScreen=\"true\" frameborder=\"0\"></iframe>'
                }
                slideListdata.push(slideData);
                slideList.push($(this));
            });
            var slide_list_data = this._preprocessSlideData(slideListdata);
            var index = 0;
            var slide = $('.o_wslides_fs_sidebar_list_item.active');
            if (slide.data().is_tincan && slide.data().category == 'scorm' && !slide.data().completed && !slide.data().hasQuestion){
                this.ScormComplete({'slideId':slide.data().id});
                if (!(slide.data().completed)){
                    this._alertShow('slide_tincan_incomplete');
                    $('.o_btn_set_done').addClass('d-none');
                    $('.o_btn_next_slide').removeClass('d-none');
                }
                else {
                    for(let [i,v] of slideList.entries()){
                        if(v[0].classList.contains('active')){
                            index = i;
                        }
                    }
                    if (index == slideList.length){
                        index = index - 1
                    }
                    var next_slide = slide_list_data[index + 1];
                    next_slide['canAccess'] = 'True';
                    var next_slide_list = slideList[index + 1]
                    var next_div = next_slide_list.find('.o_wslides_fs_slide_name');
                    this.slides.push(next_slide);
                    slide.removeClass('active');
                    $('.o_sidebar_link').attr("href", '#');
                    $('.o_btn_set_done').addClass('d-none');
                    $('.o_btn_next_slide').addClass('d-none');
                    next_slide_list.addClass('active');
                    next_div.removeClass('text-600');
                    // if (next_slide['hasLink']){
                    //     var next_link = next_slide_list.find('.o_wslides_fs_slide_link.o_sidebar_link_ids');
                    //     next_link.removeClass('text-600');
                    // }
                    if (slide.data()['hasQuestion'] || slide.data()['isQuiz'] || slide.data()['hasOra']){
                        var next_quiz = slide.find('.o_wslides_fs_sidebar_list_item a');
                        next_quiz.attr("href", '#');
                        next_quiz.removeClass('text-600');
                    }
                    this.sidebar.set('slideEntry',{
                        id: next_slide.id,
                        isQuiz: next_slide.isQuiz || false,
                        isOra: next_slide.isOra || false
                    });
                }
            }
            else {
                if ((slide.data().category != 'quiz' && slide.data().hasQuestion) || slide.data().hasOra){
                    for(let [i,v] of slideList.entries()){
                        if(v[0].classList.contains('ps-0.mb-1.active')){
                            index = i + 1;
                        }
                        else if(v[0].classList.contains('active')){
                            index = i;
                        }
                    }
                }
                else{
                    for(let [i,v] of slideList.entries()){
                        if(v[0].classList.contains('active')){
                            index = i;
                        }
                    }
                }
            if (index == slideList.length){
                index = index - 1
            }
            var next_slide = slide_list_data[index + 1];
            var next_slide_list = slideList[index + 1]
            var next_div = next_slide_list.find('.o_wslides_fs_slide_name');
            if (!(slide.data().completed) && slide.data()['isSequential'] && slide.data().category == 'quiz'){
                this._alertShow('slide_tincan_incomplete');
                $('.o_btn_set_done').addClass('d-none');
                $('.o_btn_next_slide').removeClass('d-none');
                next_div.addClass('text-600 disabled');
            }
            else {
                next_slide['canAccess'] = 'True';
                this.slides.push(next_slide);
                slide.removeClass('active');
                $('.o_sidebar_link').attr("href", '#');
                $('.o_btn_set_done').addClass('d-none');
                $('.o_btn_next_slide').addClass('d-none');
                next_slide_list.addClass('active');
                next_div.removeClass('text-600');
                // if (next_slide['hasLink']){
                //     var next_link = next_slide_list.find('.o_wslides_fs_slide_link.o_sidebar_link_ids');
                //     next_link.removeClass('text-600');
                // }
                if (slide.data()['hasQuestion'] || slide.data()['isQuiz'] || slide.data()['hasOra']){
                    var next_quiz = slide.find('.o_wslides_fs_sidebar_list_item a');
                    next_quiz.attr("href", '#');
                    next_quiz.removeClass('text-600');
                }
                this.sidebar.set('slideEntry',{
                    id: next_slide.id,
                    isQuiz: next_slide.isQuiz || false,
                    isOra: next_slide.isOra || false
                });
                }
            }
            this._rpc({
                route: '/website/channel/resume',
                params: {
                    slide_id: slide.data().id,
                },
            })
        },

        _onClickDone: function(){
            var slide = $('.o_wslides_fs_sidebar_list_item.active');
            var slideData = slide.data();
            if (slideData.is_tincan == undefined) {
                slideData.is_tincan = false;
            }
            if (slideData.hasNext == undefined) {
                slideData.hasNext = false;
            }
            if (slideData.completed == undefined) {
                slideData.completed = false;
            }
            if (!slideData.is_tincan){
                this._toggleSlideCompleted(slide.data());
                $('.o_btn_set_done').addClass('d-none');
                if (!(slideData.hasNext)){
                    $('.o_btn_next_slide').addClass('d-none');
                }
                else {
                    $('.o_btn_next_slide').removeClass('d-none');
                }
            }
            if (slideData.category == 'scorm' && slideData.is_tincan){
                var parent_this = this;
                const $slide = this.$(`.o_wslides_sidebar_done_button[data-id="${slideData.id}"]`);
                var slide_id = $slide.data().id;
                this._rpc({
                    route: '/slides/slide/scorm_set_completed',
                    params: {
                        slide_id: slide_id
                    }
                })
                .then(function (data){
                    if (data.result_passed || data.result_failed){
                        parent_this._toggleSlideCompleted($slide.data());
                        if (slideData.isTimer || slideData.isSequential){
                            $('.o_btn_set_done').addClass('d-none');
                            if (!(slideData.hasNext)){
                                $('.o_btn_next_slide').addClass('d-none');
                            }
                            else {
                                $('.o_btn_next_slide').removeClass('d-none');
                            }
                        }
                    }
                    else{
                        parent_this._alertShow('slide_tincan_incomplete');
                            if (slideData.isTimer || slideData.isSequential){
                                $('.o_btn_set_done').removeClass('d-none');
                                $('.o_btn_next_slide').addClass('d-none');
                            }
                        }
                });
            }
        },
         /**
         * After a slide has been marked as completed / uncompleted, update the state
         * of this widget and reload the slide if needed (e.g. to re-show the questions
         * of a quiz).
         *
         * We might need to set multiple slide as completed, because of "isQuiz"
         * set to True / False
         *
         */
        _toggleSlideCompleted: async function (slide, completed = true) {
            await this._super(...arguments);
            var slide = $('.o_wslides_fs_sidebar_list_item.active');
            if (slide.data().isTimer && !slide.data().completed){
                $('.o_wslides_fs_sidebar_list_item.active .o_wslides_button_complete').addClass('disabled'); 
            }
            this.toggleCompletionButton(slide, completed);
        },
        /**
         * We clicked on the "done" button.
         * It will make a RPC call to update the slide state and update the UI.
         */
        _onClickComplete: function (ev) {
            ev.stopPropagation();
            ev.preventDefault();
            const $button1 = $(ev.currentTarget).closest('.o_wslides_fs_sidebar_list_item');
            const $button = $(ev.currentTarget).closest('.o_wslides_sidebar_done_button');
            const slide = $button.data();
            if (slide.category === 'scorm' && slide.is_tincan && !slide.completed){
                if (slide.is_timer){
                    self.$('.o_wslides_fs_sidebar_list_item.active .o_wslides_button_complete').addClass('disabled');
                    $('.o_btn_set_done').addClass('d-none');
                    $('.o_btn_next_slide').addClass('d-none');
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
                var parent_this = this;
                const $slide = this.$(`.o_wslides_sidebar_done_button[data-id="${slide.id}"]`);
                var slide_id = $slide.data().id;
                this._rpc({
                    route: '/slides/slide/scorm_set_completed',
                    params: {
                        slide_id: slide_id
                    }
                })
                .then(function (data){
                    if (data.result_passed || data.result_failed){
                        parent_this._toggleSlideCompleted($slide.data());
                        if (slide.is_timer || slide.is_sequential){
                            $('.o_btn_set_done').addClass('d-none');
                            if (!($buttuon1.data().hasNext)){
                                $('.o_btn_next_slide').addClass('d-none');
                            }
                            else {
                                $('.o_btn_next_slide').removeClass('d-none');
                            }
                        }
                    }
                    else{
                        parent_this._alertShow('slide_tincan_incomplete');
                            if (slide.is_timer || slide.is_sequential){
                                $('.o_btn_set_done').removeClass('d-none');
                                $('.o_btn_next_slide').addClass('d-none');
                            }
                        }
                });
            }
            else {
                var res = this._super.apply(this, arguments);
                if (slide.is_timer){
                    self.$('.o_wslides_fs_sidebar_list_item.active .o_wslides_button_complete').addClass('disabled');
                    $('.o_btn_set_done').addClass('d-none');
                    $('.o_btn_next_slide').addClass('d-none');
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
                return res;
            }
        },

        _alertShow: function (alertCode) {
            var message = _t('There was an error validating this slide.');
            if (alertCode === 'slide_tincan_incomplete') {
                message = _t('You need to attempt current content to the end to mark it as done !');
            } else {
                message = _t('This slide is already completed');
            }
            this.displayNotification({
                type: 'warning',
                message: message,
                sticky: true
            });
        },

        _onSlideGoToNext : function (ev) {
                var self= this;
                var slide = $('.o_wslides_fs_sidebar_list_item.active');
                if (slide.data().isSequential && (slide.data().category == 'quiz' || slide.data().hasQuestion)){
                    var $slides = this.$('.o_wslides_fs_sidebar_list_item');
                    var slideListdata = [];
                    var slideList = []
                    $slides.each(function () {
                        var slideData = $(this).data();
                        if (slideData.category == 'video' && slideData.videoSourceType !== 'vimeo' && !slideData.hasQuestion && !slideData.embedCode.includes('iframe')){
                            slideData.embedCode = '<iframe src=\"'+ slideData.embedCode + '\" allowFullScreen=\"true\" frameborder=\"0\"></iframe>'
                        }
                        slideListdata.push(slideData);
                        slideList.push($(this));
                    });
                    var slide_list_data = this._preprocessSlideData(slideListdata);
                    var index = 0;
                    if (slide.data().category == 'quiz'){
                        for(let [i,v] of slideList.entries()){
                            if(v[0].classList.contains('active')){
                                index = i;
                            }
                        }
                    }
                    else if (slide.data().category != 'quiz' && slide.data().hasQuestion){
                        // if (slide.data().hasOra){
                        //     for(let [i,v] of slideList.entries()){
                        //         if(v[0].classList.contains('active')){
                        //             index = i + 2;
                        //         }
                        //     }
                        // }
                        // else{
                            for(let [i,v] of slideList.entries()){
                                if(v[0].classList.contains('active')){
                                    index = i + 1;
                                }
                            } 
                        // }
                    }
                    if (index == slideList.length){
                        index = index - 1
                    }
                    var next_slide = slide_list_data[index + 1];
                    next_slide['canAccess'] = 'True';
                    var next_slide_list = slideList[index + 1]
                    var next_div = next_slide_list.find('.o_wslides_fs_slide_name');
                    this.slides.push(next_slide);
                    slide.removeClass('active');
                    $('.o_sidebar_link').attr("href", '#');
                    $('.o_btn_set_done').addClass('d-none');
                    $('.o_btn_next_slide').addClass('d-none');
                    next_slide_list.addClass('active');
                    next_div.removeClass('text-600');
                    // if (next_slide['hasLink']){
                    //     var next_link = next_slide_list.find('.o_wslides_fs_slide_link.o_sidebar_link_ids');
                    //     next_link.removeClass('text-600');
                    // }
                    if (slide.data()['hasQuestion'] || slide.data()['isQuiz'] || slide.data()['hasOra']){
                        var next_quiz = slide.find('.o_wslides_fs_sidebar_list_item a');
                        next_quiz.attr("href", '#');
                        next_quiz.removeClass('text-600');
                        var next_mini = slide.find('.o_wslides_fs_sidebar_list_item span');
                        next_mini.attr("href", '#');
                        next_mini.removeClass('text-600');
                    }
                    this.sidebar.set('slideEntry',{
                        id: next_slide.id,
                        isQuiz: next_slide.isQuiz || false,
                        isOra: next_slide.isOra || false,
                    });
                }
                else {
                    this._super.apply(this, arguments);
                }
        },
        _preprocessSlideData: function (slidesDataList) {
            var res = this._super.apply(this, arguments);
            slidesDataList.forEach(function (slideData, index) {
                slideData.hasQuestion = !!slideData.hasQuestion;
                slideData.isQuiz = !!slideData.isQuiz;
                if (slideData.category === 'scorm'){
                    if (slideData.isTimer || slideData.is_tincan || slideData.hasQuestion == true){
                        slideData._autoSetDone = false;
                    }
                    else {
                        slideData._autoSetDone = true;
                    }
                }
                else {
                        if (_.contains(['infographic', 'document', 'article'], slideData.category)) {
                            slideData._autoSetDone = _.contains(['infographic', 'document', 'article'], slideData.category) && !slideData.hasQuestion && slideData.isTimer != 'True';
                        } else if (slideData.category === 'video' && slideData.videoSourceType === 'google_drive') {
                            slideData._autoSetDone =  !slideData.hasQuestion && slideData.isTimer != 'True';
                        }
                }
            });
            return res;
        },
        _onChangeSlideRequest: function (ev){
            this._super.apply(this, arguments);
            var slideData = ev.data;
            var $data = this.$el.prevObject.find('.js_publish_btn:visible').parents(".js_publish_management:first");
            this._rpc({
                route: '/website/publish/slide',
                params: {
                    id: slideData.id,
                },
            })
            .then(function (result) {
                if (result){
                    $data.removeClass("css_unpublished");
                    $data.addClass("css_published");
                    $data.find('input').prop("checked", result);
                    $data.parents("[data-publish]").attr("data-publish", +result ? 'on' : 'off');
                }else{
                    $data.removeClass("css_published");
                    $data.addClass("css_unpublished");
                    $data.find('input').prop("checked", result);
                    $data.parents("[data-publish]").attr("data-publish", +result ? 'on' : 'off');
                }
            })
            this._rpc({
                route: '/website/channel/resume',
                params: {
                    slide_id: slideData.id,
                },
            })
        },
        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------
        /**
         * Triggered whenever the user changes slides.
         * When the current slide is changed, widget will be automatically updated
         * and allowed to: fetch the content if needed, render it, update the url,
         * and set slide as "completed" according to its type requirements. In
         * mobile case (i.e. limited screensize), sidebar will be toggled since 
         * sidebar will block most or all of new slide visibility.
         *
         * @private
         */
        _onChangeSlide: function () {
            // var res = this._super.apply(this, arguments);
            var self = this;
            var slide = this.get('slide');
            self._pushUrlState();
            return this._fetchSlideContent().then(function() { // render content
                var websiteName = document.title.split(" | ")[1]; // get the website name from title
                document.title =  (websiteName) ? slide.name + ' | ' + websiteName : slide.name;
                if  (config.device.size_class < config.device.SIZES.MD) {
                    self._toggleSidebar(); // hide sidebar when small device screen
                }
                return self._renderSlide();
            }).then(function() {
                var slide = self.get('slide');
                var $slides = self.$('.o_wslides_fs_sidebar_list_item');
                var slideList = []
                var index = 0;
                $slides.each(function () {
                    slideList.push($(this));
                });
                if(slide.isSequential){
                    self.$('.o_wslides_fs_sidebar_list_item.active .o_wslides_button_complete').addClass('disabled');
                    self.$('.o_wslides_button_complete').addClass('disabled');
                    // for (var i = 0; i < slideList.length; i++) {
                    //     if (index != 0  && slide.isSequential){
                    //         if (slideList[i].data()['hasQuestion'] && !slideList[i].data()['completed'] || slideList[i].data()['hasOra']){
                    //             var next_quiz = slideList[i].find('.o_wslides_fs_sidebar_list_item a');
                    //             next_quiz.removeAttr("href", '#');
                    //             next_quiz.removeClass('active');
                    //             next_quiz.addClass('text-600');
                    //         }
                    //     }
                    //     if (i == 0 && slideList[i].data()['completed'] && slide.isSequential){
                    //         if (slideList[i].data()['hasQuestion']){
                    //             var next_quiz = slideList[i].find('.o_wslides_fs_sidebar_list_item a');
                    //             next_quiz.removeClass('text-600');
                    //         }
                    //     }
                    //     if (i == 0 && !slideList[i].data()['completed'] && slide.isSequential){
                    //         if (slideList[i].data()['hasOra']){
                    //             var next_quiz = slideList[i].find('.o_wslides_fs_sidebar_list_item a');
                    //             next_quiz.removeAttr("href", '#');
                    //             next_quiz.removeClass('active');
                    //             next_quiz.addClass('text-600');
                    //         }
                    //     }
                    // }
                    // for(let [i,v] of slideList.entries()){
                    //     if(v[0].classList.contains('active')){
                    //         index = i;
                    //         if (index < slideList.length - 1){
                    //             if (slide.isSequential && !slideList[index].data()['completed']){
                    //                 slideList[index].data()['hasNext'] = 'True';
                    //             }
                    //         }
                    //         if (index != 0 && slide.isSequential && !slideList[index-1].data()['completed'] ){
                    //             var CurrentSlide = slideList[index]
                    //             CurrentSlide.addClass('text-600 disabled');
                    //             CurrentSlide.removeClass('active');
                    //             slideList[index-1].addClass('active');
                    //         }
                    //         if (index != 0  && slide.isSequential){
                    //             if (slideList[index].data()['hasQuestion'] && !slideList[index].data()['completed'] || slideList[index].data()['hasOra']){
                    //                 var next_quiz = slideList[index].find('.o_wslides_fs_sidebar_list_item a');
                    //                 next_quiz.removeAttr("href", '#');
                    //                 next_quiz.removeClass('active');
                    //                 next_quiz.addClass('text-600');
                    //             }
                    //         }
                    //         if (index != 0 && slideList[index].data()['completed'] && slide.isSequential){
                    //             if (slideList[index].data()['hasQuestion'] || slideList[index].data()['hasOra']){
                    //                 var next_quiz = slideList[index].find('.o_wslides_fs_sidebar_list_item a');
                    //                 next_quiz.removeClass('text-600');
                    //             }
                    //         }
                    //     }
                    // }
                    for (var i = 0; i < slideList.length; i++) {
                        if (i == 0 && !slideList[i].data()['completed'] && slide.isSequential){
                            if (slideList[i].data()['hasQuestion']){
                                var next_quiz = slideList[i].find('.o_wslides_fs_sidebar_list_item a');
                                next_quiz.removeAttr("href", '#');
                                next_quiz.removeClass('active');
                                next_quiz.addClass('text-600');
                            }
                        }
                        if (i == 0 && slideList[i].data()['completed'] && slide.isSequential){
                            if (slideList[i].data()['hasQuestion']){
                                var next_quiz = slideList[i].find('.o_wslides_fs_sidebar_list_item a');
                                next_quiz.removeClass('text-600');
                            }
                        }
                    }
                    for(let [i,v] of slideList.entries()){
                        if(v[0].classList.contains('active')){
                            index = i;
                            if (index < slideList.length - 1){
                                if (slide.isSequential && !slideList[index].data()['completed']){
                                    slideList[index].data()['hasNext'] = 'True';
                                }
                            }
                            // if (index != 0 && !slideList[index-1].data()['completed'] && slide.isSequential){
                            //     var CurrentSlide = slideList[index]
                            //     CurrentSlide.addClass('text-600 disabled');
                            //     CurrentSlide.removeClass('active');
                            //     slideList[index-1].addClass('active');
                            // }
                            if (index != 0 && !slideList[index].data()['completed'] && slide.isSequential){
                                if (slideList[index].data()['hasQuestion']){
                                    var next_quiz = slideList[index].find('.o_wslides_fs_sidebar_list_item a');
                                    next_quiz.removeAttr("href", '#');
                                    next_quiz.removeClass('active');
                                    next_quiz.addClass('text-600');
                                }
                            }
                            if (index != 0 && slideList[index].data()['completed'] && slide.isSequential){
                                if (slideList[index].data()['hasQuestion']){
                                    var next_quiz = slideList[index].find('.o_wslides_fs_sidebar_list_item a');
                                    next_quiz.removeClass('text-600');
                                    var next_mini_slide = slideList[index].find('.o_wslides_fs_sidebar_list_item span');
                                    next_mini_slide.removeClass('text-600');
                                }
                            }
                        }
                    }
                    self.conditionOnchange(slide);
                    if(slide.isTimer){
                        if (!slide.completed){
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
                        self.conditionOnchange(slide);
                    }
                    else {
                        if (slide.is_tincan == undefined){
                            slide.is_tincan = false;
                        }
                        if((slide.category != 'scorm' && !slide.is_tincan) || (slide.category == 'scorm' && !slide.is_tincan)){
                            if (slide._autoSetDone && !session.is_website_user && !slide.isTimer) {  // no useless RPC call
                                if (slide.category === 'document') {
                                    // only set the slide as completed after iFrame is loaded to avoid concurrent execution with 'embedUrl' controller
                                    self.el.querySelector('iframe.o_wslides_iframe_viewer').addEventListener('load', () => self._toggleSlideCompleted(slide));
                                } else {
                                    self._toggleSlideCompleted(slide);
                                }
                                self.conditionOnchange(slide);
                            }
                        }
                    }    
                }
                else if(slide.isTimer && !slide.isSequential){
                    if (!slide.completed){
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
                    self.conditionOnchange(slide);
                }
                else {
                     if((slide.category != 'scorm' && !slide.is_tincan) || (slide.category == 'scorm' && !slide.is_tincan)){
                        if (slide._autoSetDone && !session.is_website_user) {  // no useless RPC call
                            if (slide.category === 'document') {
                                // only set the slide as completed after iFrame is loaded to avoid concurrent execution with 'embedUrl' controller
                                self.el.querySelector('iframe.o_wslides_iframe_viewer').addEventListener('load', () => self._toggleSlideCompleted(slide));
                            } else {
                                return self._toggleSlideCompleted(slide);
                            }
                        }
                    }
                }
            });
        },

        conditionOnchange : function(slide){
            // var slide = $('.o_wslides_fs_sidebar_list_item.active');
            var slideData = slide;
            if (slideData.completed == undefined) {
                slideData.completed = false;
            }
            if (slideData.is_tincan == undefined){
                slideData.is_tincan = false;
            }
            if (!(slideData.hasNext)){
                $('.o_btn_next_slide').addClass('d-none');
            }
            if (slideData.completed){
                $('.o_btn_set_done').addClass('d-none');
            }
            if (slideData.isSequential && !(slideData.isTimer) && slideData.hasNext){
                if ( slideData.category != 'scorm' && !slideData.is_tincan ){$('.o_btn_next_slide').removeClass('d-none');}
                if ( !(slideData.category == 'quiz') ){$('.o_btn_next_slide').removeClass('d-none');}
            }
            if (slideData.isSequential && !slideData.completed && slideData.category == 'scorm' && slideData.is_tincan && !(slideData.isTimer)){
                $('.o_btn_set_done').removeClass('d-none');
                $('.o_btn_next_slide').addClass('d-none');
            }
            if (slideData.isSequential && slideData.completed && slideData.category == 'scorm' && slideData.is_tincan && !(slideData.isTimer)){
                $('.o_btn_set_done').addClass('d-none');
                $('.o_btn_next_slide').removeClass('d-none');
            }
            if (slideData.is_tincan && slideData.isTimer && slideData.category == 'scorm' && slideData.completed){
                $('.o_btn_next_slide').addClass('d-none');
                $('.o_btn_set_done').addClass('d-none');
            }
            if (slideData.completed && slideData.isTimer == 'True' && slideData.hasNext){
                $('.o_btn_next_slide').removeClass('d-none');
                $('.o_btn_set_done').addClass('d-none');
            }
            if (slideData.completed == false && slideData.isTimer == 'True') {
                $('.o_btn_next_slide').addClass('d-none');
            }
            if ((slideData.category == 'quiz' || slideData.hasQuestion) && slideData.isTimer == 'True'){
                $('.o_btn_next_slide').addClass('d-none');
                $('.o_btn_set_done').addClass('d-none');
            }
        },
        /**
         * This method is called when slide type is scorm and scorm type is tincan
         * to complete the content based on result-passed/failed on fullscreen
         * @private
         * @param {Integer} slideId: the id of slide to set as completed
        */
        ScormComplete: function(slideId){
            var parent_this = this;
            const $slide = this.$(`.o_wslides_sidebar_done_button[data-id="${slideId}"]`);
            var slide_id = $slide.data().id;
            this._rpc({
                route: '/slides/slide/scorm_set_completed',
                params: {
                    slide_id: slide_id
                }
            })
            .then(function (data){
                if (data.result_passed || data.result_failed){
                    parent_this._toggleSlideCompleted($slide.data());
                }
            });
        }
    });
});