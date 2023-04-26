$(document).ready(function() {
  // Make a row clickable
  $('.clickable-row').click(function() {
    const url = $(this).data('url');
    window.location = url;
  });

  // Transitive/intransitive filtering
  $('input[type=radio][name=options]').on('change', function() {
    filterTable();
  });

  // Search bar
  $('#search-input').on('keyup', function() {
    filterTable();
  });

  // Pagination
  var currentPage = 1;
  var rowsPerPage = 15;
  var totalPages;

  var rows = $('#table-body tr');

  function filterTable() {
    let verbType = $('input[type=radio][name=options]:checked').val();
    let searchText = $('#search-input').val().toLowerCase();

    rows.hide();
    rows.each(function() {
      let rowVerbType = $(this).data('verb-type');
      let englishText = $(this).find('td:first-child h5').text().toLowerCase();

      if ((verbType === 'All' || rowVerbType === verbType) && englishText.indexOf(searchText) !== -1) {
        $(this).show();
      }
    });

    renderTable();
  }

  function renderTable() {
    let visibleRows = rows.filter(':visible');
    let startIndex = (currentPage - 1) * rowsPerPage;
    let endIndex = startIndex + rowsPerPage;

    visibleRows.hide();
    visibleRows.slice(startIndex, endIndex).show();

    totalPages = Math.ceil(visibleRows.length / rowsPerPage);
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

  $('#rows-per-page').on('change', function() {
    rowsPerPage = parseInt($(this).val(), 10);
    currentPage = 1;
    renderTable();
  });

  $('body').on('click', '.page-link', function(e) {
    e.preventDefault();
    currentPage = parseInt($(this).text(), 10);
    renderTable();
  });

  filterTable();
});
