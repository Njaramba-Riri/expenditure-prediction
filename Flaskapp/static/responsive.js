$(document).ready(function() {
    $('input[name="tarr"]').on('', function() {
        var selectedValue = $(this).val();
        if (selectedValue == 'Package Tour') {
            $('#pkg').show();
        } else if (selectedValue == 'Independent') {
            $('#pkg').hide();
        } else {
            $('#pkg').show();
        }
    });
});

$(function () {
    $("#slider1").responsiveSlides({
        maxwidth: 1600,
        speed: 600
    });
});