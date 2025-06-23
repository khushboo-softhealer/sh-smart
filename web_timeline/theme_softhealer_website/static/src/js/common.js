odoo.define("theme_softhealer_website.common_custom_js_crm_solution", function (require) {
    "use strict";

    var publicWidget = require("web.public.widget");
    const { loadJS, loadCSS } = require('@web/core/assets');

    publicWidget.registry.sh_theme_website_common_js = publicWidget.Widget.extend({
        selector: '#wrapwrap',

        /**
         * @override
        */
       async willStart() {
        const _super = this._super.bind(this);
        // Load Libs
            try {
                await loadJS('/theme_softhealer_website/static/src/lib/swiper/swiper.min.js');
                await loadCSS('/theme_softhealer_website/static/src/lib/swiper/swiper.min.css');
            } catch (error) {
                console.error('Error:', error);
            }
            return _super(...arguments);
        },
        async start() {
            
            this._super(...arguments);
            var swiper1 = new Swiper('.gallery-thumbs', {
                loop: true,
                loopedSlides: 10,
                centeredSlides: true,
                spaceBetween: 50,
                slideToClickedSlide: true,
                slidesPerView: 3,
                watchSlidesVisibility: true,
                watchSlidesProgress: true,
                breakpoints: {  
                                '1400': {
                                    slidesPerView: 3,
                                },
                                '1200': {
                                    slidesPerView: 3,
                                },
                                '992': {
                                    slidesPerView: 3,
                                },
                                '768': {
                                    slidesPerView: 3,
                                },
                                '576': {
                                    slidesPerView: 1,
                                    spaceBetween: 20,
                                },
                                '0': {
                                    slidesPerView: 1,
                                },
                            },
              });
              
              var swiper2 = new Swiper('.gallery-top', {
                loop: true,
                loopedSlides: 10,
                spaceBetween: 10,
                effect:'fade',
                navigation: {
                  nextEl: '.swiper-button-next',
                  prevEl: '.swiper-button-prev',
                },
              
                // USING THE THUMBS COMPONENT
                // thumbs: {
                //   swiper: galleryThumbs
                // }
              });
              
              
              // ALTERNATIVE SOLUTION to get the active thumb centered, it doesn't work on Safari if sliding backwards
              swiper2.controller.control = swiper1;
              swiper1.controller.control = swiper2;
        
    },
    });

    publicWidget.registry.ShCrmTabSolutionSection = publicWidget.Widget.extend({
        selector: ".sh_crm_solution_tab_section",
        disabledInEditableMode: true,
        events: {
            "click .sh_crm_solution_tabs_item .sh_crm_solution_tabs_item_link": "_scrollCrmSolutionClick",
        },

        _scrollCrmSolutionClick: function (ev) {
            var self = this;
            var $link = $(ev.currentTarget);
            var link = $link.attr('href');
            var $target = self.$el.find(link);
            var basescrollLocation = $target.offset().top;
            var scrollinside = $("#wrapwrap").scrollTop();
            // For tab active
            $link.parents('.sh_crm_solution_nav_tab').find('.sh_crm_solution_tabs_item_link').removeClass('active')
            $link.addClass('active')
            
            // for tab content scroll
            $('html, body').stop().animate({
				scrollTop: basescrollLocation + scrollinside - 100
			}, 1500);

        }
    });

    publicWidget.registry.ShRelatedServiceSectionCustomJs = publicWidget.Widget.extend({
        selector: ".sh_related_services",
        disabledInEditableMode: true,

        start: function () {
            var self = this
            var service_arr = [];
            while(service_arr.length < 3){
                var r = Math.floor(Math.random() * 5) + 1;
                if(service_arr.indexOf(r) === -1) service_arr.push(r);
            }
            
            if (service_arr.length > 0){
                var count = 0

               _.each(service_arr.sort(), function (service_id) {
                    count = count + 300 
                    $('.related_service_' + service_id).removeClass('d-none')
                    if ($('.related_service_' + service_id).find('div.sh_main_box').hasClass('aos-animate')){
                        $('.related_service_' + service_id).find('div.sh_main_box').removeClass('aos-animate');
                        $('.related_service_' + service_id).find('div.sh_main_box').attr('data-aos-delay',count);
                    }
                });
            }
            return this._super.apply(this, arguments);
        },

    })


});
$(document).ready(function () {
    // Load the active index from local storage and apply the 'active' class
    let activeIndex = localStorage.getItem('activeSliderIndex');
    if (activeIndex !== null) {
      $('.sh_slider_image').eq(activeIndex).addClass('active');
    }
  
    // On click, toggle 'active' class and update local storage
    $('.sh_slider_image').on('click', function () {
      // Remove 'active' class from all and add it to the clicked one
      $('.sh_slider_image').removeClass('active');
      $(this).addClass('active');
  
      // Get the index of the clicked element and store it in local storage
      let index = $('.sh_slider_image').index(this);
      localStorage.setItem('activeSliderIndex', index);
    });
  });

  $(document).ready(function() {
    $('.sh_testimonial_li').on('click', function() {
        var index = $(this).index(); // Get the index of the clicked element

        // Remove 'active' class from all elements
        $('.sh_testimonial_li, .sh_slider_image').removeClass('active');

        // Add 'active' class to the clicked item and corresponding slider image
        $('.sh_testimonial_li').eq(index).addClass('active');
        $('.sh_slider_image').eq(index).addClass('active');
    });
});