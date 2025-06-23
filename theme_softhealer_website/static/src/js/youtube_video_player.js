odoo.define('theme_softhealer_website.youtube_video_player', function (require) {
    'use strict';

    var Dialog = require('web.Dialog');
    var publicWidget = require('web.public.widget');
    var core = require('web.core');
    var _t = core._t;

    var YoutubeDialog = Dialog.extend({
        events: _.extend({}, Dialog.prototype.events, {
            'click .js_cls_iframe_close': '_onClickCloseIframe',
        }),
        template: "sh.softhealer.website.video.youtube",
        // youtubeUrl: 'https://www.youtube.com/iframe_api',
        init: function (parent, options, videoUrl) {
            options = _.defaults(options || {}, {
                // title: _t("YouTube"),
                renderHeader: false,
                renderFooter: false,
                backdrop: true,
                // buttons: [{ text: "Close", close: true }],
                size: 'large',
            });
            this.videoUrl = videoUrl;
            this._super(parent, options);
        },
        /**
         * @override
         */
        willStart: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self.$modal.find('.modal-dialog').addClass('modal-dialog-centered');
             });
        },
        /**
         * @private
         * @param {Event} ev 
         */
        _onClickCloseIframe: function (ev) {
            ev.stopPropagation();
            this.close();
        }
    })

    publicWidget.registry.YoutubeVideoPlayer = publicWidget.Widget.extend({
        selector: '.js_cls_youtube_video_player_dialog',
        events: {
            "click .js_cls_item": "_onClickItem",
            "click a.js_cls_a_video_link": "_onClickAlink"
        },
        start: function () {
            return this._super.apply(this, arguments);
        },

        _openYoutubeVideoDialog: function (videoUrl) {
            // Split the video token form video url
            const urlArr = videoUrl.split('/');
            let token = urlArr[urlArr.length - 1];
            if (token.includes('watch')) {
                token = token.split('v=')[1];
                const amp = token.indexOf('&');
                if (amp !== -1) {
                    token = token.substring(0, amp);
                }
            }
            // For iframe prepare Youtube url with embed token.
            const dialog = new YoutubeDialog(this, {}, `https://www.youtube.com/embed/${token}`);
            dialog.open();
        },
        /**
         * Open youtube video player dialog
         * 
         * @private
         * @param {Event} ev 
         */
        _onClickAlink: function (ev) {
            ev.stopPropagation();
            var videoUrl = $(ev.currentTarget).attr("data-youtube-video-url");
            this._openYoutubeVideoDialog(videoUrl);

        },
        _onClickItem: function (ev) {
            var $alink = $(ev.currentTarget).find('.js_cls_a_video_link');
            if ($alink.length) {
                var videoUrl = $alink.attr("data-youtube-video-url");
                this._openYoutubeVideoDialog(videoUrl);
            }
        }
    })
});