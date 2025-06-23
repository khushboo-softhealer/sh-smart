odoo.define('mx_elearning_pro.course_extended', function (require) {
    'use strict';
    var core = require('web.core');
    var publicWidget = require('web.public.widget');
    var CourseJoinWidget = require('@website_slides/js/slides_course_join')[Symbol.for("default")].courseJoinWidget;

    var _t = core._t;

    publicWidget.registry.websiteCourseExtended = publicWidget.Widget.extend({
        selector: '.o_course_extended',

        /**
         * @override
         */
        start: function () {
            $('.o_course_extended').on('click','#collapse_div',function() {
                var id = this.dataset.target.split('-')[1]
                if($('#slide-'+id).is(":visible")) {
                    $('#slide-'+id).hide()
                    $(this).children().first().children().removeClass('fa-minus');
                    $(this).children().first().children().addClass('fa-plus');
                }else {
                    $('#slide-'+id).show()
                    $(this).children().first().children().removeClass('fa-plus');
                    $(this).children().first().children().addClass('fa-minus');
                }
            });
        }
    }),

    CourseJoinWidget.include({
        //--------------------------------------------------------------------------
        // Public
        //--------------------------------------------------------------------------
        /**
         * @public
         * @param {integer} channelId
         */
        joinChannel: function (channelId) {
            var self = this;
            this._rpc({
                route: '/slides/channel/join',
                params: {
                    channel_id: channelId,
                },
            }).then(function (data) {
                if (!data.error) {
                    self.afterJoin();
                } else {
                    if (data.error === 'public_user') {
                        var message = _t('Please <a href="/web/login?redirect=%s">login</a> to join this course');
                        var signupAllowed = data.error_signup_allowed || false;
                        if (signupAllowed) {
                            message = _t('Please <a href="/web/signup?redirect=%s">create an account</a> to join this course');
                        }
                        self._popoverAlert(self.$el, _.str.sprintf(message, (document.URL)));
                    } else if (data.error === 'join_done') {
                        self._popoverAlert(self.$el, _t('You have already joined this channel'));
                    } else if (data.error === 'dependency_error') {
                        let error_message = `<b>Join/Complete dependent courses before opting this course.</b>
                            <table class="table table-condensed">
                                <thead>
                                    <th>Courses</th>
                                    <th>Completion(%)</th>
                                </thead>
                            <tbody>`
                        for (var key in data.error_courses) {
                            error_message += `<tr><td>${key}</td><td class="text-center">${data.error_courses[key]}</td></tr>`;
                        }
                        error_message += '</tbody></table>'
                        self._popoverAlert(self.$el, _t(error_message));
                    } else {
                        self._popoverAlert(self.$el, _t('Unknown error'));
                    }
                }
            });
        },
    })
});
