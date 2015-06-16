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
    $("#new-post-form textarea").on("keypress", send_form_by_ctrl_enter);
    // Comments reply form
    $("#content").on("keypress", ".reply-form textarea", send_form_by_ctrl_enter);

    // Delete post or comment
    $(document).on("click", ".post .edit-buttons .del", function (evt) {
        if (!confirm($(evt.target).data("confirm"))) {
            evt.preventDefault();
        }
    });
});

