function refresh() {
    $.ajax({
        url: "/portfolio",
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
    $('.fa-spin').hide();
    $('#add-stock-form').submit(function () { // catch the form's submit event
        $('.fa-spin').show();
        let form = $('#add-stock-form');
        form.find('.validation-msg').remove();
        $.ajax({ // create an AJAX call...
            data: $(this).serialize(), // get the form data
            type: $(this).attr('method'), // GET or POST
            url: $(this).attr('action'), // the file to call
            success: function (response) { // on success..
                $('.fa-spin').hide();
                form.get(0).reset();
                refresh();
                hideOverlay();
            },
            error: function (response) {
                $('.fa-spin').hide();
                respnseObj = JSON.parse(response.responseText);
                for (var key in respnseObj) {
                    error_messages = respnseObj[key];
                    form.find(`[name="${key}"]`).parent().append(
                        `<p class="text-warning validation-msg">${error_messages[0]}</p>`);
                }
            }
        });
        return false;
    });
    $('#stock-edit-form').submit(function () { // catch the form's submit event
        $('.fa-spin').show();
        let form = $('#stock-edit-form');
        form.find('.validation-msg').remove();
        $.ajax({ // create an AJAX call...
            data: $(this).serialize(), // get the form data
            type: $(this).attr('method'), // GET or POST
            url: $(this).attr('action'), // the file to call
            success: function (response) { // on success..
                $('.fa-spin').hide();
                form.get(0).reset();
                refresh();
                hideOverlay();
            },
            error: function (response) {
                $('.fa-spin').hide();
                respnseObj = JSON.parse(response.responseText);
                for (var key in respnseObj) {
                    error_messages = respnseObj[key];
                    form.find(`[name="${key}"]`).parent().append(
                        `<p class="text-warning validation-msg">${error_messages[0]}</p>`);
                }
            }
        });
        return false;
    });
    $(document).on('click', '.edit-ticker-sidebar', function () {
        let update_url = $(this).data().url;
        console.log(update_url);
        let form = $('#stock-edit-form');
        form.attr('action', update_url);
        $.ajax({
            url: update_url,
            type: 'GET',
            success: function (response) {
                let fields = JSON.parse(response)[0]['fields'];
                $('#purchase').html(fields['purchase'] ? '$' + fields['purchase'] : '-');
                $('#proximity').html(fields['proximity'] ? fields['proximity'] + '%' : '-');
                $('#potential').html(fields['potential'] ? fields['potential'] : '-');
                $('#profit').html(fields['profit'] ? '$' + fields['profit'] : '-');
                $('#stock-name').html(fields['stock_name']);
                $('#ticker').html(fields['ticker']);
                form.find('[name="purchase"]').attr('value', fields['purchase']);
                form.find('[name="shares"]').attr('value', fields['shares']);
                form.find('[name="buy_target"]').attr('value', fields['buy_target']);
                form.find('[name="sell_target"]').attr('value', fields['sell_target']);
            }
        });
    });
});