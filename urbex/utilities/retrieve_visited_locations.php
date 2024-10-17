<?php

session_start();
// Still not authenticated = return to login.php
if (!isset($_SESSION['authenticated']) || !$_SESSION['authenticated']) {
    header('Location: index.php');
    exit();
}

// Function to retrieve locations list
function retrieveLocations() {
    $locations = []; // Initialize an empty array
    // Check if the locations JSON file exists
    if (file_exists('../data/locations.json')) {
        // Read the JSON file and decode it into an array
        $json_data = file_get_contents('../data/locations.json');
        $locations = json_decode($json_data, true);
    }
    return $locations;
}

// Get the locations list
$locationsList = retrieveLocations();

echo json_encode($locationsList);
?>
