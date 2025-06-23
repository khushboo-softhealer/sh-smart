/** @odoo-module **/

import SurveyFormWidget from 'survey.form';
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";

SurveyFormWidget.include({
    start: async function () {
        this.CLIENT_ID = null;
        this.CLIENT_SECRET = null;
        this.isProctoring = null;
        // this.uiService = useService("ui");
        // this.notification = useService("notification");
        this._super.apply(this, arguments);
    },

    getTestAttemptId: function () {
        return Math.random().toString(36).slice(2, 7);
    },

    getHashTestAttemptId: function (testAttemptId) {
        if (this.CLIENT_SECRET === null) {
            return null;
        } else {
            const secretWordArray = CryptoJS.enc.Utf8.parse(this.CLIENT_SECRET);
            const messageWordArray = CryptoJS.enc.Utf8.parse(testAttemptId);
            const hash = CryptoJS.HmacSHA256(messageWordArray, secretWordArray);
            const base64HashedString = CryptoJS.enc.Base64.stringify(hash);
            return base64HashedString;
        }
    },

    getCredentials: async function () {
        const testAttemptId = this.getTestAttemptId();
        var self = this;

        await this._rpc({
            route: '/get/autoproctor/credentials',
        }).then(function (data) {
            self.CLIENT_ID = data.client_id;
            self.CLIENT_SECRET = data.client_secret;
        });
        if (!this.CLIENT_ID || !this.CLIENT_SECRET) {
            this.displayNotification({
                type: 'danger',
                message: _t('Proctoring credentials are missing. Please contact support.'),
                sticky: true
            });
            // this.notification.add(_t("Proctoring credentials are missing. Please contact support."),{type: 'danger'});
            return null;
        }

        const hashedTestAttemptId = this.getHashTestAttemptId(testAttemptId);
        const creds = {
            clientId: this.CLIENT_ID,
            testAttemptId: testAttemptId,
            hashedTestAttemptId: hashedTestAttemptId
        };
        return creds;
    },

    setupProctoring: async function () {
        if (!this.isProctoring) {
            return;
        }
        const credentials = await this.getCredentials();
        this.apInstance = new AutoProctor(credentials)
        $('body').append('<div id="fullscreen_mode"></div>');
        // Proctoring options
        const proctoringOptions = {
            trackingOptions: {
                audio: true,
                numHumans: true,
                tabSwitch: true,
                photosAtRandom: true,
                detectMultipleScreens: true,
                forceFullScreen: false,
                forceDesktop: true,
            },
            showHowToVideo: true,
            testContainerId: 'fullscreen_mode',
        };
        await this.apInstance.setup(proctoringOptions);
    },

    getReportOptions: function () {
        return {
            showProctoringSummary: true,
            showSessionRecording: true,
            groupReportsIntoTabs: true,
            userDetails: {
                name: "First Last",
                email: "user@gmail.com"
            },
        };
    },

    _onSubmit: async function (event) {
        event.preventDefault();
        var options = {};
        var $target = $(event.currentTarget);
        var self = this;
    
        if ($target.val() === 'start') {
            // Check if proctoring is enabled
            await this._rpc({
                route: '/get/autoproctor/enabled',
                params: {
                    survey_token: this.options.surveyToken,
                },
            }).then(function (data) {
                self.isProctoring = data.is_proctoring;
            });
            if (this.isProctoring) {
                await this.setupProctoring();
                this.apInstance.start();
            }
            this._submitForm(options);
        } else if ($target.val() === 'finish') {
            options.isFinish = true;
            if (this.isProctoring) {
                this.apInstance.stop();
                $('body').addClass('o_block_ui');
                window.addEventListener("apMonitoringStopped", async () => {
                    try {
                        let reportData;
                        let conditionMet = false;
    
                        while (!conditionMet) {
                            reportData = await this.apInstance.getReport();
                            conditionMet = reportData && reportData.testAttemptStatus === 'trust_score_calculated';
    
                            if (!conditionMet) {
                                await new Promise(resolve => setTimeout(resolve, 1000))
                            }
                        }
                        await self._rpc({
                            route: '/survey/save/proctor',
                            params: {
                                survey_token: self.options.surveyToken,
                                answer_token: self.options.answerToken,
                                proctor_data: reportData
                            },
                        });
                        self._submitForm(options);
                    } finally {
                        $('body').removeClass('o_block_ui');
                        // await this.uiService.unblock();
                    }
                });
            } else {
                self._submitForm(options);
            }
        } else {
            this._submitForm(options);
        }
    },
});