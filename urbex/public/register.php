<?php
// Start session
session_start();

// Database configuration
$db_host = '127.0.0.1';
$db_user = 'urbex';
$db_pass = 'PZRUrbexsql';
$db_name = 'pzr_urbex';

// Enable error reporting
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Establish database connection
$conn = new mysqli($db_host, $db_user, $db_pass, $db_name);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

function hashString($string) {
    return hash('sha3-512', $string);
}

$message = '';

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';
    $invitation_code = $_POST['invitation_code'] ?? '';

    if (!empty($username) && !empty($password) && !empty($invitation_code)) {
        // Hash the username and password using SHA3-512
        $hashed_password = hashString($password);

        // Validate invitation code
        $hashed_invitation_code = hashString($invitation_code);
        $stmt = $conn->prepare("SELECT id, creator_id FROM invitations WHERE code_hash = ? AND is_used = 0");
        if ($stmt === false) {
            die("Invalid invitation code!");
        }
        
        $stmt->bind_param("s", $hashed_invitation_code);
        
        if ($stmt->execute()) {
            $result = $stmt->get_result();
            if ($result->num_rows > 0) {
                // Invitation code is valid
                $invitation = $result->fetch_assoc();
                $invitation_id = $invitation['id'];
                $creator_id = $invitation['creator_id'];

                // Insert user data into database
                $stmt = $conn->prepare("INSERT INTO users (username, password, invited_by) VALUES (?, ?, ?)");
                if ($stmt === false) {
                    die("Error in user insertion query: " . $conn->error);
                }
                
                $stmt->bind_param("ssi", $username, $hashed_password, $creator_id);
                
                if ($stmt->execute()) {
                    // Mark invitation code as used
                    $update_stmt = $conn->prepare("UPDATE invitations SET is_used = 1 WHERE id = ?");
                    if ($update_stmt === false) {
                        die("Error updating invitation code: " . $conn->error);
                    }
                    $update_stmt->bind_param("i", $invitation_id);
                    $update_stmt->execute();

                    $message = "Registration successful! You can now log in.";
                } else {
                    $message = "Error inserting user data: " . $stmt->error;
                }
            } else {
                $message = "Invalid invitation code.";
            }
        } else {
            $message = "Error executing invitation code validation query: " . $stmt->error;
        }

        $stmt->close();
    } else {
        $message = "Please fill in all fields.";
    }
}

$conn->close();
?>

<!DOCTYPE html>
<html>
<head>
    <title>Urbex Portal</title>
    <link rel="stylesheet" href="styles/register.css">
</head>
<body>
<div class="container">
        <div class="login-container">
            <h2>PZR Urbex Portal</h2>
            <form method="post" action="register.php">
                <div class="input-group">
                    <label for="username">Username:</label>
                    <input type="text" id="username" name="username" required>
                </div>
                <div class="input-group">
                    <label for="password">Password:</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <div class="input-group">
                    <label for="invitation_code">Invitation Code:</label>
                    <input type="text" id="invitation_code" name="invitation_code" required>
                </div>
                <div class="error-message">
                <?php
                if (isset($message)) {
                    echo '<p>' . $message . '</p>';
                }
                ?>
                </div>
                <button type="submit">Register</button>
            </form>
            <br>
            <form action="index.php">
                <button type="submit">I have an account</button>
            </form>
        </div>
    </div>
</body>
</html>
