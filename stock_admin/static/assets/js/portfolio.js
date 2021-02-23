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
let seconds = 2;
setInterval(refresh, seconds * 1000);

function ajaxFormCall(form, element) {
    $('.fa-spin').show();
    form.find('button[type="submit"]').prop('disabled', true);
    form.find('.validation-msg').remove();
    $.ajax({ // create an AJAX call...
        data: element.serialize(), // get the form data
        type: element.attr('method'), // GET or POST
        url: element.attr('action'), // the file to call
        success: function (response) { // on success..
            $('.fa-spin').hide();
            form.find('button[type="submit"]').prop('disabled', false);
            form.get(0).reset();
            refresh();
            $(".close-ticker-sidebar i").click();
        },
        error: function (response) {
            $('.fa-spin').hide();
            form.find('button[type="submit"]').prop('disabled', false);
            respnseObj = JSON.parse(response.responseText);
            for (var key in respnseObj) {
                error_messages = respnseObj[key];
                form.find(`[name="${key}"]`).parent().append(
                    `<p class="text-warning validation-msg">${error_messages[0]}</p>`);
            }
        },
    });
}

$(document).ready(function () {
    $('.fa-spin').hide();
    $('#add-stock-form').submit(function () { // catch the form's submit event
        ajaxFormCall($('#add-stock-form'), $(this));
        return false;
    });
    $('#stock-edit-form').submit(function () { // catch the form's submit event
        ajaxFormCall($('#stock-edit-form'), $(this));
        return false;
    });
    $('#stock-delete-form').submit(function () { // catch the form's submit event
        ajaxFormCall($('#stock-delete-form'), $(this));
        return false;
    });

    function resetEditStock() {
        let fields = ['purchase', 'proximity', 'potential', 'profit', 'stock-name', 'ticker', 'open', 'pe', 'avg-vol', 'high', 'mkt-cap', 'yield', 'high-52', 'low-52', 'beta', 'vol', 'low', 'eps']
        for (let field of fields) {
            $(document).on('click', '.delete-ticker-sidebar', function () {
            $(`#${field}`).html('-');
        }
    }
        let deleteUrl = $(this).data().url;
        let form = $('#stock-delete-form');
        form.attr('action', deleteUrl); 
    });
    $(document).on('click', '.edit-ticker-sidebar', function () {
        resetEditStock();
        let updateUrl = $(this).data().url;
        let fundamentalsUrl = $(this).data().fundamentalsUrl;
        let form = $('#stock-edit-form');
        form.attr('action', updateUrl);
        $.ajax({
            url: updateUrl,
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
        $.ajax({
            url: fundamentalsUrl,
            type: 'GET',
            success: function (res) {
                let response = JSON.parse(res.replace(/\bNaN\b/g, "null"))
                $('#open').html(response['Open'] ? response['Open'] : '-');
                $('#pe').html(response['PE Ratio (TTM)'] ? response['PE Ratio (TTM)'] : '-');
                $('#avg-vol').html(response['Avg. Volume'] ? response['Avg. Volume'] : '-');
                $('#high').html(response["Day's Range"] ? response["Day's Range"].split(' - ')[1] : '-');
                $('#mkt-cap').html(response['Market Cap'] ? response['Market Cap'] : '-');
                $('#yield').html(response['Forward Dividend & Yield'] ? response['Forward Dividend & Yield'] : '-');
                $('#high-52').html(response['52 Week Range'] ? response['52 Week Range'].split(' - ')[1] : '-');
                $('#low-52').html(response['52 Week Range'] ? response['52 Week Range'].split(' - ')[0] : '-');
                $('#beta').html(response['Beta (5Y Monthly)'] ? response['Beta (5Y Monthly)'] : '-');
                $('#vol').html(response['Volume'] ? response['Volume'] : '-');
                $('#low').html(response["Day's Range"] ? response["Day's Range"].split(' - ')[0] : '-');
                $('#eps').html(response['EPS (TTM)'] ? response['EPS (TTM)'] : '-');
            }
        });
    });
});