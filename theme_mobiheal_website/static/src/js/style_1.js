
$(document).ready(function(){

$('.owl-carousel.mb_app_screenshots_slider').owlCarousel({
  center: true,
  items: 5,
  loop: true,
  margin: 10,
  dot: true,
  nav: false,
  autoplay:true,
  autoplayTimeout:3000,
  responsive: {
      0: {
          items: 1,
          nav: false,
      },
      600: {
          items: 3,
          nav: false,
      },
      1000: {
          items: 4,
          nav: false,
      },
      1500: {
          items: 5,
          nav: false,
      }
  }

  
});

$(function() {
    // Owl Carousel
    var owl = $(".owl-carousel");
    owl.owlCarousel({
      items: 1,
      margin: 10,
      loop: true,
      nav: true
    });
  });

  

  var swiper = new Swiper('.mb_product_slider', {
    spaceBetween: 30,
    effect: 'fade',
    // initialSlide: 2,
    loop: true,
    autoplay: 
    {
      delay: 9000,
    },
  mousewheel: 
		{
			invert: true,
		},
    navigation: {
        nextEl: '.next',
        prevEl: '.prev'
    },
    // mousewheel: {
    //     // invert: false
    // },
    on: {
        init: function(){
            var index = this.activeIndex;

            var target = $('.mb_product_slider_item').eq(index).data('target');
            $('.mb_banner_img_item').removeClass('active');
            $('.mb_banner_img_item#'+ target).addClass('active');
        }
    }

});

swiper.on('slideChange', function () {
    var index = this.activeIndex;

    var target = $('.mb_product_slider_item').eq(index).data('target');

    $('.mb_banner_img_item').removeClass('active');
    $('.mb_banner_img_item#'+ target).addClass('active');

    if(swiper.isEnd) {
        $('.prev').removeClass('disabled');
        $('.next').addClass('disabled');
    } else {
        $('.next').removeClass('disabled');
    }

    if(swiper.isBeginning) {
        $('.prev').addClass('disabled');
    } else {
        $('.prev').removeClass('disabled');
    }
});

$(".js-fav").on("click", function() {
    $(this).find('.heart').toggleClass("is-active");
});
});




