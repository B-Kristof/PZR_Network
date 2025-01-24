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
    const album_names = await retrieveAlbums(); // Declare with const or let
    const albumSelector = document.getElementById('album-selector');

    currentYear = new Date().getFullYear();
    album_names.forEach(album_name => {
        // Create a new DOM element
        const yearOption = document.createElement('div');
        yearOption.className = 'year-option';
        yearOption.textContent = album_name;
        yearOption.onclick = () => loadGallery(yearOption.innerText);

        // Append the DOM element to the album selector
        albumSelector.appendChild(yearOption);
    });
}
