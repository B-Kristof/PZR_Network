<?php
// Retrieve images from server (backend code)
$dir = '../images/gallery';

// Get all image files from the directory
$images = array_filter(scandir($dir), function($file) use ($dir) {
    return in_array(pathinfo($file, PATHINFO_EXTENSION), ['jpg', 'jpeg', 'png', 'gif']);
});

// Return the image list as JSON
echo json_encode(array_values($images));