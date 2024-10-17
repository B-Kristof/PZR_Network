<?php
session_start();
// Still not authenticated = return to login.php
if (!isset($_SESSION['authenticated']) || !$_SESSION['authenticated']) {
    header('Location: index.php');
    exit();
}

// Database configuration
$db_host = 'localhost';
$db_user = 'root';
$db_pass = '';
$db_name = 'pzr_urbex';

// Establish database connection
$conn = new mysqli($db_host, $db_user, $db_pass, $db_name);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

function getUserRangById($conn, $userId) {
    $stmt = $conn->prepare("SELECT rang FROM users WHERE id = ?");
    $stmt->bind_param("i", $userId);
    $stmt->execute();
    $result = $stmt->get_result();
    if ($result->num_rows > 0) {
        $user = $result->fetch_assoc();
        return $user['rang'];
    } else {
        return false; // User not found
    }
}

function get_id(){
    // Retrieve the username from the session
    $username = $_SESSION['username'] ?? '';

    // Database connection details
    $servername = "localhost";
    $dbname = "pzr_urbex";
    $dbusername = "root";
    $dbpassword = "";

    // Create a connection to the MySQL database
    $conn = new mysqli($servername, $dbusername, $dbpassword, $dbname);

    // Check the connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    // Prepare and execute the SQL query
    $sql = "SELECT id FROM users WHERE username = ?";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("s", $username);
    $stmt->execute();
    $stmt->bind_result($user_id);

    // Fetch the result
    if ($stmt->fetch()) {
        $conn->close();
        return $user_id;
    } else {
        $conn->close();
        return 0;
    }
}

$user_id = get_id();
echo json_encode(['user_rang' => getUserRangById($conn, $user_id)]);

$conn->close();
?>
