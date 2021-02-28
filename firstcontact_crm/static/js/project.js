/* Project specific Javascript goes here. */
/*!
    * Start Bootstrap - Freelancer v6.0.5 (https://startbootstrap.com/theme/freelancer)
    * Copyright 2013-2020 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-freelancer/blob/master/LICENSE)
    */
   (function($) {
    "use strict"; // Start of use strict

    // // Smooth scrolling using jQuery easing
    // $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function() {
    //   if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
    //     var target = $(this.hash);
    //     target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
    //     if (target.length) {
    //       $('html, body').animate({
    //         scrollTop: (target.offset().top - 71)
    //       }, 1000, "easeInOutExpo");
    //       return false;
    //     }
    //   }
    // });

    // // Scroll to top button appear
    // $(document).scroll(function() {
    //   var scrollDistance = $(this).scrollTop();
    //   if (scrollDistance > 100) {
    //     $('.scroll-to-top').fadeIn();
    //   } else {
    //     $('.scroll-to-top').fadeOut();
    //   }
    // });

    // Closes responsive menu when a scroll trigger link is clicked
     // Toggle the side navigation
  // $("#sidebarToggle, #sidebarToggleTop").on('click', function(e) {
  //   $("body").toggleClass("sidebar-toggled");
  //   $(".sidebar").toggleClass("toggled");
  //   if ($(".sidebar").hasClass("toggled")) {
  //     $('.sidebar .collapse').collapse('hide');
  //   };
  // });

  $("#sidebarToggle, #sidebarToggleTop").click(function(e) {
    $("body").toggleClass("sidebar-toggled");
    $(".sidebar").toggleClass("toggled");
    if ($(".sidebar").hasClass("toggled")) {
      $('.sidebar .collapse').collapse('hide');
    };
  });
  
  // Close any open menu accordions when window is resized below 768px
  $(window).resize(function() {
    if ($(window).width() < 768) {
      $('.sidebar .collapse').collapse('hide');
    };
    
    // Toggle the side navigation when window is resized below 480px
    if ($(window).width() < 480 && !$(".sidebar").hasClass("toggled")) {
      $("body").addClass("sidebar-toggled");
      $(".sidebar").addClass("toggled");
      $('.sidebar .collapse').collapse('hide');
    };
  });

  // Prevent the content wrapper from scrolling when the fixed side navigation hovered over
  $('body.fixed-nav .sidebar').on('mousewheel DOMMouseScroll wheel', function(e) {
    if ($(window).width() > 768) {
      var e0 = e.originalEvent,
        delta = e0.wheelDelta || -e0.detail;
      this.scrollTop += (delta < 0 ? 1 : -1) * 30;
      e.preventDefault();
    }
  });

  // Scroll to top button appear
  $(document).on('scroll', function() {
    var scrollDistance = $(this).scrollTop();
    if (scrollDistance > 100) {
      $('.scroll-to-top').fadeIn();
    } else {
      $('.scroll-to-top').fadeOut();
    }
  });

  // Smooth scrolling using jQuery easing
  $(document).on('click', 'a.scroll-to-top', function(e) {
    var $anchor = $(this);
    $('html, body').stop().animate({
      scrollTop: ($($anchor.attr('href')).offset().top)
    }, 1000, 'easeInOutExpo');
    e.preventDefault();
  });

  $(document).ready(function() {
    function triggerClick(elem) {
        $(elem).click();
    }
    var $progressWizard = $('.stepper'),
        $tab_active,
        $tab_prev,
        $tab_next,
        $btn_prev = $progressWizard.find('.prev-step'),
        $btn_next = $progressWizard.find('.next-step'),
        $tab_toggle = $progressWizard.find('[data-toggle="tab"]'),
        $tooltips = $progressWizard.find('[data-toggle="tab"][title]');

    // To do:
    // Disable User select drop-down after first step.
    // Add support for payment type switching.

    //Initialize tooltips
    $tooltips.tooltip();

    //Wizard
    $tab_toggle.on('show.bs.tab', function(e) {
        var $target = $(e.target);

        if (!$target.parent().hasClass('active, disabled')) {
            $target.parent().prev().addClass('completed');
        }
        if ($target.parent().hasClass('disabled')) {
            return false;
        }
    });

    // $tab_toggle.on('click', function(event) {
    //     event.preventDefault();
    //     event.stopPropagation();
    //     return false;
    // });

    $btn_next.on('click', function() {
        $tab_active = $progressWizard.find('.active');

        $tab_active.next().removeClass('disabled');

        $tab_next = $tab_active.next().find('a[data-toggle="tab"]');
        triggerClick($tab_next);

    });
    $btn_prev.click(function() {
        $tab_active = $progressWizard.find('.active');
        $tab_prev = $tab_active.prev().find('a[data-toggle="tab"]');
        triggerClick($tab_prev);
    });
});  
    // $('.js-scroll-trigger').click(function() {
    //   $('.navbar-collapse').collapse('hide');
    // });

    // // Activate scrollspy to add active class to navbar items on scroll
    // $('body').scrollspy({
    //   target: '#mainNav',
    //   offset: 80
    // });

    // Collapse Navbar
    // var navbarCollapse = function() {
    //   if ($("#mainNav").offset().top > 100) {
    //     $("#mainNav").addClass("navbar-shrink");
    //   } else {
    //     $("#mainNav").removeClass("navbar-shrink");
    //   }
    // };
    // // Collapse now if page is not at top
    // navbarCollapse();
    // // Collapse the navbar when page is scrolled
    // $(window).scroll(navbarCollapse);

    // // Floating label headings for the contact form
    // $(function() {
    //   $("body").on("input propertychange", ".floating-label-form-group", function(e) {
    //     $(this).toggleClass("floating-label-form-group-with-value", !!$(e.target).val());
    //   }).on("focus", ".floating-label-form-group", function() {
    //     $(this).addClass("floating-label-form-group-with-focus");
    //   }).on("blur", ".floating-label-form-group", function() {
    //     $(this).removeClass("floating-label-form-group-with-focus");
    //   });
    // });

    $(document).ready(function () {
      $('.stepper').mdbStepper();
      })
      
      function someFunction21() {
      setTimeout(function () {
      $('#horizontal-stepper').nextStep();
      }, 2000);
    }

  })(jQuery); // End of use strict
