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
            window.location.href = '/esport/en/home.html';
        } else {
            // Redirect to Hungarian version
            window.location.href = '/esport/home.html';
        }
    });
});


// Trigger animation on scroll for 'about', 'youtube_card', 'stream_card', and 'vertical_fifth'
document.addEventListener("DOMContentLoaded", function() {
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

    // Observe the 'about' section and YouTube cards
    observer.observe(aboutSection);
    youtubeCards.forEach(card => observer.observe(card));

    // Observe the single 'stream_card'
    if (streamCard) {
        observer.observe(streamCard);
    }

    // Add observer for the vertical_fifth section
    const verticalFifth = document.querySelector('.vertical_fifth');
    const sponsorImages = document.querySelectorAll('.vertical_fifth .sponsor');
    const partnersHeading = document.querySelector('.vertical_fifth h1');

    // Observe the vertical_fifth section (line animation under 'Our Partners')
    observer.observe(partnersHeading);

    // Observe the vertical_fifth section (line animation)
    observer.observe(verticalFifth);

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

    // Observe each sponsor image
    sponsorImages.forEach(sponsor => {
        sponsorObserver.observe(sponsor);
    });
});


// Smooth scrolling for menu links
document.querySelectorAll('.top_menu .menu-container a').forEach(link => {
    link.addEventListener('click', function(e) {
        const targetId = this.getAttribute('href'); // Get the target section ID
        const targetSection = document.querySelector(targetId); // Find the target section

        // Check if the target is the home section and the user is already there
        if (targetId === "#home" && window.scrollY === 0) {
            // Redirect to another page if already at the home section
            window.location.href = "../home.html"; // Change this to your desired URL
        } else {
            e.preventDefault(); // Prevent default anchor click behavior

            // Scroll to the target section smoothly
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
        if (link.getAttribute('href').includes(currentSection)) {
            link.classList.add('active');
        }
    });
}

// Set the default active menu item on page load
window.addEventListener('load', () => {
    updateActiveMenu(); // Ensure the default menu item is highlighted
});

// Update the active menu item on scroll
window.addEventListener('scroll', updateActiveMenu);

// Slideshow functionality
let currentSlide = 0;
let slides;
async function fetchImages() {
    try {
        let en_switch = false;
        let response = await fetch('utilities/get_images_for_gallery.php'); // Fetch image list from server
        if (response.status == 404){
            console.log("en")
            response = await fetch('../utilities/get_images_for_gallery.php'); // Fetch image list from server
            en_switch = true;
        }
        const images = await response.json();
        const slideshowContainer = document.getElementById('slideshow');

        // Add images to the DOM
        images.forEach((image, index) => {
            let img = document.createElement('img');
            if (!en_switch){
                img.src = `images/gallery/${image}`;
            } else {
                img.src = `../images/gallery/${image}`;
            }
            img.classList.add('slide');
            if (index === 0) {
                img.classList.add('active'); // Show first image initially
            }
            slideshowContainer.appendChild(img);
        });

        slides = document.querySelectorAll('.slide'); // Update the slides array
        startSlideshow();
    } catch (error) {
        console.error('Error fetching images:', error);
    }
}

function showSlide(index) {
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
    showSlide(currentSlide + 1);
}

function prevSlide() {
    showSlide(currentSlide - 1);
}


// Load images when the page loads
window.onload = fetchImages;
