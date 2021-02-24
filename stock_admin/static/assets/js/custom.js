/* ----- Custom Scripts for Destiny template ----- */
$(document).ready(function () {
  $('[data-toggle="tooltip"]').tooltip();

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
    console.log('pass')
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