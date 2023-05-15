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


    // next button is clicked - check info before server submission
    var originalForm = $("#container-verb").html();

    $("#next-verb").on('click', function(e) {

        var english = $("#english-verb").val();
        var infinitive = $("#infinitive-verb").val();
        var written = $("#written-verb").val();
        var spoken = $("#spoken-verb").val();
        var commonUse1 = $("#commonuse-1-verb").val();
        var commonUse2 = $("#commonuse-2-verb").val();

        var cardHTML = `
            <div class="card rounded-lg mx-5 mb-5 mt-2">
                <div class="card-body mx-5 my-4">
                    <p>English Definition: ${english}</p>
                    <p>Farsi Infinitive: ${infinitive}</p>
                    <p>Written Present Stem: ${written}</p>
                    <p>Spoken Present Stem: ${spoken}</p>
                    <p>Common Use (1): ${commonUse1}</p>
                    <p>Common Use (2): ${commonUse2}</p>
                    <button class="btn btn-blue" id="back-verb">Back</button>
                    <button class="btn btn-blue ml-2" id="confirm-verb" type="submit">Confirm</button>
                </div>
            </div>

        `;

        $("#container-verb").html(cardHTML);
    });

    $(document).on('click', '#back-verb', function() {
        $("#container-verb").html(originalForm);
        $("#english-verb").val(english);
        $("#infinitive-verb").val(infinitive);
        $("#written-verb").val(written);
        $("#spoken-verb").val(spoken);
        $("#commonuse-1-verb").val(commonUse1);
        $("#commonuse-2-verb").val(commonUse2);
    });
});
