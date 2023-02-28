$(document).ready(function($) {
    $(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });

    $("#writte-test").click(function() {
      $("#start-test-button").prop("href", "/test");
    });

    $("#cards").click(function() {
      $("#start-test-button").prop("href", "/cards");
    });
  });