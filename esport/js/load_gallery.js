async function fetchImages(year) {
    try {
        const response = await fetch(`utilities/get_gallery_images_by_year.php?year=${year}`);
        if (!response.ok) {
            throw new Error('Failed to fetch images');
        }
        const images = await response.json();
        return images;
    } catch (error) {
        console.error('Error fetching images:', error);
        return []; // Return an empty array in case of an error
    }
}

async function loadGallery(year) {
    unloadGallery();
    const gallery = document.querySelector('.gallery');
    if (!gallery) return; // Check if the gallery element exists

    const images = await fetchImages(year);

    if (images && images.length > 0) {
        images.forEach(src => {
            const img = document.createElement('img');
            img.src = `images/gallery/${year}/${src}`;
            img.alt = "Gallery Image";
            img.addEventListener('click', () => openFullscreen(src, year));
            gallery.appendChild(img);
        });
    } else {
        gallery.innerHTML += `<div style="color: white; margin-top: 5vh;">No image for that year!</div>`;
    }
}

async function retrieveAlbums() {
    try {
        const response = await fetch(`utilities/get_albums_for_gallery.php`);
        if (!response.ok) {
            throw new Error('Failed to fetch albums');
        }
        const albums = await response.json();
        return albums;
    } catch (error) {
        console.error('Error fetching albums:', error);
        return []; // Return an empty array in case of an error
    }
}

function unloadGallery() {
    const gallery = document.querySelector('.gallery');
    if (gallery) {
        gallery.innerHTML = '';
    }
}

function openFullscreen(src, year) {
    const topMenu = document.getElementById('top_menu');
    if (topMenu) {
        topMenu.style.display = "none";
    }

    const fullscreen = document.getElementById('fullscreen');
    const fullscreenImage = document.getElementById('fullscreenImage');
    if (fullscreen && fullscreenImage) {
        fullscreenImage.src = `images/gallery/${year}/${src}`;
        fullscreen.classList.add('visible');
    }
}

function closeFullscreen() {
    const fullscreen = document.getElementById('fullscreen');
    const topMenu = document.getElementById('top_menu');

    if (fullscreen) {
        fullscreen.classList.remove('visible');
    }

    if (topMenu) {
        topMenu.style.display = "inline-flex";
    }
}

document.getElementById('close')?.addEventListener('click', closeFullscreen);

async function loadAlbumSelector() {
    const album_names = await retrieveAlbums();
    const albumSelector = document.getElementById('album-selector');
    if (!albumSelector) return; // Check if the album selector exists

    const currentYear = new Date().getFullYear();
    if (album_names && album_names.length > 0) {
        album_names.forEach(album_name => {
            const yearOption = document.createElement('div');
            yearOption.className = 'year-option';
            yearOption.textContent = album_name;
            yearOption.onclick = () => {
                // Remove active class from all options
                document.querySelectorAll('.year-option').forEach(option => {
                    option.classList.remove('active');
                });
                // Add active class to the clicked option
                yearOption.classList.add('active');
                loadGallery(yearOption.innerText);
            };

            // Set the current year as active by default
            if (album_name === currentYear.toString()) {
                yearOption.classList.add('active');
            }

            albumSelector.appendChild(yearOption);
        });

        // Load the gallery for the current year by default
        loadGallery(currentYear);
    } else {
        console.error('No albums found!');
    }
}
