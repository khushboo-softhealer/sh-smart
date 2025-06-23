
odoo.define('theme_softhealer_website.home_page_slider', function (require) {
    'use strict';

    const publicWidget = require('web.public.widget');

    publicWidget.registry.home_page_slider = publicWidget.Widget.extend({
        selector: ".home_page_slider",

        start() {
            return this._super(...arguments);
        },

        async willStart() {
            // Load Libs
            try {
                await loadJS(
                    'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js',
                    'https://cdnjs.cloudflare.com/ajax/libs/OwlCarousel2/2.2.1/owl.carousel.min.js'
                );
                await loadCSS(
                    'https://cdnjs.cloudflare.com/ajax/libs/OwlCarousel2/2.2.1/assets/owl.carousel.min.css',
                    'https://cdnjs.cloudflare.com/ajax/libs/OwlCarousel2/2.2.1/assets/owl.theme.default.min.css'
                );
            } catch (error) {
                console.error('Error:', error);
            }

            var sync1 = $("#sync1");
            var sync2 = $("#sync2");
            var slidesPerPage = 6; // globally define number of elements per page
            var syncedSecondary = true;

            sync1.owlCarousel({
                items: 1,
                slideSpeed: 2000,
                nav: true,
                autoplay: false,
                dots: true,
                loop: true,
                responsiveRefreshRate: 200,
            }).on('changed.owl.carousel', syncPosition);

            sync2
                .on('initialized.owl.carousel', function () {
                    sync2.find(".owl-item").eq(0).addClass("current");
                })
                .owlCarousel({
                    items: slidesPerPage,
                    dots: true,
                    nav: true,
                    smartSpeed: 200,
                    slideSpeed: 500,
                    slideBy: slidesPerPage,
                    responsiveRefreshRate: 100,
                    loop: true, // Ensure loop is enabled for smooth reordering
                })
                .on('changed.owl.carousel', syncPosition2);

            function syncPosition(el) {
                // Calculate the current item index, accounting for loop
                var count = el.item.count - 1;
                var current = Math.round(el.item.index - (el.item.count / 2) - 0.5);

                // Ensure current index stays within loop bounds
                if (current < 0) {
                    current = count;
                }
                if (current > count) {
                    current = 0;
                }

                // Update the current class in sync2
                sync2
                    .find(".owl-item")
                    .removeClass("current")
                    .eq(current)
                    .addClass("current");

                // Scroll sync2 so the current item is at the first position
                sync2.data('owl.carousel').to(current, 100, true);
            }

            function syncPosition2(el) {
                if (syncedSecondary) {
                    var number = el.item.index;
                    sync1.data('owl.carousel').to(number, 100, true);
                }
            }

            sync2.on("click", ".owl-item", function (e) {
                e.preventDefault();
                var number = $(this).index();
                sync1.data('owl.carousel').to(number, 300, true);
            });
        },
    });
});






















// odoo.define('theme_softhealer_website.home_page_slider', function (require) {
//     'use strict';

//     const publicWidget = require('web.public.widget');

//     publicWidget.registry.home_page_slider = publicWidget.Widget.extend({
//         selector: ".home_page_slider",

//         start() {
//             // this._bindCategoryButtons();
//             return this._super(...arguments);
//         },

//         async willStart() {
//             // Load Libs
//             console.log("--------------> 16 will start called",);
//             try {

//                 await loadJS('https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js','https://cdnjs.cloudflare.com/ajax/libs/OwlCarousel2/2.2.1/owl.carousel.min.js');
//                 // await loadJS('https://cdnjs.cloudflare.com/ajax/libs/OwlCarousel2/2.2.1/owl.carousel.min.js');

//                 await loadCSS('https://cdnjs.cloudflare.com/ajax/libs/OwlCarousel2/2.2.1/assets/owl.carousel.min.css','https://cdnjs.cloudflare.com/ajax/libs/OwlCarousel2/2.2.1/assets/owl.theme.default.min.css');
//             } catch (error) {
//                 console.error('Error:', error);
//             }
            

//             var sync1 = $("#sync1");
//             var sync2 = $("#sync2");
//             console.log("--------------> 30 sync1",sync1);
//             console.log("--------------> 31 sync2",sync2);
//             var slidesPerPage = 4; //globaly define number of elements per page
//             var syncedSecondary = true;
          
//             sync1.owlCarousel({
//               items : 1,
//               slideSpeed : 2000,
//               nav: true,
//               autoplay: false,
//               dots: true,
//               loop: true,
//               responsiveRefreshRate : 200,
          
//             }).on('changed.owl.carousel', syncPosition);
          
//             sync2
//               .on('initialized.owl.carousel', function () {
//                 sync2.find(".owl-item").eq(0).addClass("current");
//               })
//               .owlCarousel({
//               items : slidesPerPage,
//               dots: true,
//               nav: true,
//               smartSpeed: 200,
//               slideSpeed : 500,
//               slideBy: slidesPerPage, //alternatively you can slide by 1, this way the active slide will stick to the first item in the second carousel
//               responsiveRefreshRate : 100
//             }).on('changed.owl.carousel', syncPosition2);
          
//             function syncPosition(el) {
//               //if you set loop to false, you have to restore this next line
//               //var current = el.item.index;
              
//               //if you disable loop you have to comment this block
//               var count = el.item.count-1;
//               var current = Math.round(el.item.index - (el.item.count/2) - .5);
              
//               if(current < 0) {
//                 current = count;
//               }
//               if(current > count) {
//                 current = 0;
//               }
              
//               //end block
          
//               sync2
//                 .find(".owl-item")
//                 .removeClass("current")
//                 .eq(current)
//                 .addClass("current");
//               var onscreen = sync2.find('.owl-item.active').length - 1;
//               var start = sync2.find('.owl-item.active').first().index();
//               var end = sync2.find('.owl-item.active').last().index();
              
//               if (current > end) {
//                 sync2.data('owl.carousel').to(current, 100, true);
//               }
//               if (current < start) {
//                 sync2.data('owl.carousel').to(current - onscreen, 100, true);
//               }
//             }
            
//             function syncPosition2(el) {
//               if(syncedSecondary) {
//                 var number = el.item.index;
//                 sync1.data('owl.carousel').to(number, 100, true);
//               }
//             }
            
//             sync2.on("click", ".owl-item", function(e){
//               e.preventDefault();
//               var number = $(this).index();
//               sync1.data('owl.carousel').to(number, 300, true);
//             });



//         },
        
//     });
// });







// odoo.define('theme_softhealer_website.home_page_slider', function (require) {
//     'use strict';

//     const publicWidget = require('web.public.widget');

//     publicWidget.registry.home_page_slider = publicWidget.Widget.extend({
//         selector: ".home_page_slider",

//         start() {
//             this._bindCategoryButtons();
//             return this._super(...arguments);
//         },

//         // 33333333333333333333333333333333333 
//         _bindCategoryButtons() {
//              const container = this.el.querySelector('.category-buttons-container');
//             const buttons = container.querySelectorAll('.category-button');

//             // Duplicate buttons to simulate infinite loop
//             buttons.forEach(btn => {
//                 const clone = btn.cloneNode(true);
//                 clone.classList.add('clone');
//                 container.appendChild(clone);
//             });

//             const allButtons = container.querySelectorAll('.category-button');

//             allButtons.forEach((btn, index) => {
//                 btn.addEventListener('click', (e) => {
//                     // Remove all active
//                     allButtons.forEach(b => b.classList.remove('active'));
//                     btn.classList.add('active');
//                     console.log("--------------> 32",btn);

//                     // Scroll to make clicked button first
//                     const containerLeft = container.getBoundingClientRect().left;
//                     const buttonLeft = btn.getBoundingClientRect().left;
//                     const offset = buttonLeft - containerLeft;
                    
//                     const current = e.currentTarget;
//                     //             current.classList.add('active');
//                     const id = current.dataset.id;
//                     console.log("--------------> 42 id",id);
//                     const allDataText = document.querySelectorAll('.data-text');
//                     allDataText.forEach(txt => txt.classList.remove('active'));
//                     const selectedText = document.getElementById(id);
//                     if (selectedText) {
//                         console.log("--------------> 47selectedText",selectedText);
//                         selectedText.classList.add('active');
//                     }
//                     container.scrollBy({
//                         left: offset,
//                         behavior: 'smooth'
//                     });

//                     // Simulate wrap after reaching original + clones
//                     if (index >= buttons.length) {
//                         // Delay reset scroll to original set
//                         setTimeout(() => {
//                             container.scrollLeft = 0;
//                         }, 350);
//                     }
//                 });
//             });
//         },





        
//     });
// });
