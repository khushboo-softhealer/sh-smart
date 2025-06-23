odoo.define('theme_softhealer_website.sh_cricket_tournament_player_filter', function (require) {
    "use strict";

    var concurrency = require("web.concurrency");
    var publicWidget = require('web.public.widget');
    var rpc = require('web.rpc'); // Import RPC for data fetching
    var _t = require('web.core')._t; // Translation utility

    publicWidget.registry.ShCricketPlayerFilter = publicWidget.Widget.extend({
        selector: ".sh_cricket_tournament_player_filter",
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
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self._initIsotope();
            });
        },

        /**
         * Initialize Isotope
         */
        _initIsotope: function () {
            var $grid = this.$('.grid').isotope({
                itemSelector: '.element-item',
                layoutMode: 'fitRows',
                // getSortData: {
                //     name: '.name',
                //     symbol: '.symbol',
                //     number: '.number parseInt',
                //     category: '[data-category]',
                //     weight: function(itemElem) {
                //         var weight = $(itemElem).find('.weight').text();
                //         return parseFloat(weight.replace(/[\(\)]/g, ''));
                //     }
                // }
            });

            // Filter functions
            var filterFns = {
                numberGreaterThan50: function() {
                    var number = $(this).find('.number').text();
                    return parseInt(number, 10) > 50;
                },
                ium: function() {
                    var name = $(this).find('.name').text();
                    return name.match(/ium$/);
                }
            };

            // Bind filter button click
            this.$('#filters').on('click', 'button', function() {
                var filterValue = $(this).attr('data-filter');
                filterValue = filterFns[filterValue] || filterValue;
                $grid.isotope({ filter: filterValue });
            });

            // // Bind sort button click
            // this.$('#sorts').on('click', 'button', function() {
            //     var sortByValue = $(this).attr('data-sort-by');
            //     $grid.isotope({ sortBy: sortByValue });
            // });

            // Change is-checked class on buttons
            this.$('.button-group').each(function(i, buttonGroup) {
                var $buttonGroup = $(buttonGroup);
                $buttonGroup.on('click', 'button', function() {
                    $buttonGroup.find('.is-checked').removeClass('is-checked');
                    $(this).addClass('is-checked');
                });
            });
        }
    });

    return publicWidget.registry.ShCricketPlayerFilter;
});

// odoo.define('theme_softhealer_website.sh_cricket_tournament_player_filter', function (require) {
//     "use strict";
//     alert("2")
//     var concurrency = require("web.concurrency");
//     const {Markup} = require('web.utils');

//     var publicWidget = require('web.public.widget');
//     var rpc = require('web.rpc'); // Import RPC for data fetching
//     var _t = require('web.core')._t; // Translation utility
    

//     publicWidget.registry.ShCricketPlayerFilter = publicWidget.Widget.extend({
        
//         selector: ".sh_cricket_tournament_player_filter",
       
//         disabledInEditableMode: true,
//         /**
//          * @constructor
//          */
//         init: function () {
//             this._super.apply(this, arguments);
//             this._dp = new concurrency.DropPrevious();

//         },
//         /**
//          * @override
//          */
//         start: function () {
//             // this._super.apply(this, arguments);
//             // this._dp.add(this._fetch()).then(this._render.bind(this));
//             // this.image_data = this._fetch()
//             // return this._super.apply(this, arguments);
//             $(document).ready(function() {
//                 // init Isotope
//                 console.log("--------------> 35",document);
//                 var $grid = $('.grid').isotope({
//                     itemSelector: '.element-item',
//                     layoutMode: 'fitRows',
//                     getSortData: {
//                         name: '.name',
//                         symbol: '.symbol',
//                         number: '.number parseInt',
//                         category: '[data-category]',
//                         weight: function(itemElem) {
//                             var weight = $(itemElem).find('.weight').text();
//                             return parseFloat(weight.replace(/[\(\)]/g, ''));
//                         }
//                     }
//                 });
            
//                 // filter functions
//                 var filterFns = {
//                     numberGreaterThan50: function() {
//                         var number = $(this).find('.number').text();
//                         return parseInt(number, 10) > 50;
//                     },
//                     ium: function() {
//                         var name = $(this).find('.name').text();
//                         return name.match(/ium$/);
//                     }
//                 };
            
//                 // bind filter button click
//                 $('#filters').on('click', 'button', function() {
//                     var filterValue = $(this).attr('data-filter');
//                     filterValue = filterFns[filterValue] || filterValue;
//                     $grid.isotope({ filter: filterValue });
//                 });
            
//                 // bind sort button click
//                 $('#sorts').on('click', 'button', function() {
//                     var sortByValue = $(this).attr('data-sort-by');
//                     $grid.isotope({ sortBy: sortByValue });
//                 });
            
//                 // change is-checked class on buttons
//                 $('.button-group').each(function(i, buttonGroup) {
//                     var $buttonGroup = $(buttonGroup);
//                     $buttonGroup.on('click', 'button', function() {
//                         $buttonGroup.find('.is-checked').removeClass('is-checked');
//                         $(this).addClass('is-checked');
//                     });
//                 });
//             });
//         },

         
//     });



//     return publicWidget.registry.ShCricketPlayerFilter;
// });
