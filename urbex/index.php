<?php
session_start();
// Hash function
function calculateSHA3_512($input) {
    return hash('sha3-512', $input);
}

function loginWithHash($conn, $inputUsername, $inputPassword) {
    $hashedPassword = calculateSHA3_512($inputPassword);

    $sql = "SELECT * FROM users WHERE username = :username AND password = :password";
    $stmt = $conn->prepare($sql);
    $stmt->bindParam(':username', $inputUsername);
    $stmt->bindParam(':password', $hashedPassword);
    $stmt->execute();
    $user = $stmt->fetch();

    if ($user) {
        $_SESSION['authenticated'] = true;
        $_SESSION['username'] = $inputUsername;
        return true;
    } else {
        return false;
    }
}

// Check if the form is submitted
$errorMessage = ''; // Initialize errorMessage
if (isset($_POST['login'])) {
    // Database connection parameters
    $host = '127.0.0.1';
    $username_d = 'urbex';
    $password_d = 'PZRUrbexsql';
    $database = 'pzr_urbex';

    try {
        $conn = new PDO("mysql:host=$host;dbname=$database", $username_d, $password_d);
        $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    } catch (PDOException $e) {
        die("Connection failed: " . $e->getMessage());
    }
    $inputUsername = $_POST['username'];
    $inputPassword = $_POST['password'];

    if (loginWithHash($conn, $inputUsername, $inputPassword)) {
        // Redirect to the main page
        header('Location: locations.php');
        exit();
    } else {
        $errorMessage = 'Invalid username or password.';
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Urbex Login</title>

    <!-- Desktop style -->
    <link rel="stylesheet" href="styles/index.css" media="screen and (min-device-width: 767px)">

    <!-- Mobile style -->
    <link rel="stylesheet" type="text/css" media="screen and (max-device-width: 767px)" href="styles/mobile/index_mobile.css"/>
</head>
<body>
    <div class="container">
        <div class="login-container">
            <h2>PZR Urbex Portal</h2>
            <form id="login-form" method="post" action="<?php echo htmlspecialchars($_SERVER['PHP_SELF'], ENT_QUOTES, 'UTF-8'); ?>">
                <div class="input-group">
                    <label for="username">Username</label>
                    <input type="text" id="username" name="username" required>
                </div>
                <div class="input-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <!-- Failed login attempt -->
                <?php if (!empty($errorMessage)): ?>
                    <div class="error-message">
                        <?php echo $errorMessage; ?>
                    </div>
                <?php endif; ?>
                <button type="submit" name="login">Login</button>
            </form><br>
            <form action="register.php">
                <button type="submit">Create new account</button>
            </form>
        </div>
    </div>
</body>
</html>
