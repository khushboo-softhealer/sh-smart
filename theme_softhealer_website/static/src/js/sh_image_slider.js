odoo.define('theme_softhealer_website.sh_image_scroll', function (require) {
    "use strict";
    // alert("2")
    var concurrency = require("web.concurrency");
    const {Markup} = require('web.utils');

    var publicWidget = require('web.public.widget');
    var rpc = require('web.rpc'); // Import RPC for data fetching
    var _t = require('web.core')._t; // Translation utility
    

    publicWidget.registry.ShImageScroll = publicWidget.Widget.extend({
        
        selector: ".sh_image_scroll",
        events: Object.assign({}, publicWidget.Widget.prototype.events, {
            
            'click .open_slider': '_onClickOpenSlider',
        }),
        disabledInEditableMode: true,
        /**
         * @constructor
         */
        init: function () {
            this._super.apply(this, arguments);
            this._dp = new concurrency.DropPrevious();

        },
        /**
         * @override
         */
        start: function () {
            this._dp.add(this._fetch()).then(this._render.bind(this));
            this.image_data = this._fetch()
            return this._super.apply(this, arguments);
        },
        
        /**
         * @private
         */
        _fetch: async function (values) {
            // Add dynamic content
            // return this._rpc
            // ({
            //     model: 'sh.image.slider',
            //     method: 'get_data',
            //     args: [[]],
            return this._rpc({
                route: "/theme_softhealer_website/get_data",
                params: {},
            }).then((res) => {
                console.log("re",res.data)
                this.image_data = res.data
                return res;
            });
            
        },

        _render: function (res) {
            // Add dynamic content
            this.$(".js_cls_render_image").html(res.data)},

        _onClickOpenSlider: function (ev) {
                let parentCard = $(ev.currentTarget).closest(".sh_image_card");
                let imageText = parentCard.find("h1").eq(1).text(); // Get image data
                if (!imageText) {
                    console.warn("No image data found.");
                    return;
                }
    
                // Parse image URLs
                let imageUrls = imageText.replace(/[\[\]']/g, "").split(", ");
                imageUrls = imageUrls.filter(img => img && img !== "False");
    
                if (imageUrls.length === 0) {
                    console.warn("No valid images to display.");
                    return;
                }
    
                // Open the image slider
                this._openImageSlider(imageUrls);
            },
    
            /**
             * Creates and opens an image slider
             */
            _openImageSlider: function (images) {
                let sliderHtml = `
                    <div class="sh-image-slider">
                        <span class="slider-close">&times;</span>
                        <div class="slider-container">
                            ${images.map((img, index) => `
                                <img src="data:image/webp;base64,${img}" class="slider-image ${index === 0 ? 'active' : ''}" data-index="${index}">
                            `).join('')}
                        </div>
                        <button class="slider-prev">&lt;</button>
                        <button class="slider-next">&gt;</button>
                    </div>
                `;
                $("body").append(sliderHtml);
    
                $(".slider-close").click(() => $(".sh-image-slider").remove());
                $(".slider-prev").click(() => this._changeImage(-1));
                $(".slider-next").click(() => this._changeImage(1));
    
                this.currentIndex = 0;
                this.totalImages = images.length;
            },
    
            /**
             * Handles Next/Prev image navigation
             */
            _changeImage: function (direction) {
                let images = $(".slider-image");
                images.eq(this.currentIndex).removeClass("active");
    
                this.currentIndex += direction;
                if (this.currentIndex < 0) this.currentIndex = this.totalImages - 1;
                if (this.currentIndex >= this.totalImages) this.currentIndex = 0;
    
                images.eq(this.currentIndex).addClass("active");
            },
        
            // // Close Modal
            // closeSlider() {
            //     document.getElementById("imageSliderModal").style.display = "none";
            // }

    });



    return publicWidget.registry.ShImageScroll;
});
