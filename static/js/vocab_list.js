$(document).ready(function() {
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
      let searchText = $('#search-input').val().toLowerCase();
  
      rows.hide();
      rows.each(function() {
        let englishText = $(this).find('td:first-child h5').text().toLowerCase();
        let farsiText = $(this).find('td:nth-child(2)').text();
  
        if ( englishText.indexOf(searchText) !== -1 || farsiText.indexOf(searchText) !== -1 ) {
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
  