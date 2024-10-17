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
    <!-- Desktop style -->
    <link rel="stylesheet" href="styles/locations.css">
    <link rel="stylesheet" href="styles/top_menu.css" media="screen and (min-device-width: 767px)">

    <!--  Mobile style -->
    <meta name="viewport" content="width=device-width, initial-scale=0.6">

</head>
<body>
<nav class="navbar">
    <div class="menu-container">
        <h1 class="logo">Urbex Portal</h1>
        <div class="search-container">
        <ul class="menu">
            <li><a href="map.php">Map</a></li>
            <li><a href="target_locations.php">Target locations</a></li>
            <input type="text" id="searchInput" placeholder="Search locations by name">&ensp;
            <button class="button" onclick="searchLocations()">Search</button>
            <div class="dropdown">
                <div class="avatar">
                    <div class="user-icon"><span></span></div>
                </div>
                <div class="dropdown-content">
                <a class="dropdown_profile" href="my_profile.php">My Profile</a>
                    <a href="add_location.php">Add new location</a>
                    <a href="generate_invitation.php">Generate Invitation code</a>
		            <a href="utilities/logout.php">Logout</a>
                </div>
            </div>
        </ul>
        </div>
    </div>
</nav>

<div class="location_category">Visited locations</div>
<!-- Container to display locations -->
<div id="searchResult"></div>
<div id="locationsContainer"></div>

<!-- Include Location.js, LocationRepo.js -->
<script src="js/Location.js"></script>
<script src="js/LocationRepo.js"></script>

<script src="js/locations.js"></script>

</body>
</html>
