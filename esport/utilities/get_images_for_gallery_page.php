<?php
// Retrieve images for a specific year from the server
$year = $_GET['year'] ?? ''; // Get the year parameter from the URL

// Create whitelist to avoid Folder Enumeration attacks
$allowedYears = ['2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029'];

if (!in_array($year, $allowedYears)) {
    echo "This is not possible!";
    exit;
}

// Base directory for gallery images
$baseDir = '../images/gallery';

// Check if the directory for the given year exists
$dir = $baseDir . '/' . $year;
if (!is_dir($dir)) {
    echo json_encode([]); // Return an empty array if the directory doesn't exist
    exit;
}

// Get all image files from the directory
$images = array_filter(scandir($dir), function($file) use ($dir) {
    return in_array(pathinfo($file, PATHINFO_EXTENSION), ['jpg', 'jpeg', 'png', 'gif']);
});

// Return the image list as JSON
echo json_encode(array_values($images));