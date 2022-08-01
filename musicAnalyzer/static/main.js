function toggleDiv(divId) {
    $('#' + divId).fadeToggle(150);
}

function suggestHeadline() {
    $.post('suggest_headline', {
        url: $('#url').val()
    }, function(data) {
        $('#headline').val(data);
    });
}