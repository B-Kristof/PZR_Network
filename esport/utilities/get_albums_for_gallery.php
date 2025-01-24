<?php
// Base directory for folders
$baseDir = '../images/gallery';

// Resolve the real path of the base directory
$realBaseDir = realpath($baseDir);

// Check if the base directory is valid
if (!$realBaseDir || !is_dir($realBaseDir)) {
    echo json_encode([]);
    exit;
}

// Get all subfolders within the base directory
$folders = array_filter(glob($realBaseDir . '/*'), 'is_dir');

// Extract folder names
$folderNames = array_map(function ($folder) use ($realBaseDir) {
    return basename($folder); // Get the folder name only
}, $folders);

// Return the folder names as JSON
echo json_encode($folderNames);