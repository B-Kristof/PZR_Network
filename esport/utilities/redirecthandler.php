<?php
// Define allowed domains to avoid open redirection vulnerability
$allowedDomains = [
    'www.instagram.com',
    'www.youtube.com',
    'www.twitch.tv',
    'www.discord.gg',
    'www.tiktok.com',
    'rajtvonalmagazin.hu',
    'mtsimtech.hu',
    'hypeitmarketing.hu',
    'www.skynet-computer.hu',
    'nbnhutestechnika.hu',
    'simhome.hu'
];

// Path to the log file
$logFile = 'redirect_log.txt';

// Function to log redirects
function logRedirect($src, $dst, $logFile) {
    $timestamp = date('Y-m-d H:i:s'); // Get current timestamp
    $logEntry = "$src;$timestamp;$dst" . PHP_EOL; // Create log entry

    // Append log entry to the log file
    file_put_contents($logFile, $logEntry, FILE_APPEND | LOCK_EX);
}

// Validate the input parameters
if (isset($_GET['src']) && isset($_GET['dst'])) {
    $src = filter_var($_GET['src'], FILTER_SANITIZE_URL);
    $dst = filter_var($_GET['dst'], FILTER_SANITIZE_URL);

    // Check if the destination URL belongs to the allowed domains
    $parsedUrl = parse_url($dst);
    if (isset($parsedUrl['host']) && in_array($parsedUrl['host'], $allowedDomains)) {
        // Log the redirect
        logRedirect($src, $dst, $logFile);

        // Perform the redirection
        header("Location: $dst");
        exit;
    } else {
        // Invalid destination URL (not in allowed domains)
        echo "Invalid destination URL.";
        exit;
    }
} else {
    // Missing URL parameters
    echo "Invalid request.";
    exit;
}
