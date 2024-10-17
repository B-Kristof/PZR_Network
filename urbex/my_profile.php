<?php

session_start();
// Still not authenticated = return to login.php
if (!isset($_SESSION['authenticated']) || !$_SESSION['authenticated']) {
    header('Location: index.php');
    exit();
}

?>


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Locations</title>
    <link rel="stylesheet" href="styles/my_profile.css">
    <meta name="viewport" content="width=device-width, initial-scale=0.6">
</head>

<nav class="navbar">
    <div class="container">
        <div><h1 class="logo">Urbex Portal</h1></div>
        <div class="search-container">
        <ul class="menu">
        <li><a href="map.php">Map</a></li>
            <li><a href="locations.php">Visited locations</a></li>
            <li><a href="target_locations.php">Target locations</a></li>&emsp;
            <div class="dropdown">
                <div class="avatar">
                    <div class="user-icon"><span></span></div>
                </div>
                <div class="dropdown-content">
                <a href="my_profile.php">My Profile</a>
                    <a href="add_location.php">Add new location</a>
                    <a href="generate_invitation.php">Generate Invitation code</a>
		            <a href="utilities/logout.php">Logout</a>
                </div>
            </div>
        </ul>
        </div>
    </div>
</nav>
<div id="user_stats"></div>
<div class="location_category"><div>&emsp;&emsp;&emsp;</div><div>My Locations</div><div><a href="my_locations.php"><button>All locations</button></a></div></div>
<div id="location_container">
    <div id="locationsContainer"></div>
</div>

<!-- Include Location.js, LocationRepo.js -->
<script src="js/Location.js"></script>
<script src="js/LocationRepo.js"></script>

<script>
    let allLocations = [];
    let rang = null;
    let my_location_counter = 0;

    async function getRank() {
        const response = await fetch("utilities/retrieve_user_rang.php");
        const data = await response.json();
        rang = data.user_rang
        return rang;
    }

    async function loadUserDetails() {
        const userStats = document.getElementById("user_stats");
        const rang = await getRank();


        userStats.innerHTML += `
            <div class="location_category"><div></div>My Profile<div></div></div>
            <div style="margin: 20px; text-align: center;">
                <h3>Username: <?php echo $_SESSION['username'] ?></h3>`;
                if (rang === "DEV"){
                    userStats.innerHTML += `<h3>Rang: <div class='DEV_rang'>${rang}</div></h3>`;
                } else if (rang === "admin"){
                    userStats.innerHTML += `<h3>Rang: <div class='admin_rang'>${rang}</div></h3>`;
                } else if (rang === "explorer"){
                    userStats.innerHTML += `<h3>Rang: <div class='explorer_rang'>${rang}</div></h3>`;
                } else if (rang === "member"){
                    userStats.innerHTML += `<h3>Rang: <div class='member_rang'>${rang}</div></h3>`;
                } else if (rang === "user"){
                    userStats.innerHTML += `<h3>Rang: <div class='user_rang'>${rang}</div></h3>`;
                }
                
                userStats.innerHTML +=  `<h3>Total locations added: ${my_location_counter}</h3>
            </div>`;
    }

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

    async function loadLocations(util_name) {
        try {
            const userId = await getUserId();
            if (!userId) {
                console.error('Failed to retrieve user ID');
                return [];
            }

            const response = await fetch(`utilities/${util_name}`);
            const locations = await response.json();
            return locations;
        } catch (error) {
            console.error('Error:', error);
            return [];
        }
    }

    async function displayLocations(locations) {
        const userId = await getUserId();
        const locationsContainer = document.getElementById('locationsContainer');
        locationsContainer.innerHTML = '';

        const filteredLocations = locations.filter(location => location.created_by == userId);
        my_location_counter =filteredLocations.length;
        if (filteredLocations.length > 0) {
            // Only display the first 12 locations
            const limitedLocations = filteredLocations.slice(0, 12);
            limitedLocations.forEach((location, index) => {
                const locationCard = document.createElement('div');
                locationCard.classList.add('location-card');
                if (locations.length === 1) {
                    locationCard.classList.add('single-location');
                }

                const anchor = document.createElement('a');
                if (location.visitDate) {
                    anchor.href = `location_detail.php?locationId=${location.id}`;
                } else {
                    anchor.href = `target_detail.php?locationId=${location.id}`;
                }

                const titleImage = document.createElement('img');
                if (location.visitDate) {
                    titleImage.src = `images/${location.id}/${location.titleImage}`;
                } else {
                    titleImage.src = `images/targets/${location.id}/${location.titleImage}`;
                }
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
        } else {
            locationsContainer.innerHTML = "<div><h2>You don't have any location.</h2><a style='color: white; text-decoration: none;' href='add_location.php'>Click here to add a new location!</a></div>";
        }
    }

    (async function() {
        const allVisitedLocations = await loadLocations("retrieve_visited_locations.php");
        const allTargetLocations = await loadLocations("retrieve_target_locations.php");
        allLocations = allVisitedLocations.concat(allTargetLocations);
        displayLocations(allLocations);
        loadUserDetails();
    })();
</script>
</html>
