/* =================================
------------------------------------
	Photo Gallery HTML Template
	Version: 1.0
 ------------------------------------
 ====================================*/


'use strict';
	
    /*------------------
		Background Set
	--------------------*/
	$('.set-bg').each(function() {
		var bg = $(this).data('setbg');
        $(this).css('background-image', 'url(' + bg + ')');
        $(this).css('background-size:', 'cover');
    });
    
	/*------------------
		Hero Slider
	--------------------*/
	var hero_s = $(".hero-slider");
    hero_s.owlCarousel({
        loop: true,
        margin: 0,
        nav: true,
        items: 1,
        dots: false,
        animateOut: 'fadeOut',
    	animateIn: 'fadeIn',
        navText: ['<img src="./static/img/angle-left-w.png" alt="">', '<img src="./static/img/angle-rignt.png" alt="">'],
        smartSpeed: 1200,
        autoHeight: false,
		startPosition: 'URLHash',
        mouseDrag: false,
        onInitialized: function() {
        	var a = this.items().length;
        	if(a < 10){
            	$("#snh-1").html("<span>01" + "</span>/0" + a);
       		} else{
       			$("#snh-1").html("<span>01" + "</span>/" + a);
       		}
        }
    }).on("changed.owl.carousel", function(a) {
        var b = --a.item.index, a = a.item.count;
        if(a < 10){
        	$("#snh-1").html("<span>0" + ( 1 > b ? b + a : b > a ? b - a : b) + "</span>/0" + a);
    	} else{
    		$("#snh-1").html("<span> "+ (1 > b ? b + a : b > a ? b - a : b) + "</span>/" + a);
    	}
    });


	/*------------------
		Gallery Slider
	--------------------*/
	$('.gallery-single-slider').owlCarousel({
        loop: true,
        margin: 0,
        nav: true,
        items: 1,
        dots: false,
        navText: ['<img src="./static/img/angle-left.png" alt="">', '<img src="./static/img/angle-rignt-w.png" alt="">'],
	});


	/*------------------
		Isotope Filter
	--------------------*/
	var $container = $('.portfolio-gallery');
		$container.imagesLoaded().progress( function() {
			$container.isotope();
		});

	$('.portfolio-filter li').on("click", function(){
		$(".portfolio-filter li").removeClass("active");
		$(this).addClass("active");
		var selector = $(this).attr('data-filter');
		$container.imagesLoaded().progress( function() {
			$container.isotope({
				filter: selector,
			});
		});
		return false;
	});



	/*------------------
		Accordions
	--------------------*/
	$('.panel-link').on('click', function (e) {
		$('.panel-link').parent('.panel-header').removeClass('active');
		var $this = $(this).parent('.panel-header');
		if (!$this.hasClass('active')) {
			$this.addClass('active');
		}
		e.preventDefault();
	});


	/*------------------
		Circle progress
	--------------------*/
	$('.circle-progress').each(function() {
		var cpvalue = $(this).data("cpvalue");
		var cpcolor = $(this).data("cpcolor");
		var cptitle = $(this).data("cptitle");
		var cpid 	= $(this).data("cpid");

		$(this).append('<div class="'+ cpid +'"></div><div class="progress-info"><h2>'+ cpvalue +'%</h2><p>'+ cptitle +'</p></div>');

		if (cpvalue < 100) {

			$('.' + cpid).circleProgress({
				value: '0.' + cpvalue,
				size: 166,
				thickness: 5,
				fill: cpcolor,
				emptyFill: "rgba(0, 0, 0, 0)"
			});
		} else {
			$('.' + cpid).circleProgress({
				value: 1,
				size: 166,
				thickness: 5,
				fill: cpcolor,
				emptyFill: "rgba(0, 0, 0, 0)"
			});
		}

    });

    

	$(".blog-warp").niceScroll({
		cursorborder:"",
		cursorcolor:"#323232",
		boxzoom:false,
		cursorwidth: 3,
		autohidemode:false,
		background: '#b9c9da',
		cursorborderradius:0,
		railoffset: { top: 50, right: 0, left: 0, bottom: 0 },
		railpadding: { top: 0, right: 0, left: 0, bottom: 100 },

    });
    
    $('.action-btn').on('click', function() {
		$('#template').load(this.id, function() {
			$.getScript("static/js/page.js");
		});
    });

    $('.style-item').on('click', function() {
        $('.style-item').css("border","0px");
        $(this).css('border', '2px solid grey');

        var img_id = $(this).find('.thumbnail').attr('id');
        $('.style-single').html('<img src="static/img/styles/'+img_id+'.jpg" alt="">');
        $('#style-title').html(camelize(img_id));
    });

    function camelize(str) {
        str = str.charAt(0).toUpperCase() + str.slice(1);
        return str.replace(/_([a-z])/g, function (g) { return ' ' + g[1].toUpperCase(); });
    }

    $(document).ready( function() {
        $('.thumbnail').each(function(i) {
            $(this).parent().siblings("span").html(camelize(this.id));
        });
        
    });

    function updateProgress(){
        var bar = $('#bar');
        var p = $('#pbar');

        $(".form").hide();
        $(".wrapper").show();

        var width = $(".wrapper").width(); // the width of the wrapper can be set via CSS

        
        var interval;
        var start = 0; 
        var end = 100; //Percentage were the bar must end (value from 0 to 100)
        var current = start;
        
        // var calculate_percentage = (width / 100) * end

        
        var countUp = function() {
        // current++;
        // $('div.meter span').animate({width:end+"%"},11000); // Animation of the progress bar
        // p.html((current*100/width) + "%");

        // if (current === calculate_percentage) {
        //     clearInterval(interval);
        // }
            $.get('/progress').done(function(data){
                var json = JSON.parse(data);
                var n = json.progress;
                console.log(n);
                n = n / 5;  // percent value
                if (n >= 100) {
                    clearInterval(interval);
                    showVideo(); // user defined
                }
                $('div.meter span').animate({'width': n +'%'}).attr('aria-valuenow', n); 
                p.html(n + "%")   
            }).fail(function() {
                clearInterval(interval);
                displayerror(); // user defined
            });
        };
        interval = setInterval(countUp,1000); 
    }

    function showVideo(){
        $(".wrapper").hide();
        $(".video").show();
    }

    function resetPage(){
        $(".wrapper").hide();
        $(".video").hide();
        $(".form").show();
    }

    $('#percent').on('change',function (e) {
        console.log($(this).val());
        $("#percentval").html($(this).val()+"%");
    });

    $('#styleform').on('submit',function (e) {
        var formData = new FormData();

        formData.append('range', $("#percent").val());
        formData.append('video', $('#video')[0].files[0]);
        for (var pair of formData.entries()) {
            console.log(pair[0]+ ', ' + pair[1]); 
        }
        $.ajax({
            type: 'post',
            url: 'apply_style',
            processData: false,
            contentType: false,
            data: formData,
            success: function (q) {
                console.log(q);
                updateProgress();
            }
        });
        e.preventDefault();
        
    });
    
    
    