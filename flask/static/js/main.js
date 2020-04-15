/* =================================
------------------------------------
	Photo Gallery HTML Template
	Version: 1.0
 ------------------------------------
 ====================================*/


'use strict';


$(window).on('load', function() {
	/*------------------
		Preloder
	--------------------*/
	$(".loader").fadeOut();
	$("#preloder").delay(400).fadeOut("slow");
	$('#template').load("home", function() {
		$.getScript("static/js/page.js");
	});
});

(function($) {
	/*------------------
		Navigation
	--------------------*/
	$('.nav-switch-warp').on('click', function() {
		$('.header-section, .nav-switch').addClass('active');
		$('.main-warp').addClass('overflow-hidden');
	});

	$('.header-close').on('click', function() {
		$('.header-section, .nav-switch').removeClass('active');
		$('.main-warp').removeClass('overflow-hidden');
	});

	// Search model
	$('.search-switch').on('click', function() {
		$('.search-model').fadeIn(400);
	});

	$('.search-close-switch').on('click', function() {
		$('.search-model').fadeOut(400,function(){
			$('#search-input').val('');
		});
	});

	$('.menulink').on('click', function() {
		$('#template').load(this.id, function() {
			$.getScript("static/js/page.js");
		});
		$('.menulink').parents().find('li').removeClass('active'); //remove all the active classes
		$(this).parent().addClass('active'); //set the active class to all the li parents of the anchor element
		$('.header-close').click();
		
	});


	



	/*------------------
		Scrollbar
	--------------------*/
	if($(window).width() > 991) {
		$(".header-section").niceScroll({
			cursorborder:"",
			cursorcolor:"#afafaf",
			boxzoom:false,
			cursorwidth: 4,
		});
	}


})(jQuery);
