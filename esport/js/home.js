document.addEventListener("DOMContentLoaded", function () {
    const languageToggle = document.getElementById('language-toggle');

    // Restore scroll position after page load
    const savedScrollPosition = localStorage.getItem('scrollPosition');
    if (savedScrollPosition) {
        window.scrollTo(0, parseInt(savedScrollPosition, 10));
        localStorage.removeItem('scrollPosition'); // Clean up storage after restoring position
    }

    // Ensure languageToggle exists before using it
    if (languageToggle) {
        // Set the initial state based on the current URL
        if (window.location.href.includes("/en/")) {
            languageToggle.checked = true;
        }

        // Listen for changes to the toggle switch
        languageToggle.addEventListener('change', function () {
            // Save the current scroll position
            localStorage.setItem('scrollPosition', window.scrollY);

            // Redirect to the appropriate version based on toggle
            window.location.href = this.checked ? '/esport/en/home.html' : '/esport/home.html';
        });
    }
});

// Trigger animation on scroll for 'about', 'youtube_card', 'stream_card', and 'vertical_fifth'
document.addEventListener("DOMContentLoaded", function () {
    const observerOptions = {
        threshold: 0.1 // Trigger when 10% of the element is visible
    };

    // Create a new IntersectionObserver instance
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
            } else {
                entry.target.classList.remove('animate'); // Reset animation on scroll away
            }
        });
    }, observerOptions);

    // Select elements to observe
    const aboutSection = document.querySelector('.vertical_second .about');
    const youtubeCards = document.querySelectorAll('.vertical_sixth .youtube_card');
    const streamCard = document.querySelector('.vertical_sixth .stream_card');
    const verticalFifth = document.querySelector('.vertical_fifth');
    const sponsorImages = document.querySelectorAll('.vertical_fifth .sponsor');
    const partnersHeading = document.querySelector('.vertical_fifth h1');

    // Observe elements only if they exist
    if (aboutSection) observer.observe(aboutSection);
    youtubeCards.forEach(card => observer.observe(card));
    if (streamCard) observer.observe(streamCard);
    if (partnersHeading) observer.observe(partnersHeading);
    if (verticalFifth) observer.observe(verticalFifth);

    // Create a separate observer for sponsor images to appear one by one
    const sponsorObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible'); // Add class to make image slide in
            } else {
                entry.target.classList.remove('visible'); // Reset image animation
            }
        });
    }, observerOptions);

    // Observe each sponsor image only if there are any
    if (sponsorImages.length > 0) {
        sponsorImages.forEach(sponsor => sponsorObserver.observe(sponsor));
    }
});

// Smooth scrolling for menu links
document.querySelectorAll('.top_menu .menu-container a').forEach(link => {
    link.addEventListener('click', function (e) {
        const targetId = this.getAttribute('href'); // Get the target section ID
        if (!targetId.startsWith("#")) return; // Ensure it's an internal link

        const targetSection = document.querySelector(targetId); // Find the target section
        if (!targetSection) return; // Prevent error if section doesn't exist

        // Check if the target is the home section and the user is already there
        if (targetId === "#home" && window.scrollY === 0) {
            window.location.href = "../home.html"; // Redirect if already at the home section
        } else {
            e.preventDefault(); // Prevent default anchor click behavior
            targetSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

// Get all sections and menu links for active class update on scroll
const sections = document.querySelectorAll('section');
const menuLinks = document.querySelectorAll('.menu-link');

// Function to change the active class based on scroll position
function updateActiveMenu() {
    let currentSection = '';

    const viewportHeight = window.innerHeight;
    sections.forEach(section => {
        const sectionTop = section.offsetTop;

        if (scrollY >= sectionTop - viewportHeight / 4) {
            currentSection = section.getAttribute('id');
        }
    });

    // Check if the user is near the bottom of the page
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 2) {
        currentSection = 'contacts'; // Set to the id of the #contacts section
    }

    menuLinks.forEach(link => {
        link.classList.remove('active');
        if (currentSection && link.getAttribute('href').includes(currentSection)) {
            link.classList.add('active');
        }
    });
}

// Set the default active menu item on page load
window.addEventListener('load', updateActiveMenu);
window.addEventListener('scroll', updateActiveMenu);

// Slideshow functionality
let currentSlide = 0;
let slides;
async function fetchImages(year) {
    try {
        let en_switch = false;
        let response = await fetch('utilities/get_images_for_gallery.php?year=' + year); // Fetch image list from server

        if (response.status == 404) {
            console.log("en");
            response = await fetch('../utilities/get_images_for_gallery.php?year=' + year); // Try alternative path
            en_switch = true;
        }

        const images = await response.json();
        console.log(images);

        const slideshowContainer = document.getElementById('slideshow');
        if (!slideshowContainer) return; // Prevent errors if the element is missing

        // Clear existing images
        slideshowContainer.innerHTML = "";

        // Add images to the DOM
        images.forEach((image, index) => {
            let img = document.createElement('img');
            img.src = en_switch
                ? `../images/gallery/${year}/${image}`
                : `images/gallery/${year}/${image}`;
            img.classList.add('slide');

            if (index === 0) {
                img.classList.add('active'); // Show first image initially
            }

            slideshowContainer.appendChild(img);
        });

        slides = document.querySelectorAll('.slide'); // Update the slides array

    } catch (error) {
        console.error('Error fetching images:', error);
    }
}

function showSlide(index) {
    if (!slides || slides.length === 0) return; // Prevent errors if slides are not available

    // Wrap around index if it goes out of bounds
    if (index < 0) {
        currentSlide = slides.length - 1;
    } else if (index >= slides.length) {
        currentSlide = 0;
    } else {
        currentSlide = index;
    }

    // Hide all slides, then show the current one
    slides.forEach((slide, i) => {
        slide.classList.remove('active');
        if (i === currentSlide) {
            slide.classList.add('active');
        }
    });
}

function nextSlide() {
    if (slides && slides.length > 0) {
        showSlide(currentSlide + 1);
    }
}

function prevSlide() {
    if (slides && slides.length > 0) {
        showSlide(currentSlide - 1);
    }
}
