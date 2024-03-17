document.addEventListener("DOMContentLoaded", function() {
    var isResultsPage = window.location.pathname.includes('/results');
    var form = document.getElementById("myForm");
    if (form) {
        form.addEventListener('submit', function() {
            var loader = document.querySelector(".loader-container");
            if (loader) {
                loader.style.display = "flex"; 
            }
        });
    }
    if (isResultsPage && loader) {
        loader.style.display = "none";
    }
});