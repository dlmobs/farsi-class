// script for login page incorrect password alert

$(document).ready(function() {
    var incorrectPassword = $('form').data('incorrect-password');
    if (incorrectPassword == "True") {
        $('.incorrect-password').show();
    } else {
        $('.incorrect-password').hide();
    }
});
