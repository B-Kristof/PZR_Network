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

function generateInvitationCode($length = 10) {
    $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    $charactersLength = strlen($characters);
    $randomString = '';
    for ($i = 0; $i < $length; $i++) {
        $randomString .= $characters[rand(0, $charactersLength - 1)];
    }
    return $randomString;
}


function hashInvitationCode($code) {
    return hash('sha3-512', $code);
}

$message = '';

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // Get username from session
    $username = $_SESSION['username'] ?? '';

    if (!empty($username)) {

        // Retrieve user ID from the database using the hashed username
        $stmt = $conn->prepare("SELECT id FROM users WHERE username = ?");
        $stmt->bind_param("s", $username);
        
        if ($stmt->execute()) {
            $result = $stmt->get_result();

            if ($result->num_rows > 0) {
                $user = $result->fetch_assoc();
                $user_id = $user['id'];

                // Generate invitation code
                $invitation_code = generateInvitationCode();
                $hashed_code = hashInvitationCode($invitation_code);

                // Insert invitation code into database along with user ID
                $stmt = $conn->prepare("INSERT INTO invitations (code_hash, creator_id) VALUES (?, ?)");
                $stmt->bind_param("si", $hashed_code, $user_id);

                if ($stmt->execute()) {
                    $message = "Invitation code generated: " . $invitation_code;
                } else {
                    $message = "Error inserting invitation code: " . $stmt->error;
                }
            } else {
                $message = "User not found";
            }
        } else {
            $message = "Error executing user query: " . $stmt->error;
        }

        $stmt->close();
    } else {
        $message = "Session username not set";
    }
} else {
    // Retrieve user's rang from the database
    $username = $_SESSION['username'] ?? '';
    if (!empty($username)) {
        $stmt = $conn->prepare("SELECT rang FROM users WHERE username = ?");
        $stmt->bind_param("s", $username);
        
        if ($stmt->execute()) {
            $result = $stmt->get_result();

            if ($result->num_rows > 0) {
                $user = $result->fetch_assoc();
                $user_rang = $user['rang'];

                // Check user's rang and display message accordingly
                if ($user_rang == 'user') {
                    $message = '<br>You need to be at least a "member" to generate invitation codes.<br><br>To become a member you need to add at least 5 VISITED locations (all of them must be verified)!';
                } else {
                    // User can generate invitation codes
                    // No message needed here as the form will be displayed
                }
            } else {
                $message = "User not found";
            }
        } else {
            $message = "Error executing user query: " . $stmt->error;
        }

        $stmt->close();
    } else {
        $message = "Session username not set";
    }
}

$conn->close();
?>

<!DOCTYPE html>
<html>
<head>
    <title>Generate Invitation Code</title>
    <link rel="stylesheet" href="styles/generate_invitation.css">
    <script>
        function copyToClipboard() {
            const codeElement = document.getElementById('invitation_code');
            const range = document.createRange();
            range.selectNode(codeElement);
            window.getSelection().removeAllRanges();
            window.getSelection().addRange(range);
            document.execCommand('copy');
            //alert('Invitation code copied to clipboard: ' + codeElement.innerText);
        }
    </script>

</head>
<body>
    <div class="container">
        <nav class="navbar">
            <h1 class="logo">Urbex Portal</h1>
	     <ul class="menu">
                <li><a href="locations.php">Visited locations</a></li>
                <li><a href="target_locations.php">Target locations</a></li>
            </ul>
        </nav>
        <h1>Generate Invitation Code</h1>
        <?php
        if ($user_rang != 'user') {
            echo "<h2 style='color: red; font-size: 15px;'>Warning: You won't be able to access this code after you close this page!</h2>";
            echo "<h2 style='color: red; font-size: 15px;''>You are able to use this code once.</h2>";
            echo '<form method="post" action="">';
            echo '<button class="btn" type="submit">Generate Invitation Code</button>';
            echo '</form>';
        }
        ?>
        <?php
        if (!empty($invitation_code)) {
            echo "<h2>Invitation code:</h2>";
            echo '<h2 id="invitation_code">' . $invitation_code . '</h2>';
            echo '<button class="btn" onclick="copyToClipboard()">Copy Invitation Code</button>';
        }
        ?>
        <p><?php echo $message; ?></p>
    </div>
</body>
</html>
