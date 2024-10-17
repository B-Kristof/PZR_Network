<?php

session_start();
// Still not authenticated = return to login.php
if (!isset($_SESSION['authenticated']) || !$_SESSION['authenticated']) {
    header('Location: index.php');
    exit();
}

// get_images.php

// Check if locationId is provided in the GET parameters
if(isset($_GET['locationId'])) {
    // Sanitize the input to prevent directory traversal attacks
    $locationId = htmlspecialchars($_GET['locationId']);

    // Directory where images are stored
    $imageDir = "../images/$locationId/";

    // Check if the directory exists
    if(is_dir($imageDir)) {
        // Get list of files in the directory
        $files = scandir($imageDir);
        
        // Filter out non-image files
        $images = array_filter($files, function($file) {
            return preg_match('/\.(jpg|jpeg|png|gif)$/i', $file);
        });

        // Prepend the directory path to each image
        $images = array_map(function($image) use ($imageDir) {
            return $imageDir . $image;
        }, $images);

        // Send the image paths as JSON
        echo json_encode(['images' => array_values($images)]);
    } else {
        // Directory doesn't exist
        echo json_encode(['error' => 'Directory not found']);
    }
} else {
    // locationId not provided
    echo json_encode(['error' => 'locationId parameter is missing']);
}
?>
