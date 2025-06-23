odoo.define('theme_mobiheal_website.custom_header_mobiheal', function (require) {
    'use strict';
    
    var publicWidget = require('web.public.widget');
	var animations = require('website.content.snippets.animation');
    
    
    publicWidget.registry.js_cls_sh_custom_header_mobiheal = publicWidget.Widget.extend({
        
        selector: '.js_cls_sh_custom_mobiheal_wrapper, .js_cls_sh_custom_mobiheal_new_wrapper',
        disabledInEditableMode: true,

        events: {
			'click .js_cls_custom_header_btn':'_onClickCustomHeaderBtn',
			'click .navbar-toggler':'_onClickCustomHeaderNewBtn',
        },
        
		/**
         * @constructor
         */
		init: function () {
			var self = this
			
			return this._super.apply(this, arguments);
		},

		/**
         * @override
         */
        start: function () {
			var self = this
			self.$el.find('#top_menu').addClass('hideMenu')
            return this._super.apply(this, arguments);
        },
    
        
        _onClickCustomHeaderBtn: function (ev) {
			var self = this
			var $btn = $(ev.currentTarget);
			$btn.toggleClass('active')
			var $liList = self.$el.find('#top_menu li')
			self.$el.find('#top_menu').toggleClass('hideMenu showMenu');
			var screensize = document.documentElement.clientWidth;
			
			var arr = [];
			
			for( var name in $liList ) {
			    arr[name] = $liList[name];
			}
			
			var len = arr.length;
			var right = 30
			var bottom = 10
			while( len-- ) {
				if(screensize && screensize >= 992){
					if (self.$el.find('#top_menu').hasClass('showMenu')){
					    if( arr[len] !== undefined ) {
							if (screensize && screensize > 1024){
								right = right + 100
								$(arr[len]).animate({'right':right+'px','opacity':'1','z-index':'8'},500);
							}
							if (screensize && screensize <= 1024){
								right = right + 90
								$(arr[len]).animate({'right':right+'px','opacity':'1','z-index':'8'},500);
							}

					    }
					}
					else{
						if( arr[len] !== undefined ) {
							right = right + 100
							$(arr[len]).animate({'right':'100','opacity':'0','z-index':'8'},500);
					    }
					}
				}
				else{
					if (self.$el.find('#top_menu').hasClass('showMenu')){
					    if( arr[len] !== undefined ) {
							bottom = bottom + 100
							$(arr[len]).animate({'bottom':bottom+'px','opacity':'1','z-index':'8'},500);
					    }
					}
					else{
						if( arr[len] !== undefined ) {
							bottom = bottom + 100
							$(arr[len]).animate({'bottom':'100','opacity':'0','z-index':'8'},500);
					    }
					}
				}
			}
		},

		_onClickCustomHeaderNewBtn: function (ev) {
			var self = this
			var $btn = $(ev.currentTarget);
			$btn.toggleClass('active')
		}
    });




	publicWidget.registry.theme_mobiheal_website_custom_scroll_js = animations.Animation.extend({
        selector: "#wrapwrap",
        disabledInEditableMode: true,
        effects: [{
            startEvents: 'scroll',
            update: '_on_scroll_check_header_classes',
        }],

        //--------------------------------------------------------------------------
        /**
         * Called when the window is scrolled
         *
         * @private
         * @param {integer} scroll
         */
		 _on_scroll_check_header_classes: function (scroll) {
            var self = this;
			if ($('.js_cls_sh_custom_mobiheal_new_wrapper .navbar-toggler').hasClass('active')){
				$('.js_cls_sh_custom_mobiheal_new_wrapper .navbar-toggler').removeClass('active')
			}
		},


    });
    
});