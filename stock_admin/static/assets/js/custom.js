/*----- Subscription Form ----- */

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