(function($) {
  
  "use strict";

  // Preloader
  function stylePreloader() {
    $('body').addClass('preloader-deactive');
  }

  // Header Sticky Js
  var varWindow = $(window);
  varWindow.on('scroll', function(event) {
    var scroll = varWindow.scrollTop();
    if (scroll < 350) {
      $(".sticky-header").removeClass("sticky");
    } else{
      $(".sticky-header").addClass("sticky");
    }
  });

  // Background Image
  const bgSelector = $("[data-bg-img]");
  bgSelector.each(function (index, elem) {
    let element = $(elem),
      bgSource = element.data('bg-img');
    element.css('background-image', 'url(' + bgSource + ')');
  });

  // Width
  $('[data-width]').each(function() {
    $(this).css('width', $(this).data("width"));
  });
  // Margin Top
  $('[data-margin-top]').each(function() {
    $(this).css('margin-top', $(this).data("margin-top"));
  });
  // Margin Bottom
  $('[data-margin-bottom]').each(function() {
    $(this).css('margin-bottom', $(this).data("margin-bottom"));
  });
  // Padding Top
  $('[data-padding-top]').each(function() {
    $(this).css('padding-top', $(this).data("padding-top"));
  });
  // Padding Bottom
  $('[data-padding-bottom]').each(function() {
    $(this).css('padding-bottom', $(this).data("padding-bottom"));
  });

  // Off Canvas JS
  var canvasWrapper = $(".off-canvas-wrapper");
  $(".btn-menu").on('click', function() {
    canvasWrapper.addClass('active');
    $("body").addClass('fix');
  });

  $(".close-action > .btn-menu-close, .off-canvas-overlay").on('click', function() {
    canvasWrapper.removeClass('active');
    $("body").removeClass('fix');
  });

  //Responsive Slicknav JS
  $('.main-menu').slicknav({
    appendTo: '.res-mobile-menu',
    closeOnClick: false,
    removeClasses: true,
    closedSymbol: '<i class="ion-ios-add"></i>',
    openedSymbol: '<i class="ion-ios-remove"></i>'
  });

  // Menu Activeion Js
  var cururl = window.location.pathname;
  var curpage = cururl.substr(cururl.lastIndexOf('/') + 1);
  var hash = window.location.hash.substr(1);
  if((curpage == "" || curpage == "/" || curpage == "admin") && hash=="")
    {
    } else {
      $(".header-navigation-area li").each(function()
    {
      $(this).removeClass("active");
    });
    if(hash != "")
      $(".header-navigation-area li a[href*='"+hash+"']").parents("li").addClass("active");
    else
    $(".header-navigation-area li a[href*='"+curpage+"']").parents("li").addClass("active");
  }

  // Search Box  JS
  $(".btn-search").on('click', function() {
    $(".btn-search-content").toggleClass("show").focus();
  });

  // Popup Quick View JS
  var popupProduct = $(".popup-product-quickview");
  $(".btn-quick-view").on('click', function() {
    popupProduct.addClass('active');
    $(".popup-product-overlay").addClass('active');
    $(".popup-product-close").addClass('active');
    $("body").addClass("fix");
  });
  $(".popup-product-overlay,.popup-product-close").on('click', function() {
    popupProduct.removeClass('active');
    $(".popup-product-overlay").removeClass('active');
    $(".popup-product-close").removeClass('active');
    $("body").removeClass("fix");
  });

  // Hero Slider Js
    var carouselSlider = new Swiper('.default-slider-container', {
      slidesPerView : 1,
      slidesPerGroup: 1,
      loop: true,
      speed: 500,
      spaceBetween: 0,
      autoplay: false,
      effect: 'fade',
      fadeEffect: {
        crossFade: true,
      },
      pagination: {
        el: '.swiper-pagination',
        clickable: true,
        type: 'bullets',
      },
    });

  // Swiper Slider Js

    // Product Single Thumb Slider Js
      var ProductNav = new Swiper('.single-product-nav-slider', {
        spaceBetween: 10,
        slidesPerView: 4,
        freeMode: true,
      });
      var ProductThumb = new Swiper('.single-product-thumb-slider', {
        freeMode: true,
        effect: 'fade',
        fadeEffect: {
          crossFade: true,
        },
        thumbs: {
          swiper: ProductNav
        }
      });

    // Product Single Thumb Slider2 Js
      var ProductNav2 = new Swiper('.single-product-nav-slider2', {
        spaceBetween: 10,
        slidesPerView: 4,
        freeMode: true,
      });
      var ProductThumb2 = new Swiper('.single-product-thumb-slider2', {
        freeMode: true,
        effect: 'fade',
        fadeEffect: {
          crossFade: true,
        },
        thumbs: {
          swiper: ProductNav2
        }
      });

  // Owl Slider Js

      // Image Slider Js
        var product = $(".images-col3-slider");
        product.owlCarousel({
          autoplay: false,
          smartSpeed: 1000,
          nav: false,
          dots: false,
          margin: 30,
          responsive: {
            0: {
              items: 1,
            },
            540: {
              items: 2,
              margin: 15,
            },
            576: {
              items: 2,
              margin: 15,
            },
            768: {
              items: 3,
            },
            992: {
              items: 3,
            },
            1200: {
              items: 3,
            }
          }
        });

      // Product Slider Js
        var product = $(".product-slider");
        product.owlCarousel({
          autoplay: false,
          smartSpeed: 1000,
          nav: true,
          dots: false,
          margin: 0,
          responsive: {
            0: {
              items: 1,
            },
            540: {
              items: 2,
            },
            576: {
              items: 2,
            },
            768: {
              items: 3,
            },
            992: {
              items: 3,
            },
            1200: {
              items: 4,
            }
          }
        });

      // Product Col2 Slider Js
        var product = $(".product-col2-slider");
        product.owlCarousel({
          autoplay: false,
          smartSpeed: 1000,
          nav: true,
          dots: false,
          margin: 0,
          responsive: {
            0: {
              items: 1,
            },
            540: {
              items: 2,
            },
            576: {
              items: 2,
            },
            768: {
              items: 3,
            },
            992: {
              items: 2,
            },
            1200: {
              items: 2,
            }
          }
        });

      // Product Col2 Slider Js
        var product = $(".product-col4-slider");
        product.owlCarousel({
          autoplay: false,
          smartSpeed: 1000,
          nav: true,
          dots: false,
          margin: 0,
          responsive: {
            0: {
              items: 1,
            },
            480: {
              items: 1,
            },
            576: {
              items: 2,
            },
            768: {
              items: 2,
            },
            992: {
              items: 3,
            },
            1200: {
              items: 4,
            }
          }
        });

      // Product Discount Slider Js
        var productcategories = $(".discount-product-slider");
        productcategories.owlCarousel({
          autoplay: false,
          smartSpeed: 1000,
          nav: true,
          dots: false,
          margin: 15,
          responsive: {
            0: {
              items: 1,
            },
            576: {
              items: 2,
            },
            768: {
              items: 2,
            },
            992: {
              items: 3,
            },
            1400: {
              items: 1,
            }
          }
        });

      // Product Categorys Col5 Slider Js
        var productcategories = $(".product-categorys-col5-slider");
        productcategories.owlCarousel({
          autoplay: false,
          smartSpeed: 1000,
          nav: true,
          dots: false,
          margin: 30,
          responsive:{
            0:{
              items:1,
            },
            480:{
              items:2,
              margin: 15,
            },
            576:{
              items:2,
      
            },
            768:{
              items:3,
            },
            992:{
              items:4,
            },
            1200:{
              items:5,
            }
          }
        });

      // Product Categorys Slider Js
        var productcategories = $(".product-categorys-slider");
        productcategories.owlCarousel({
          autoplay: false,
          smartSpeed: 1000,
          nav: true,
          dots: false,
          margin: 30,
          responsive: {
            0: {
              items: 1,
            },
            576: {
              items: 2,
            },
            768: {
              items: 3,
            },
            992: {
              items: 4,
            },
            1200: {
              items: 4,
            }
          }
        });

      // Testimonials Slider Js
        var testi = $(".testimonials-slider");
        testi.on('changed.owl.carousel initialized.owl.carousel', function(event) {
        $(event.target)
          .eq(event.item.index).addClass('firstActiveItem');
          }).owlCarousel({
          autoplay:false,
          autoplayHoverPause: true,
          smartSpeed: 1000,
          nav:true,
          dots: false,
          margin: 30,
          responsiveClass: true,
          responsive : {
            0 : {
                  items: 1,
              }, 
            360 : {
                  items: 1,
              },
              576 : {
                  items: 1,
              },
              768 : {
                  items: 1,
              },
              992 : {
                  items:2,
              },
            1200 : {
                  items: 2,
              }
          }
        });

      // Blog Slider Js
        var blog = $(".blog-slider");
        blog.owlCarousel({
          autoPlay: false,
          smartSpeed: 1000,
          nav: true,
          dots: false,
          margin: 30,
          responsive: {
            0: {
              items: 1,
            },
            480: {
              items: 1,
            },
            768: {
              items: 2,
            },
            992: {
              items: 2,
            },
            1200: {
              items: 3,
            }
          }
        });

  // Product Quantity JS
  var proQty = $(".pro-qty");
  proQty.append('<div class="inc qty-btn"><i class="fa fa-angle-up"></i></div>');
  proQty.append('<div class= "dec qty-btn"><i class="fa fa-angle-down"></i></div>');
  $('.qty-btn').on('click', function (e) {
    e.preventDefault();
    var $button = $(this);
    var oldValue = $button.parent().find('input').val();
    if ($button.hasClass('inc')) {
      var newVal = parseFloat(oldValue) + 1;
    } else {
      // Don't allow decrementing below zero
      if (oldValue > 1) {
        var newVal = parseFloat(oldValue) - 1;
      } else {
        newVal = 1;
      }
    }
    $button.parent().find('input').val(newVal);
  });

  // Fancybox Js
  $('.lightbox-image').fancybox();

  // Images Zoom
  $('.zoom-hover').zoom();

  //Match Height Js
  $(".matchHeight").matchHeight();

  // Countdown Js 
  $(".ht-countdown").each(function(index, element) {
    var $element = $(element),
    $date = $element.data('date');
    $element.countdown($date, function(event) {
      var $this = $(this).html(event.strftime(''
      +
      '<div class="countdown-item"><span class="countdown-item__time">%D</span><span class="countdown-item__label">Days</span></div>' +
      '<div class="countdown-item"><span class="countdown-item__time">%H</span><span class="countdown-item__label">Hours</span></div>' +
      '<div class="countdown-item"><span class="countdown-item__time">%M</span><span class="countdown-item__label">Mins</span></div>' +
      '<div class="countdown-item"><span class="countdown-item__time">%S</span><span class="countdown-item__label">Secs</span></div>'));
    });
  });

  // Ajax Contact Form JS
  var form = $('#contact-form');
  var formMessages = $('.form-message');

  $(form).submit(function(e) {
    e.preventDefault();
    var formData = form.serialize();
    $.ajax({
      type: 'POST',
      url: form.attr('action'),
      data: formData
    }).done(function(response) {
      // Make sure that the formMessages div has the 'success' class.
      $(formMessages).removeClass('alert alert-danger');
      $(formMessages).addClass('alert alert-success fade show');

      // Set the message text.
      formMessages.html("<button type='button' class='btn-close' data-bs-dismiss='alert'>&times;</button>");
      formMessages.append(response);

      // Clear the form.
      $('#contact-form input,#contact-form textarea').val('');
    }).fail(function(data) {
      // Make sure that the formMessages div has the 'error' class.
      $(formMessages).removeClass('alert alert-success');
      $(formMessages).addClass('alert alert-danger fade show');

      // Set the message text.
      if (data.responseText !== '') {
        formMessages.html("<button type='button' class='btn-close' data-bs-dismiss='alert'>&times;</button>");
        formMessages.append(data.responseText);
      } else {
        $(formMessages).text('Oops! An error occurred and your message could not be sent.');
      }
    });
  });

  function scrollToTop() {
    var $scrollUp = $('#scroll-to-top'),
      $lastScrollTop = 0,
      $window = $(window);
      $window.on('scroll', function () {
      var st = $(this).scrollTop();
        if (st > $lastScrollTop) {
            $scrollUp.removeClass('show');
        } else {
          if ($window.scrollTop() > 120) {
            $scrollUp.addClass('show');
          } else {
            $scrollUp.removeClass('show');
          }
        }
        $lastScrollTop = st;
    });
    $scrollUp.on('click', function (evt) {
      $('html, body').animate({scrollTop: 0}, 50);
      evt.preventDefault();
    });
  }
  scrollToTop();
  
/* ==========================================================================
   When document is loading, do
   ========================================================================== */
  
  varWindow.on('load', function() {
    stylePreloader();
  });

})(window.jQuery);