$(document).ready(function(){
    $(document).on("click", ".post .edit-buttons .del", function (evt) {
        if (!confirm($(evt.target).data("confirm"))) {
            evt.preventDefault();
        }
    });

    $(".post .reply-form textarea, #new-post-form textarea").on("keypress", function (evt) {
        if ((evt.keyCode === 10 || evt.keyCode === 13) && (evt.ctrlKey || evt.metaKey)) {
            evt.stopPropagation();
            evt.preventDefault();
            $(this).parents("form").submit();
        }
    });
});

