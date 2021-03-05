/* ----- Custom Scripts for Destiny template ----- */

$(document).ready(function () {
  $('[data-toggle="tooltip"]').tooltip();
});
// get the value of the bottom of the #main element by adding the offset of that element plus its height, set it as a variable
var mainbottom = $('#main').offset().top;

// on scroll,
$(window).on('scroll', function () {

  // we round here to reduce a little workload
  stop = Math.round($(window).scrollTop());
  if (stop > mainbottom) {
    $('.navbar').addClass('past-main');
    $('.navbar').addClass('effect-main')
  } else {
    $('.navbar').removeClass('past-main');
  }

});

// Collapse navbar on click

$(document).on('click.nav', '.navbar-collapse.in', function (e) {
  if ($(e.target).is('a')) {
    $(this).removeClass('in').addClass('collapse');
  }
});

/* ------ jQuery for Easing min -- */

$(function () {
  $('a.page-scroll').bind('click', function (event) {
    var $anchor = $(this);
    $('html, body').stop().animate({
      scrollTop: $($anchor.attr('href')).offset().top
    }, 1500, 'easeInOutExpo');
    event.preventDefault();
  });
});

/* --------- Wow Init -------*/

new WOW().init();


$(".animsition").animsition({
  inClass: 'fade-in',
  outClass: 'fade-out',
  inDuration: 1500,
  outDuration: 800,
  linkElement: '.animsition-link',
  // e.g. linkElement: 'a:not([target="_blank"]):not([href^="#"])'
  loading: true,
  loadingParentElement: 'body', //animsition wrapper element
  loadingClass: 'animsition-loading',
  loadingInner: '', // e.g '<img src="loading.svg" />'
  timeout: false,
  timeoutCountdown: 5000,
  onLoadEvent: true,
  browser: ['animation-duration', '-webkit-animation-duration'],
  // "browser" option allows you to disable the "animsition" in case the css property in the array is not supported by your browser.
  // The default setting is to disable the "animsition" in a browser that does not support "animation-duration".
  overlay: false,
  overlayClass: 'animsition-overlay-slide',
  overlayParentElement: 'body',
  transition: function (url) {
    window.location.href = url;
  }
});

$('#subscribe').submit(function (e) {
  e.preventDefault();
  var email_id = $("#email_id").val();
  if (email_id) {
    var csrfmiddlewaretoken = csrftoken;
    var email_data = {
      "email_id": email_id,
      "csrfmiddlewaretoken": csrfmiddlewaretoken
    };
    $.ajax({
      type: 'POST',
      url: '/subscribe/',
      data: email_data,
      success: function (response) {
        $('#email_id').val('');
        $('.error-message').hide();
        $('.success-message').hide();
        $('.subscribe-form').hide();
        $('.success-message').html(response.message);
        $('.success-message').fadeIn('fast', function () {
          $('.top-content').backstretch("resize");
        });
      },
      error: function (response) {
        $('.success-message').hide();
        $('.error-message').hide();
        $('.error-message').html(response.responseJSON.message);
        $('.error-message').fadeIn('fast', function () {
          $('.subscribe-form').addClass('animated flash').one(
            'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend',
            function () {
              $(this).removeClass('animated flash');
            });
        });
      }
    });
    return false;
  } else {
    $('.success-message').hide();
    $('.error-message').hide();
    $('.error-message').html('Please provide a email address!');
    $('.error-message').fadeIn('fast', function () {
      $('.subscribe-form').addClass('animated flash').one(
        'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend',
        function () {
          $(this).removeClass('animated flash');
        });
    });

  }
});


function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

function csrfSafeMethod(method) {
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
  beforeSend: function (xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
})

// -----password---
$(document).on('click', '.fa-eye', function () {
  $(this).toggleClass("fa-eye-slash");
  let input = $(this).prev();
  (input.attr("type") == "password") ? input.attr("type", "text"): input.attr("type", "password");
});

// ----caps lock on validation---
$('input[type="password"]').each(function () {
  $(this).get(0).addEventListener("keyup", function (event) {
    if (event.getModifierState("CapsLock")) {
      $(this).parents('.form-group').find('.text-warning').show();
    } else {
      $(this).parents('.form-group').find('.text-warning').hide();
    }
  });
})

// -----Mobile menu---
$(document).on("click", ".three-bar i", function () {
  $(".sidebar").toggleClass("show-sidebar");
  $(".ticker-sidebar .ticker-overlay").toggleClass("show-overlay").removeClass("hide-overlay");
  $("body").addClass("open-sidebar");
});

$(document).on("click", ".close-btn i", function () {
  $(".sidebar").removeClass("show-sidebar");
  $(".ticker-overlay").toggleClass("hide-overlay").removeClass("show-overlay");
  $("body").removeClass("open-sidebar");
});


//-----Side Add Ticker Script---
$(document).on('click', ".plus-square", function () {
  $(".real-ticker-filed").toggleClass("show-ticker-sidebar");
  $("body").addClass("open-sidebar");
  $(".ticker-sidebar .ticker-overlay").toggleClass("show-overlay").removeClass("hide-overlay");
});
$(document).on("click", ".close-ticker-sidebar i", function () {
  $(".real-ticker-filed").removeClass("show-ticker-sidebar");
  $(".ticker-sidebar .ticker-overlay").toggleClass("hide-overlay").removeClass("show-overlay");
  $("body").removeClass("open-sidebar");
});

//-----Edit Ticker Script---
$(document).on('click', ".edit-ticker-sidebar", function () {
  $(".edit-real-ticker-filed").toggleClass("edit-show-ticker-sidebar");
  $("body").addClass("open-sidebar");
  $(".ticker-sidebar .ticker-overlay").toggleClass("show-overlay").removeClass("hide-overlay");
});
$(document).on('click', ".close-ticker-sidebar i", function () {
  $(".edit-real-ticker-filed").removeClass("edit-show-ticker-sidebar");
  $(".ticker-sidebar .ticker-overlay").toggleClass("hide-overlay").removeClass("show-overlay");
  $("body").removeClass("open-sidebar");
});


//-----delete Ticker Script---
$(document).on('click', ".delete-ticker-sidebar", function () {
  $(".delete-sidebar").toggleClass("delete-show-ticker-sidebar");
  $("body").addClass("open-sidebar");
  $(".delete-ticker-overlay").toggleClass("show-overlay").removeClass("hide-overlay");
});
$(document).on('click', ".close-ticker-sidebar i", function () {
  $(".delete-sidebar").removeClass("delete-show-ticker-sidebar");
  $("body").removeClass("open-sidebar");
  $("body").removeClass("open-sidebar-second");
});
$(document).on('click', ".delete-ticker-sidebar", function () {
  $("body").addClass("open-sidebar");
  $("body").addClass("open-sidebar-second");
});
$(document).on('click', ".confirm-delete-cancel-btn", function () {
  $("body").removeClass("open-sidebar-second");
  $(".delete-sidebar").removeClass("delete-show-ticker-sidebar");
});

var removeClass = true;
$(document).on('click', "html", function () {
  if (removeClass) {
    $(".real-ticker-filed").removeClass("show-ticker-sidebar");
    $(".edit-real-ticker-filed").removeClass("edit-show-ticker-sidebar");
    $(".sidebar").removeClass("show-sidebar");
    $(".delete-sidebar").removeClass("delete-show-ticker-sidebar");
    $("body").removeClass("open-sidebar");
    $("body").removeClass("open-sidebar-second");
  }
  removeClass = true;
});
$(document).on('click', ".plus-square,.real-ticker-filed,.edit-ticker-sidebar,.edit-real-ticker-filed,.sidebar,.three-bar i,.delete-ticker-sidebar,.delete-sidebar", function () {
  removeClass = false;
});
// ------Cookie Script---
$(document).on('click', ".cookie-accept-btn button", function () {
  $(".cookie-bg-color").fadeOut();;
});

// Reads cookie and return value
function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

// ------Cookie Script---
$(document).ready(function () {
  $(".cookie-bg-color").hide();
  var cookie_ack = getCookie('cookie_acknowledgement');
  if (!cookie_ack) {
    $(".cookie-bg-color").show()
  }
});

$(document).on('click', ".cookie-accept-btn button", function () {
  document.cookie = "cookie_acknowledgement=done";
  $(".cookie-bg-color").show();
});