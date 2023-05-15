// js file for edit.html

// $(function () {
//     $('[data-toggle="popover"]').popover()
// })

function isFarsi(str) {
    return /[\u0600-\u06FF]/.test(str);
}

$(document).ready(function() {
    $('#search-results').addClass('hidden'); // Hide the search results on page load

    $('#search-verb').on('keyup', function() {
        var search_term = $(this).val();

        if (!search_term) {
            $('#search-results').addClass('hidden');
            return;
        } else {
            var search_key = isFarsi(search_term) ? 'infinitive' : 'english';
            $('#search-results').removeClass('hidden');
        
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
        }
    });
    $(document).on('click', '.search-result', function() {
        var data = $(this).data('result');
        let written_stem = data["Pres. Stem"]['written'].join(' ')
        let spoken_stem = data["Pres. Stem"]['spoken'].join(' ')

        // autofill input fields
        $('#english-verb').val(data['english']);
        $('#infinitive-verb').val(data['infinitive']);
        $('#written-verb').val(written_stem);
        $('#spoken-verb').val(spoken_stem);
        $('#commonuse-1-verb').val(data["common use"][0]);
        $('#commonuse-2-verb').val(data["common use"][1])

        // autofill search field and remove the dropdown line
        $('#search-verb').val(data['english'])
        $('#search-results').addClass('hidden');
    });

    // hide the dropdown if somewhere is clicked
    $(document).on('click', function(e) {
        if (!$(e.target).closest('#search-results').length) {
            $('#search-results').addClass('hidden');
        }
    });
});
