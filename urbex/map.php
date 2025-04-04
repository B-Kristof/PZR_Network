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
    <meta name="viewport" content="width=device-width, initial-scale=0.42">
    <title>Urbex Portal - Map</title>
    <link rel="stylesheet" href="styles/map.css">
    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
</head>
<body>
    <!-- Side Menu -->
    <div class="side-menu">
        <div class="logo"><a href="locations.php"><h1 class="logo">Urbex Portal</h1></a></div><br><div style="border-bottom: solid 1px"></div><br>
        <ul class="menu">
            <div>
                <div style="display: inline-flex">
                    <label>Only my locations: &ensp;</label>
                    <div>
                        <label id="switch" class="switch" for="filter-switch">
                            <input type="checkbox" id="filter-switch" name="filter-switch"/>
                            <div></div>
                        </label>
                    </div>
                </div>
                <br><br>
                <details open>
                    <summary style="font-size: 22px; font-weight: bold;">Visited Locations</summary>
                    <li style="padding-top: 15px;" id="menu-visited"></li>
                </details>
                <br>
                <details open>
                    <summary style="font-size: 22px; font-weight: bold;">Target Locations</summary>
                    <li style="padding-top: 15px;" id="menu-target"></li>
                </details>
            </div>
        </ul>
    </div>

    <!-- Map -->
    <div id="map"></div>

    <script>
        async function getUserId() {
            try {
                const response = await fetch('utilities/get_userid_by_username.php');
                const data = await response.json();
                return data.user_id;
            } catch (error) {
                console.error('Error fetching user ID:', error);
                return null;
            }
        }

        function getLocationIdFromUrl() {
            const params = new URLSearchParams(window.location.search);
            const loctype = params.get('LocType');
            const locid = params.get('locationId');
            
            // Validate loctype
            if ((loctype === "visited" || loctype === "target") && locid && !isNaN(locid)) {
                return [loctype, Number(locid)];
            } else {
                return null;
            }
        }

        document.addEventListener('DOMContentLoaded', async () => {
            const map = L.map('map').setView([47.511198972714055, 18.96963568631461], 13);

            const greenIcon = L.icon({
                iconUrl: 'images/map/marker-icon-green.png',
                shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                iconSize: [25, 41],
                iconAnchor: [12, 41],
                popupAnchor: [1, -34],
                shadowSize: [41, 41]
            });

            const redIcon = L.icon({
                iconUrl: 'images/map/marker-icon-red.png',
                shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                iconSize: [25, 41],
                iconAnchor: [12, 41],
                popupAnchor: [1, -34],
                shadowSize: [41, 41]
            });

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);

            const userId = await getUserId();
            if (!userId) {
                console.error('User ID could not be retrieved.');
                return;
            }

            const allMarkers = [];
            let locationIdandTypeFromUrl = null;
            const visitedLocations = await (await fetch('utilities/retrieve_visited_locations.php')).json();
            const targetLocations = await (await fetch('utilities/retrieve_target_locations.php')).json();
            const menuVisited = document.getElementById('menu-visited');
            const menuTarget = document.getElementById('menu-target');
            locationIdandTypeFromUrl = getLocationIdFromUrl();

            function renderLocations(filter = false) {
                menuVisited.innerHTML = '';
                menuTarget.innerHTML = '';
                allMarkers.forEach(({ marker }) => map.removeLayer(marker));
                allMarkers.length = 0;

                const filteredVisited = filter ? visitedLocations.filter(location => location.created_by == userId) : visitedLocations;
                const filteredTarget = filter ? targetLocations.filter(location => location.created_by == userId) : targetLocations;

                filteredVisited.forEach(location => {
                    const coords = location.coordinates.split(',').map(coord => parseFloat(coord.trim()));

                    const marker = L.marker(coords, { icon: greenIcon })
                        .bindPopup(`<a href="location_detail.php?locationId=${location.id}"><b>${location.name}</b><br>${location.address !== null ? location.address : "Unknown address"}</a>`)
                        .addTo(map);

                    allMarkers.push({ marker, coords });

                    const listItem = document.createElement('li');
                    listItem.innerHTML = `<a style="font-size: 15px;" href="#" data-coords="${coords}" data-index="${allMarkers.length - 1}">${location.name}</a>`;
                    menuVisited.appendChild(listItem);
                });

                filteredTarget.forEach(location => {
                    const coords = location.coordinates.split(',').map(coord => parseFloat(coord.trim()));

                    const marker = L.marker(coords, { icon: redIcon })
                        .bindPopup(`<a href="target_detail.php?locationId=${location.id}"><b>${location.name}</b><br>${location.address !== null ? location.address : "Unknown address"}</a>`)
                        .addTo(map);

                    allMarkers.push({ marker, coords });

                    const listItem = document.createElement('li');
                    listItem.innerHTML = `<a style="font-size: 15px;" href="#" data-coords="${coords}" data-index="${allMarkers.length - 1}">${location.name}</a>`;
                    menuTarget.appendChild(listItem);
                });

                document.querySelectorAll('.menu a').forEach(anchor => {
                    anchor.addEventListener('click', function (event) {
                        event.preventDefault();

                        const coords = this.getAttribute('data-coords').split(',').map(Number);
                        const index = this.getAttribute('data-index');
                        const { marker } = allMarkers[index];

                        map.setView(coords, 13);
                        marker.openPopup();
                    });
                });

                if (locationIdandTypeFromUrl) {
                    let location = null;
                    const location_type = locationIdandTypeFromUrl[0];
                    const location_id = locationIdandTypeFromUrl[1];
                    if (location_type == "visited"){
                        location = filteredVisited.find(loc => loc.id == location_id);
                    }
                    else if (location_type == "target"){
                        location = filteredTarget.find(loc => loc.id == location_id);
                    }
                    if (location) {
                        const coords = location.coordinates.split(',').map(coord => parseFloat(coord.trim()));
                        map.setView(coords, 13);
                        const marker = allMarkers.find(m => m.coords[0] === coords[0] && m.coords[1] === coords[1]).marker;
                        marker.openPopup();
                    }
                }
            }

            document.getElementById('filter-switch').addEventListener('change', function () {
                renderLocations(this.checked);
                const sw = document.getElementById('switch');
                const sw_state = document.getElementById('filter-switch');
                if (sw_state.checked) {
                    sw.style.background = "black";
                } else {
                    sw.style.background = "#ababab";
                }
            });

            renderLocations();
        });
    </script>
</body>
</html>
