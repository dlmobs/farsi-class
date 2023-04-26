$(document).ready(function () {
    $('#verbs-btn').click(function (event) {
      event.stopPropagation();
      window.location.href = "/verb-list";
    });
});