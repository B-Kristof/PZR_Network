<?php
if (!session_id()){
    session_start();
}

// Still not authenticated = return JSON error message
if (!isset($_SESSION['authenticated']) || !$_SESSION['authenticated']) {
    header('Location: index.php');
    exit();
}

function get_id(){
    // Retrieve the username from the session
    $username = $_SESSION['username'];

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

// Call the function and return the user ID as JSON
//header('Content-Type: application/json');
echo json_encode(['user_id' => get_id()]);
?>
