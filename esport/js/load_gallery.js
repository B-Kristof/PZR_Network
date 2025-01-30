async function fetchImages(year) {
    try {
        const response = await fetch(`utilities/get_gallery_images_by_year.php?year=${year}`);
        const images = await response.json();
        return images;
    } catch (error) {
        console.error('Error fetching images:', error);
    }
}


async function loadGallery(year) {
    unloadGallery();
    const gallery = document.querySelector('.gallery');

    const images = await fetchImages(year);

    if (images.length > 0) {
        if (images.length === 1){
            images.forEach(src => {
                const img = document.createElement('img');
                img.className = "single-img";
                img.src = `images/gallery/${year}/${src}`;
                img.alt = "Gallery Image";
                img.addEventListener('click', () => openFullscreen(src, year));
                gallery.appendChild(img);
            });
        } else {
            images.forEach(src => {
                const img = document.createElement('img');
                img.src = `images/gallery/${year}/${src}`;
                img.alt = "Gallery Image";
                img.addEventListener('click', () => openFullscreen(src, year));
                gallery.appendChild(img);
            });
        }
    } else {
        gallery.innerHTML += `<div style="color: white; margin-top: 5vh;">No image for that year!</div>`;
    }
}
async function retrieveAlbums() {
    try {
        const response = await fetch(`utilities/get_albums_for_gallery.php`);
        const albums = await response.json();
        return albums;
    } catch (error) {
        console.error('Error fetching images:', error);
    }
    if (albums.length > 0) {
        return 
    } else {
        gallery.innerHTML += `<div style="color: white; margin-top: 5vh;">No albums found!</div>`;
    }
}

function unloadGallery(){
    const gallery = document.querySelector('.gallery');
    gallery.innerHTML = '';
}

function openFullscreen(src, year) {
    top_menu.style.display = "none";
    const fullscreen = document.getElementById('fullscreen');
    const fullscreenImage = document.getElementById('fullscreenImage');
    fullscreenImage.src = `images/gallery/${year}/${src}`;
    fullscreen.classList.add('visible');
}

function closeFullscreen() {
    const fullscreen = document.getElementById('fullscreen');
    fullscreen.classList.remove('visible');
    top_menu.style.display = "inline-flex";
}

document.getElementById('close').addEventListener('click', closeFullscreen);


async function loadAlbumSelector() {
    const album_names = await retrieveAlbums();
    const albumSelector = document.getElementById('album-selector');

    currentYear = new Date().getFullYear();
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
}
