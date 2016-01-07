$(document).ready(function() {
    // Common send form function
    function send_form_by_ctrl_enter(evt) {
        if ((evt.keyCode === 10 || evt.keyCode === 13) && (evt.ctrlKey || evt.metaKey)) {
            evt.stopPropagation();
            evt.preventDefault();
            $(this).closest("form").submit();
        }
    }

    // Listeners
    // New post form
    $("#new-post-form textarea").on("keydown", send_form_by_ctrl_enter);
    // Comments reply form
    $("#content").on("keydown", ".reply-form textarea", send_form_by_ctrl_enter);

    // Delete post or comment
    $(document).on("click", ".post .edit-buttons .del", function (evt) {
        if (!confirm($(evt.target).data("confirm"))) {
            evt.preventDefault();
        }
    });
    
    // Scroll line numbers
    $('.codehilitetable').each(function() {
      var lines = $('.linenos pre', this);
      if (lines.length === 0) {
        //return;
      }
      $('.codehilite pre', this).on('scroll', function(evt) {
        lines.scrollTop($(this).scrollTop());
      });
    });
});

