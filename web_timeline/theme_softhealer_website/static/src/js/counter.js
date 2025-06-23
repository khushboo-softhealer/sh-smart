odoo.define('sh_softhealer_theme.s_counter', function (require) {
    'use strict';
    
    
    
    
    
    
    
    var publicWidget = require('web.public.widget');
    var utils = require('web.utils');
    var registry = publicWidget.registry;
    var animations = require('website.content.snippets.animation');
    
    
    registry.CorpomateCounterWidget = animations.Animation.extend({
        selector: '.sh_project_counter, .sh_counter_section, #sh_custom_software_counter_section',	
        disabledInEditableMode: true,
        effects: [{
            startEvents: 'scroll',
            update: '_updateCounterOnScroll',
        }],
    
        /**
         * @constructor
         */
        init: function () {
            this._super(...arguments);
            this.HasCounted = false;
        },
    
        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------
        /**
         * Called when the window is scrolled
         *
         * @private
         * @param {integer} scroll
         */
        _updateCounterOnScroll: function (scroll) {    	
    
            var oTop = this.$el.offset().top - window.innerHeight;
              if (this.HasCounted == false && $(window).scrollTop() > oTop) {
                  //counter part start here
                  var looping = true;
            this.$el.find('.js_cls_counter_number').each(function () {
                       var $this = $(this);
                       looping = true;
                       jQuery({ Counter: 0 }).animate({ Counter: $this.text() }, {
                         duration: 8000,
                         easing: 'swing',
                         step: function () {
                           $this.text(Math.ceil(this.Counter));
                         }
                       });
                     }).promise().done( function(){
                         
                         looping = false;
                     });	  
                  //counter part ends here
                  this.HasCounted = true;
              }        
        },
    
    });
    
    
    
    });
    // var owl = $('.owl-carousel');
    // owl.owlCarousel({
    //     items:4,
    //     loop:true,
    //     margin:10,
    //     autoplay:true,
    //     autoplayTimeout:1000,
    //     autoplayHoverPause:true
    // });
    // $('.play').on('click',function(){
    //     // owl.trigger('play.owl.autoplay',[1000])
    // })
    // $('.stop').on('click',function(){
    //     // owl.trigger('stop.owl.autoplay')
    // })    
  