
// make a row clickable
$(document).ready(function() {
    $('.clickable-row').click(function() {
      const url = $(this).data('url')
      window.location = url;
    });
});

// pagination
$(document).ready(function () {
  var currentPage = 1;
  var rowsPerPage = 15;
  var totalPages;

  var rows = $('#table-body tr');

  function renderTable() {
    rows.hide();
    var startIndex = (currentPage - 1) * rowsPerPage;
    var endIndex = startIndex + rowsPerPage;
    rows.slice(startIndex, endIndex).show();

    totalPages = Math.ceil(rows.length / rowsPerPage);
    renderPagination();
  }

  function renderPagination() {
    var pagination = $('.pagination');
    pagination.empty();

    for (var i = 1; i <= totalPages; i++) {
      var pageItem = $('<li class="page-item"><a class="page-link" href="#">' + i + '</a></li>');
      if (i === currentPage) {
        pageItem.addClass('active');
      }
      pagination.append(pageItem);
    }
  }

  $('#rows-per-page').on('change', function () {
    rowsPerPage = parseInt($(this).val(), 10);
    currentPage = 1;
    renderTable();
  });

  $('body').on('click', '.page-link', function (e) {
    e.preventDefault();
    currentPage = parseInt($(this).text(), 10);
    renderTable();
  });

  renderTable();
});