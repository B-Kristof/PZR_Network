let allLocations = [];

async function loadLocations() {
    try {
        const response = await fetch('../utilities/retrieve_visited_locations.php');
        const locations = await response.json();
        return locations;
    } catch (error) {
        console.error('Error:', error);
        return [];
    }
}

async function displayLocations(locations) {
    const locationsContainer = document.getElementById('locationsContainer');
    locationsContainer.innerHTML = '';

    locations.forEach((location, index) => {
        const locationCard = document.createElement('div');
        locationCard.classList.add('location-card');
        if (locations.length === 1) {
            locationCard.classList.add('single-location');
        }

        const anchor = document.createElement('a');
        anchor.href = `location_detail.php?locationId=${location.id}`;

        const titleImage = document.createElement('img');
        titleImage.src = `images/${location.id}/${location.titleImage}`;
        titleImage.onerror = function() {
            titleImage.src = 'images/default/no_image.jpg';
        };
        titleImage.alt = 'Location Image';

        anchor.appendChild(titleImage);

        anchor.innerHTML += `
            <h2>${location.name}</h2>
            <p><strong>Coordinates:</strong> ${location.coordinates}</p>
            <p><strong>Address:</strong> ${location.address !== null ? location.address : "Unknown"}</p>
            <p><strong>Visit Date:</strong> ${location.visitDate !== null ? location.visitDate : "Not visited"}</p>`;
        if (location.visitDate !== null && location.partofDay !== null) {
            anchor.innerHTML += `<p><strong>Part of day:</strong> ${location.partofDay}</p>`;
        }
        anchor.innerHTML += `
            <p><strong>Factor:</strong> ${location.factor !== null ? location.factor : 'Not available'}</p>
        `;

        locationCard.appendChild(anchor);
        locationsContainer.appendChild(locationCard);
    });
}

function searchLocations() {
    const query = document.getElementById('searchInput').value.toLowerCase();
    if (query){
        const filteredLocations = allLocations.filter(location => location.name.toLowerCase().includes(query));
        const searchResult = document.getElementById('searchResult');
        const searchInput = document.getElementById('searchInput');
        searchInput.value = "";
        searchResult.style.display = "inline-block";
        if (filteredLocations.length > 0){
            searchResult.innerHTML = `<div class="searchResult">Search results for "${query}":
            <button class='delete_search_button' onclick="reset_search()">x</button></div>`;
        } else {
            searchResult.innerHTML = `<div class="searchResult">No results for "${query}".
            <button class='delete_search_button' onclick="reset_search()">x</button></div>`;
        }
        displayLocations(filteredLocations);
    }
}

(async function() {
    allLocations = await loadLocations();
    displayLocations(allLocations);
})();

async function reset_search(){
    const searchResult = document.getElementById('searchResult');
    searchResult.style.display = "none";
    searchResult.innerHTML = ""
    allLocations = await loadLocations();
    displayLocations(allLocations);
}