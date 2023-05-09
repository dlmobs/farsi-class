$(document).ready(function() {
  // Make a row clickable
  $('.clickable-row').click(function() {
    const url = $(this).data('url');
    window.location = url;
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

  // store the current sort order
  var engSortOrder = 1;
  var farsiSortOrder = 1;

  // event listener for the English sort button
  $('#eng-sort-btn').click(function() {
    engSortOrder = -engSortOrder;
    sortTable(0, engSortOrder);
  });

  // event listener for the Farsi sort button
  $('#farsi-sort-btn').click(function() {
    farsiSortOrder = -farsiSortOrder;
    sortTable(3, farsiSortOrder);
  });

  // event listener for the checkbox
  $('#spoken-checkbox').on('change', function() {
    filterTable();
  });

  // sort the table by the specified column
  function sortTable(columnIndex, sortOrder) {
    var rows = $('#table-body tr').get();
    rows.sort(function(a, b) {
      var valueA = $(a).find('td:nth-child(' + (columnIndex + 1) + ') h5').text();
      var valueB = $(b).find('td:nth-child(' + (columnIndex + 1) + ') h5').text();

      if (columnIndex === 0) {
        valueA = valueA.toLowerCase();
        valueB = valueB.toLowerCase();
      }
      
      if (valueA < valueB) {
        return -sortOrder;
      } else if (valueA > valueB) {
        return sortOrder;
      } else {
        return 0;
      }
    });

    // Re-append the sorted rows to the table
    for (var i = 0; i < rows.length; i++) {
      $('#table-body').append(rows[i]);
    }
  }

  function filterTable() {
    let checkboxChecked = $('#spoken-checkbox').prop('checked');
    let searchText = $('#search-input').val().toLowerCase().trim();
  
    rows.hide();
    rows.each(function() {
      let englishText = $(this).find('td:first-child h5').text().toLowerCase();
      let farsiText = $(this).find('td:nth-child(3), td:nth-child(4)').text();
      let spokenText = $(this).find('td:nth-child(3) h5.green-color').text().trim();
  
      if (
        (englishText.indexOf(searchText) !== -1 || farsiText.indexOf(searchText) !== -1) &&
        (!checkboxChecked || (checkboxChecked && spokenText !== ""))
      ) {
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
  sortTable(0, engSortOrder);
});
