window.addEventListener("load", function(){
    scrollToTop = document.getElementById("scrollToTop");

    var scrollToTopFunction = function () {
        var y = window.scrollY;
        if (y >= 50) {
            scrollToTop.className = "totopshow"
        } else {
            scrollToTop.className = "totophide"
        }
    };

    window.addEventListener("scroll", scrollToTopFunction);
    scrollToTopFunction();
});