odoo.define("theme_softhealer_website.owl_carousel_init", function (require) {
    "use strict";

    var publicWidget = require("web.public.widget");

    publicWidget.registry.ShAllOwlCarouselInit = publicWidget.Widget.extend({
		selector: "#wrapwrap",

		events: {
            "click .js_cls_sh_website_back_to_top": "_onClickScrollToTop",
        },

		start: function () {
			
			$('.sh_carousel_main').owlCarousel({
				items: 6,
				loop: true,
				margin: 10,
				dots: false,
				nav:false,
				autoplay: true,
				autoplayTimeout: 3000,
				responsiveClass:true,
				responsive:{
					0:{
						items:2,
					},
					600:{
						items:3,
						
					},
					1000:{
						items:6,
					}
				}
				
			})

			$("#owl-demo").owlCarousel({
				items: 4,
				loop: true,
				autoplay: true,
				autoplayTimeout: 5000,
				margin: 20,
				nav: true,
				dots: false,
				responsiveClass:true,
				responsive:{
					0:{
						items:1,
					},
					500:{
						items:2,
						
					},
					1000:{
						items:3,
					},
					1300:{
						items:4,
					}
				}
		
			});
			$("#owl-testimonial").owlCarousel({
				items: 3,
				loop: true,
				center:true,
				autoplay: true,
				autoplayTimeout: 5000,
				dots:false,
				margin: 10,
				responsiveClass:true,
				responsive:{
					0:{
						items:1,
						center:false,
					},
					500:{
						items:2,
						center:false,
						
					},
					1000:{
						items:3,
					}
				}
		
			});

			$("#navratri-slider").owlCarousel({
				items: 3,
				loop: true,
				autoplay: true,
				autoplayTimeout: 5000,
				margin: 20,
				nav: true,
				dots: false,
				responsiveClass:true,
				responsive:{
					0:{
						items:1,
					},
					500:{
						items:2,
						
					},
					1000:{
						items:3,
					},
					1300:{
						items:3,
					}
				}
		
			});

			$("#sh_future_owl_demo").owlCarousel({
				item:3,
				loop: true,
				autoplay: true,
				autoplayTimeout: 5000,
				margin: 20,
				nav: true,
				dots: false,
				responsiveClass:true,
				responsive:{
					0:{
						items:1,
					},
					500:{
						items:2,
						
					},
					1000:{
						items:3,
					},
					1300:{
						items:3,
					}
				}
		
			});

			$("#work-anniversary-slider").owlCarousel({
				item:3,
				loop: true,
				autoplay: true,
				autoplayTimeout: 5000,
				margin: 20,
				nav: true,
				slideTransition: 'linear',
				dots: false,
				responsiveClass:true,
				responsive:{
					0:{
						items:1,
					},
					500:{
						items:2,
						
					},
					1000:{
						items:3,
					},
					1300:{
						items:3,
					}
				}
		
			});

			$("#employee-slider").owlCarousel({
				item:3,
				loop: true,
				autoplay: true,
				autoplayTimeout: 5000,
				margin: 20,
				nav: true,
				slideTransition: 'linear',
				dots: false,
				responsiveClass:true,
				responsive:{
					0:{
						items:1,
					},
					500:{
						items:2,
						
					},
					1000:{
						items:3,
					},
					1300:{
						items:3,
					}
				}
		
			});
			$("#cooking_competition").owlCarousel({
				item:3,
				loop: true,
				autoplay: true,
				autoplayTimeout: 5000,
				margin: 20,
				nav: true,
				slideTransition: 'linear',
				dots: false,
				responsiveClass:true,
				responsive:{
					0:{
						items:1,
					},
					500:{
						items:2,
						
					},
					1000:{
						items:3,
					},
					1300:{
						items:3,
					}
				}
		
			});
			$("#table_tennis_tournament").owlCarousel({
				item:3,
				loop: true,
				autoplay: true,
				autoplayTimeout: 5000,
				margin: 20,
				nav: true,
				slideTransition: 'linear',
				dots: false,
				responsiveClass:true,
				responsive:{
					0:{
						items:1,
					},
					500:{
						items:2,
						
					},
					1000:{
						items:3,
					},
					1300:{
						items:3,
					}
				}
		
			});

			  $(".custom_partner_slider").owlCarousel({
				loop: true,
				margin: 20,
				items: 7,
				nav: false,
				autoplay: false,
				autoplayHoverPause: true,
				responsive: {
				  0: {
					items: 2,
					margin:10
				  },
				  600: {
					items: 3
				  },
				  1000: {
					items: 5
				  },
				  1200: {
					items: 7
				  }
				}
		
			});
			$(".custom_partner_slider-1").owlCarousel({
				loop: true,
				margin: 20,
				items: 7,
				nav: false,
				autoplay: false,
				autoplayHoverPause: true,
				responsive: {
				  0: {
					items: 2
				  },
				  600: {
					items: 3
				  },
				  1000: {
					items: 5
				  },
				  1200: {
					items: 7
				  }
				}
		
			});
			$("#owl_animation").owlCarousel({
				center: true,
    			items:3,
    			loop:true,
    			margin:40,
    			responsive:{
    			    600:{
    			        items:4
    			    }
    			}
		
			});

            return this._super();
        },

		_onClickScrollToTop: function (ev) {
			ev.stopPropagation();
			ev.preventDefault();

			$('#wrapwrap').stop().animate({
				scrollTop: 0
			}, 2000, 'easeInOutExpo');
		},
	})
})