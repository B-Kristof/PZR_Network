<?php
// ---- AUTH START -----
require_once 'Auth.php';
$auth = new Auth();

if (!$auth->isAuthenticated()) {
    header("Location: /urbex/public/index.php");
    exit;
}

// ---- AUTH END -----
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Location Details</title>
    <link rel="stylesheet" href="styles/location_detail.css">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/lightbox2/2.11.3/css/lightbox.min.css" rel="stylesheet">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/lightbox2/2.11.3/js/lightbox.min.js"></script>
</head>
<body>

<div class="container">
    <div>
        <div class="location-details" id="locationDetails"></div>
            <button class="map-btn" id="mapButton">Open on map</button>
            <button class="dropdown-btn" onclick="toggleGallery()">Open gallery</button>
        </div>
    </div>
<div class="gallery_container">
    <div class="gallery" id="gallery" style="display: none;">
        <h2 style="margin-right: 100px;">Gallery</h2>
    </div>
</div>

<script>
    function RedirectMap(location) {
        if (location.visitDate) {
            window.location.href = `map.php?LocType=visited&locationId=${location.id}`;
        } else {
            window.location.href = `map.php?LocType=target&locationId=${location.id}`;
        }
    }

    // Function to parse URL query parameters
    function getUrlParameter(name) {
        name = name.replace(/[[]/, '\\[').replace(/[\]]/, '\\]');
        var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
        var results = regex.exec(location.search);
        return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
    }

    // Function to load location details from JSON file
    async function loadLocationDetails(locationId) {
        try {
            const response = await fetch('utilities/retrieve_visited_locations.php');
            const locationsData = await response.json();

            let location = null;
            locationsData.forEach(data => {
                if (data.id === locationId) {
                    location = data;
                }
            });
            return location;
        } catch (error) {
            console.error('Error fetching location details:', error);
            return null;
        }
    }

    // Function to load images for the gallery
    async function loadImages(locationId) {
        return new Promise((resolve, reject) => {
            const scriptUrl = 'utilities/get_images.php'; 
            $.ajax({
                url: scriptUrl,
                method: 'GET',
                data: { locationId: locationId },
                dataType: 'json',
                success: function (data) {
                    if (data && Array.isArray(data.images)) {
                        const images = data.images.map(image => `${image}`);
                        resolve(images);
                    } else {
                        console.error('Invalid response format or missing images array.');
                        reject('Invalid response format or missing images array.');
                    }
                },
                error: function (xhr, status, error) {
                    console.error('Error fetching images:', error);
                    reject(error);
                }
            });
        });
    }

    // Function to display location details
    async function displayLocationDetails() {
        const locationId_str = getUrlParameter('locationId');
        const locationId = parseInt(locationId_str);
        if (locationId) {
            const locationDetailsContainer = document.getElementById('locationDetails');

            const location = await loadLocationDetails(locationId);
            if (location) {
                locationDetailsContainer.innerHTML += `
                <h2><input class="back-btn" type="button" value="Back" onclick="window.history.back()" /> ${location.name}</h2>
                <img loading="lazy" src="images/${location.id}/${location.titleImage}" alt="Location Image">
                <p><strong>Coordinates:</strong> ${location.coordinates !== null ? location.coordinates : "Unknown"}</p>
                <p><strong>Address:</strong> ${location.address !== null ? location.address : "Unknown"}</p>
                <p><strong>Visit Date:</strong> ${location.visitDate !== null ? location.visitDate : "Not visited"}</p>`;
                if (location.visitDate !== null && location.partOfDay !== null) {
                    locationDetailsContainer.innerHTML += `<p><strong>Part of day:</strong> ${location.partofDay}</p>`;
                }
                locationDetailsContainer.innerHTML += `
                <p><strong>Factor:</strong> ${location.factor !== null ? location.factor : 'Not available'}</p><br>
                <details><p><summary><strong>Links</strong></summary>${location.links ? location.links.map(link => `<br><a href="${link}" target="_blank">${link}</a><br>`).join('') : '<br>Not available'}</p></details><br>
                <details><p><summary><strong>Description<br></strong></summary><div style='font-size: 15px;'>${location.description !== null ? location.description : '<br>Not available'}</div></p></details>
                `; // Display links (list)
                
                // Attach the location object to the button's onclick event
                document.getElementById('mapButton').onclick = () => RedirectMap(location);

                // Load and display gallery images
                const galleryContainer = document.getElementById('gallery');
                const imageFiles = await loadImages(location.id);
                imageFiles.forEach((image, index) => {
                    galleryContainer.innerHTML += `
                        <a href="${image}" data-lightbox="gallery" data-title="Image ${index + 1}">
                            <img loading="lazy" src="${image}" alt="Gallery Image" style="width: 150px; height: auto; margin: 10px;">
                        </a>`;
                });
            } else {
                locationDetailsContainer.innerHTML = '<p>Location not found.</p>';
            }
        } else {
            console.error('Location ID not provided.');
        }
    }

    displayLocationDetails();

    // Function to toggle the display of the gallery and change button text
    function toggleGallery() {
        const gallery = document.getElementById("gallery");
        const button = document.querySelector(".dropdown-btn");
        if (gallery.style.display === "none") {
            gallery.style.display = "block";
            button.textContent = "Close gallery";
        } else {
            gallery.style.display = "none";
            button.textContent = "Open gallery";
        }
    }
</script>

</body>
</html>
