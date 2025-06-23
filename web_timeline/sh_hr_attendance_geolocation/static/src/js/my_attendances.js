odoo.define("sh_hr_attendance_geolaction.my_attendances_geolocation", function (require) {
    "use strict";

    var core = require("web.core");
    var ajax = require("web.ajax");
    var QWeb = core.qweb;
    var _t = core._t;
    window.location_data = "";
    var latitude = "";
    var longitude = "";
    var other_data = ""
    var MyAttendances = require("hr_attendance.my_attendances");

    MyAttendances.include({

        events: {
            "click .o_hr_attendance_sign_in_out_icon": _.debounce(function () {
                this.update_attendance();
            }, 200, true),
            "change #sh_break": _.debounce(function () {
                this.onchange_break();
            }, 200, true),
        },
        _startTimeCounter: function (duration, start) {
            var self = this;
            var pr = start
            if (pr) {
                self.abc = setTimeout(function () {
                    duration += 1000;
                    $("#break_task_timer").html('<span>' + moment.utc(duration).format("HH:mm:ss") + '</span>');
                    localStorage.setItem("break", duration);
                    localStorage.setItem("break_start", true);
                    var ss = localStorage.getItem('break');
                    self._startTimeCounter(parseInt(ss), pr);

                }, 1000);
            } else {
                clearTimeout();
                localStorage.removeItem("break");
                localStorage.removeItem("break_start");
            }





        },
        onchange_break: function () {
            $("#break_task_timer").css("display", "none")
            var duration;

            var message_selection = $("#message_selection_input").val();

            message_selection = message_selection.replaceAll("'", "");
            var option = $("#message_selection").find("[value='" + message_selection + "']");
            var message = $("#message_selection_input").val();
            var sh_break = $('#sh_break').prop("checked");
            var self = this;
            this._rpc({
                model: 'hr.employee',
                method: 'sh_onchange_break',
                args: [
                    [self.employee.id],
                    [message, sh_break]],
            })
                .then(function (result) {

                    if (result && result.warning_end) {
                        self.displayNotification({ title: result.warning_end, type: 'danger' });
                        $('#sh_break').prop('checked', true);
                        $('.o_hr_attendance_sign_in_out_icon').css("display", "inline-block");
                        $('.bye').css("display", "flex");

                    }
                    else if (result && result.warning_break) {
                        self.displayNotification({ title: result.warning_break, type: 'danger' });
                        $('#sh_break').prop('checked', false);
                    }
                    else if (result && result.warning) {
                        if (result) {

                            $("#message_selection_input").val("")
                            var duration = 0.0

                            if (result['timer_start']) {
                                $("#break_task_timer").css("display", "block")
                                localStorage.setItem("break_start", true);
                                self._startTimeCounter(duration, true);
                                $('.o_hr_attendance_sign_in_out_icon').css("display", "none");
                                $('.bye').attr("style", "display: none !important");
                            } else {
                                localStorage.removeItem('break');
                                localStorage.removeItem('break_start');
                                clearTimeout(self.abc)
                                self._startTimeCounter(duration, false);
                                $("#break_task_timer").css("display", "none")
                                if (self.show_checkin) {
                                    $('.o_hr_attendance_sign_in_out_icon').css("display", "inline-block");
                                    $('.o_hr_attendance_sign_in_out_icon').removeClass('d-none');
                                }

                                $('.bye').css({"display":"flex","justify-content":"center"});
                                $('.bye').removeClass('d-none');

                            }


                        }
                        self.displayNotification({ title: result.warning, type: 'danger' });
                        //                    location.reload();

                    }
                });
        },
        matchItem: function (string, data) {
            var i = 0,
                j = 0,
                html = '',
                regex,
                regexv,
                match,
                matches,
                version;

            for (i = 0; i < data.length; i += 1) {
                regex = new RegExp(data[i].value, 'i');
                match = regex.test(string);
                if (match) {
                    regexv = new RegExp(data[i].version + '[- /:;]([\d._]+)', 'i');
                    matches = string.match(regexv);
                    version = '';
                    if (matches) { if (matches[1]) { matches = matches[1]; } }
                    if (matches) {
                        matches = matches.split(/[._]+/);
                        for (j = 0; j < matches.length; j += 1) {
                            if (j === 0) {
                                version += matches[j] + '.';
                            } else {
                                version += matches[j];
                            }
                        }
                    } else {
                        version = '0';
                    }
                    return {
                        name: data[i].name,
                        version: parseFloat(version)
                    };
                }
            }
            return { name: 'unknown', version: 0 };
        },
        init: function (parent, action) {
            var self = this;
            this._super.apply(this, arguments);
            this.break_start = false
            this.show_checkin = false
            var os = [
                { name: 'Windows Phone', value: 'Windows Phone', version: 'OS' },
                { name: 'Windows', value: 'Win', version: 'NT' },
                { name: 'iPhone', value: 'iPhone', version: 'OS' },
                { name: 'iPad', value: 'iPad', version: 'OS' },
                { name: 'Kindle', value: 'Silk', version: 'Silk' },
                { name: 'Android', value: 'Android', version: 'Android' },
                { name: 'PlayBook', value: 'PlayBook', version: 'OS' },
                { name: 'BlackBerry', value: 'BlackBerry', version: '/' },
                { name: 'Macintosh', value: 'Mac', version: 'OS X' },
                { name: 'Linux', value: 'Linux', version: 'rv' },
                { name: 'Palm', value: 'Palm', version: 'PalmOS' }
            ]


            var browser = [
                { name: 'Chrome', value: 'Chrome', version: 'Chrome' },
                { name: 'Firefox', value: 'Firefox', version: 'Firefox' },
                { name: 'Safari', value: 'Safari', version: 'Version' },
                { name: 'Internet Explorer', value: 'MSIE', version: 'MSIE' },
                { name: 'Opera', value: 'Opera', version: 'Opera' },
                { name: 'BlackBerry', value: 'CLDC', version: 'CLDC' },
                { name: 'Mozilla', value: 'Mozilla', version: 'Mozilla' }
            ]

            var header = [
                navigator.platform,
                navigator.userAgent,
                navigator.appVersion,
                navigator.vendor,
                window.opera
            ];
            var agent = header.join(' ');
            var os = this.matchItem(agent, os);
            var browser = this.matchItem(agent, browser);
            other_data = 'Os : ' + os.name + '\n ,Browser: ' + browser.name + '\n ,Agent : ' + agent + '\n ,Platform ' + window.navigator.platform
            // if (os.name === 'Windows' || os.name === 'Linux' ) {

            const isTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
            if (window.navigator.platform == 'Linux x86_64' || window.navigator.platform == 'Win32' || (window.navigator.platform == 'MacIntel' && !isTouch)) {
                
                this.show_checkin = true
            } else {
                this.show_checkin = false
            }
            
            this._rpc({
                model: 'hr.employee',
                method: 'sh_get_break_duration',
                args: [
                ],
            })
                .then(function (result) {
                    if (result) {
                        self.break_start = true
                    }
                });


            var message = [];
            ajax.jsonRpc(
                "/web/dataset/call_kw",
                "call",
                {
                    model: "sh.predefined.reason",
                    method: "search_read",
                    args: [[], ["name"]],
                    kwargs: {},
                },
                { async: false }
            ).then(function (result) {
                _.each(result, function (reason) {
                    message.push({ id: reason["id"], name: reason["name"] });
                });
                self.message_list = message;
            });

        },
        start: function () {
            var self = this;
            this._super.apply(this);

            $.get('/get_break_start_time', {
            }, function (result) {
                var data = JSON.parse(result);
                if (data['end']) {
                    self._startTimeCounter(parseInt(data['b_start']), true);
                }

            });

            if ("geolocation" in navigator) {
                navigator.geolocation.getCurrentPosition(setCurrentPosition, positionError, {
                    enableHighAccuracy: true,
                    timeout: 15000,
                    maximumAge: 0,
                });

                function setCurrentPosition(position) {
                    latitude = position.coords.latitude;
                    longitude = position.coords.longitude;
                }
                function positionError(error) {
                    switch (error.code) {
                        case error.PERMISSION_DENIED:
                            console.error("User denied the request for Geolocation.");
                            break;
                        case error.POSITION_UNAVAILABLE:
                            console.error("Location information is unavailable.");
                            break;
                        case error.TIMEOUT:
                            console.error("The request to get user location timed out.");
                            break;
                        case error.UNKNOWN_ERROR:
                            console.error("An unknown error occurred.");
                            break;
                    }
                }
            }
        },
        update_attendance: function () {
            var message_selection = $("#message_selection_input").val();
            var option = $("#message_selection").find("[value='" + message_selection + "']");
            var message = $("#message_selection_input").val();
            var bye = $('#sh_bye').prop("checked");
            var self = this;
            // if (!latitude || !longitude) {
            //     alert("Please Check your browser Settings and Allow Location !")
            // } else {
                this._rpc({
                    model: 'hr.employee',
                    method: 'sh_attendance_manual',
                    args: [
                        [self.employee.id],
                        [message, latitude, longitude, bye, other_data], 'hr_attendance.hr_attendance_action_my_attendances'
                    ],
                })
                    .then(function (result) {
                        if (result.action) {
                            self.do_action(result.action);
                        } else if (result.warning) {
                            self.displayNotification({ title: result.warning, type: 'danger' });
                        }
                    });

            // }

        },
    });
});
