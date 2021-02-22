function refresh() {
    $.ajax({
        url: "{% url 'portfolio' %}",
        success: function (data) {
            $('#table-body').replaceWith($('#table-body', data));
            $('#investment-profit').replaceWith($('#investment-profit', data));
            $('#updated-time').replaceWith($('#updated-time', data));
        }
    });
}
let seconds = 3;
setInterval(refresh, seconds * 1000);
$(document).ready(function () {
    $('#add-stock-form').submit(function () { // catch the form's submit event
        let form = $('#add-stock-form');
        form.find('.validation-msg').remove();
        $.ajax({ // create an AJAX call...
            data: $(this).serialize(), // get the form data
            type: $(this).attr('method'), // GET or POST
            url: $(this).attr('action'), // the file to call
            success: function (response) { // on success..
                form.get(0).reset();
                refresh();
                hideOverlay();
            },
            error: function (response) {
                respnseObj = JSON.parse(response.responseText);
                for (var key in respnseObj) {
                    error_messages = respnseObj[key];
                    $(`[name="${key}"]`).parent().append(
                        `<p class="text-warning validation-msg">${error_messages[0]}</p>`);
                }
            }
        });
        return false;
    });
});