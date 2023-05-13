// js file for edit.html

// $(function () {
//     $('[data-toggle="popover"]').popover()
// })

function isFarsi(str) {
    return /[\u0600-\u06FF]/.test(str);
}

$(document).ready(function() {
    $('#search-verb').on('keyup', function() {
        var search_term = $(this).val();
        var search_key = isFarsi(search_term) ? 'infinitive' : 'english';
        $.ajax({
            url: '/search',
            data: { 'term': search_term, 'key': search_key },
            success: function(data) {
                var results_html = '';
                if (data.length == 0) {
                    results_html = '<div>No matches found</div>';
                } else {
                    for (var i = 0; i < data.length; i++) {
                        results_html += '<div class="search-result" data-result=\'' + JSON.stringify(data[i]) + '\'>' + data[i][search_key] + '</div>';
                    }
                }
                $('#search-results').html(results_html);
            }
        });
    });
    $(document).on('click', '.search-result', function() {
        var data = $(this).data('result');
        $('#english-verb').val(data['english']);
        $('#infinitive-verb').val(data['infinitive']);
        $('#written-verb').val(data["Pres. Stem"]['written']);
        $('#spoken-verb').val(data["Pres. Stem"]['spoken']);
        $('#commonuse-1-verb').val(data["common use"][0]);
        $('#commonuse-2-verb').val(data["common use"][1])
    });
});
