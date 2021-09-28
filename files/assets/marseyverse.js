var clipboard = new ClipboardJS('.copy-link');
clipboard.on('success', function(e) {
        var myToast = new bootstrap.Toast(document.getElementById('toast-success'));
        myToast.show();
        console.log(e);
});
clipboard.on('error', function(e) {
        var myToast = new bootstrap.Toast(document.getElementById('toast-error'));
        myToast.show();
        console.log(e);
});


function expandDesktopImage(image) {
    var linkText = document.getElementById("desktop-expanded-image-link");
    var imgLink = document.getElementById("desktop-expanded-image-wrap-link");

    var inlineImage = document.getElementById("desktop-expanded-image");

    inlineImage.src = image.replace("100w.webp", "giphy.webp");
    linkText.href = image;
    imgLink.href=image;

    linkText.textContent = 'View original';
};


window.onload = function () {
    var prevScrollpos = window.pageYOffset;
    window.onscroll = function () {
        var currentScrollPos = window.pageYOffset;

        var topBar = document.getElementById("fixed-bar-mobile");

        var bottomBar = document.getElementById("mobile-bottom-navigation-bar");

        var dropdown = document.getElementById("mobileSortDropdown");

        var navbar = document.getElementById("navbar");

        if (bottomBar != null) {
            if (prevScrollpos > currentScrollPos && (window.innerHeight + currentScrollPos) < (document.body.offsetHeight - 65)) {
                bottomBar.style.bottom = "0px";
            } 
            else if (currentScrollPos <= 125 && (window.innerHeight + currentScrollPos) < (document.body.offsetHeight - 65)) {
                bottomBar.style.bottom = "0px";
            }
            else if (prevScrollpos > currentScrollPos && (window.innerHeight + currentScrollPos) >= (document.body.offsetHeight - 65)) {
                bottomBar.style.bottom = "-50px";
            }
            else {
                bottomBar.style.bottom = "-50px";
            }
        }

        if (topBar != null && dropdown != null) {
            if (prevScrollpos > currentScrollPos) {
                topBar.style.top = "48px";
                navbar.classList.remove("shadow");
            } 
            else if (currentScrollPos <= 125) {
                topBar.style.top = "48px";
                navbar.classList.remove("shadow");
            }
            else {
                topBar.style.top = "-48px";
                dropdown.classList.remove('show');
                navbar.classList.add("shadow");
            }
        }
        prevScrollpos = currentScrollPos;
    }
}

for(let el of document.getElementsByClassName('text-expand')) {
    el.onclick = function(event){
        if (event.which != 1) {
            return
        };
        id=this.data('id');


        document.getElementById('post-text-'+id).toggleClass('d-none');
        document.getElementsByClassName('text-expand-icon-'+id)[0].toggleClass('fa-expand-alt');
        document.getElementsByClassName('text-expand-icon-'+id)[0].toggleClass('fa-compress-alt');

    }
}

document.addEventListener("DOMContentLoaded", function(){
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(element){
        return new bootstrap.Tooltip(element);
    });
});