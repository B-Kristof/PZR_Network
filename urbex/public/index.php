<?php
require_once 'Auth.php';
$auth = new Auth();

if ($auth->isAuthenticated()) {
	header("Location: /urbex/home.php");
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = trim($_POST['username']);
    $password = trim($_POST['password']);

    if ($auth->login($username, $password)) {
        header("Location: /urbex/home.php"); // Redirect to a protected page
        exit;
    } else {
        $_SESSION['failed_login'] = true;
    }
} elseif($_SERVER['REQUEST_METHOD'] === 'GET' && $auth->isAuthenticated()){
	header("Location: /urbex/home.php");
	exit;
}


?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Urbex Login</title>

    <!-- Desktop style -->
    <link rel="stylesheet" href="../styles/index.css" media="screen and (min-device-width: 767px)">

    <!-- Mobile style -->
    <link rel="stylesheet" type="text/css" media="screen and (max-device-width: 767px)" href="../styles/mobile/index_mobile.css"/>
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
