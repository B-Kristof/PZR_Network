document.addEventListener("DOMContentLoaded", function() {
    const languageToggle = document.getElementById('language-toggle');
    
    // Restore scroll position after page load
    if (localStorage.getItem('scrollPosition')) {
        window.scrollTo(0, localStorage.getItem('scrollPosition'));
        localStorage.removeItem('scrollPosition'); // Clean up storage after restoring position
    }
  
    // Set the initial state based on the current URL
    if (window.location.href.includes("/en/")) {
        languageToggle.checked = true;
    }
  
    // Listen for changes to the toggle switch
    languageToggle.addEventListener('change', function() {
        // Save the current scroll position
        localStorage.setItem('scrollPosition', window.scrollY);
        
        // Redirect to the appropriate version based on toggle
        if (this.checked) {
            // Redirect to English version
            window.location.href = '/en/home.html';
        } else {
            // Redirect to Hungarian version
            window.location.href = '/home.html';
        }
    });
});


const nav_esport = document.getElementById("nav-esport");
const nav_urbex = document.getElementById("nav-urbex");
const nav_members_only = document.getElementById("nav-members-only");
const esport_overlay = document.getElementById('nav-esport-overlay');
const members_only_overlay = document.getElementById('nav-members-only-overlay');
const urbex_overlay = document.getElementById('nav-urbex-overlay');

nav_esport.onmousedown = function () {
    const old_esport_style = nav_esport.style;
    const old_esport_overlay = esport_overlay.style;

    nav_esport.style.marginRight = "-200%";
    esport_overlay.style.opacity = 0;
    setTimeout(function () {
        window.location.href = "/esport/home.html";
    }, 400);
    setTimeout(function () {
        nav_esport.style = old_esport_style;
        esport_overlay.style = old_esport_overlay;
    }, 1000);
};

nav_members_only.onmousedown = function () {
    const old_members_only_style = nav_members_only.style;
    const old_members_only_overlay = members_only_overlay.style;

    nav_members_only.style.marginLeft = "-150%";
    nav_members_only.style.marginRight = "-150%";
    members_only_overlay.style.opacity = 0;
    setTimeout(function () {
        window.location.href = "/drink/login.php";
    }, 400);
    setTimeout(function () {
        nav_members_only.style = old_members_only_style;
        members_only_overlay.style = old_members_only_overlay;
    }, 1000);
;};

nav_urbex.onmousedown = function () {
    const old_urbex_style = nav_urbex.style;
    const old_urbex_overlay = urbex_overlay.style;

    nav_urbex.style.marginLeft = "-200%";
    urbex_overlay.style.opacity = 0;
    setTimeout(function () {
        window.location.href = "http://urbex.pzrteam.hu";
    }, 400);
    setTimeout(function () {
        nav_urbex.style = old_urbex_style;
        urbex_overlay.style = old_urbex_overlay;
    }, 1000);
;};