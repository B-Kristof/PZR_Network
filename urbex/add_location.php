<?php
// ---- AUTH START -----
require_once 'Auth.php';
$auth = new Auth();

if (!$auth->isAuthenticated()) {
    header("Location: /urbex/public/index.php");
    exit;
}

// ---- AUTH END -----


// Handle the form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Directory where images will be saved
    if (isset($_POST['visitedSwitch'])){
        $baseDir = "images/";
        $jsonFile = 'data/locations.json';
    }
    else{
        $baseDir = "images/targets/";
        $jsonFile = 'data/target_locations.json';
    }

    // Helper function to handle image upload
    function uploadImage($imageName, $targetDir, $newFileName = null) {
        $targetFile = $targetDir . ($newFileName ? $newFileName : basename($_FILES[$imageName]["name"]));
        $imageFileType = strtolower(pathinfo($targetFile, PATHINFO_EXTENSION));
        

        // Allow certain file formats
        if ($imageFileType != "jpg" && $imageFileType != "jpeg") {
            echo "Sorry, only JPG, JPEG files are allowed.";
            return null;
        }

        // Try to upload file
        if (move_uploaded_file($_FILES[$imageName]["tmp_name"], $targetFile)) {
            return basename($targetFile); // Return only the filename
        } else {
            echo "Sorry, there was an error uploading your file.";
            return null;
        }
    }

    // Load existing locations

    if (file_exists($jsonFile)) {
        $locations = json_decode(file_get_contents($jsonFile), true);
    } else {
        $locations = [];
    }

    // Determine the new ID
    if (!empty($locations)) {
        $lastLocation = end($locations);
        $newId = $lastLocation['id'] + 1;
    } else {
        $newId = 1;
    }

    // Collect form data
    $name = $_POST['name'];
    $coordinates = $_POST['coordinates'];
    $address = $_POST['address'];
    if ($address == ""){
        $address = null;
    }
    $visitDate = $_POST['visitDate'];
    if ($visitDate == ""){
        $visitDate = null;
    }
    $partofDay = $_POST['partofDay'];
    if ($partofDay == ""){
        $partofDay = null;
    }
    $factor = $_POST['factor'];
    if ($factor == ""){
        $factor = null;
    }
    $description = $_POST['description'];
    if ($description == ""){
        $description = null;
    }
    $links = explode(',', $_POST['links']); // Split the links by comma to create an array
    if ($links == [""]){
        $links = null;
    }

    // Trim whitespace from each link
    if ($links){
        $links = array_map('trim', $links);
    }

    // Create a directory for the new location
    $locationDir = $baseDir . $newId . "/";
    if (!file_exists($locationDir)) {
        mkdir($locationDir, 0777, true);
    }

    // Upload the title image
    $titleImage = uploadImage('titleImage', $locationDir, 'title.jpg');

    // Initialize $images array before using it
    $images = [];

    // Upload additional images
    if (isset($_FILES['images']['name'])) {
        foreach ($_FILES['images']['name'] as $key => $value) {
            if ($_FILES['images']['tmp_name'][$key]) {
                $imageName = 'images_' . $key;
                $_FILES[$imageName] = [
                    'name' => $_FILES['images']['name'][$key],
                    'type' => $_FILES['images']['type'][$key],
                    'tmp_name' => $_FILES['images']['tmp_name'][$key],
                    'error' => $_FILES['images']['error'][$key],
                    'size' => $_FILES['images']['size'][$key]
                ];
                $uploadedImage = uploadImage($imageName, $locationDir);
                if ($uploadedImage) {
                    // Use [] to append to array instead of array_push()
                    $images[] = $uploadedImage;
                }
            }
        }
    }

    // Include the file with the get_id function
    require __DIR__ . '/utilities/get_userid_by_username.php';
    
    // Get the user ID
    $userid = get_id();
    

    // Create a location array
    $location = [
        "id" => $newId,
        "created_by" => $userid,
        "name" => $name,
        "coordinates" => $coordinates,
        "address" => $address,
        "visitDate" => $visitDate,
        "partofDay" => $partofDay,
        "factor" => $factor,
        "description" => $description,
        "titleImage" => $titleImage,
        "images" => $images,
        "links" => $links
    ];

    // Append new location to the list
    $locations[] = $location;

    // Save locations back to the file with JSON_UNESCAPED_UNICODE and JSON_UNESCAPED_SLASHES
    file_put_contents($jsonFile, json_encode($locations, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES));

    echo "<div style='color: green; text-align: center; font-size: 18px;'><strong>Location added successfully!</strong></div>";
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Add Location</title>
    <link rel="stylesheet" href="styles/add_location.css">
    <script>
        function validateForm() {
            const titleImage = document.getElementById('titleImage').value;
            const images = document.getElementById('images').files;
            const allowedExtensions = /(\.jpg|\.jpeg)$/i;

            if (!allowedExtensions.exec(titleImage)) {
                alert('Only JPG and JPEG files are allowed for the title image.');
                return false;
            }

            for (let i = 0; i < images.length; i++) {
                if (!allowedExtensions.exec(images[i].name)) {
                    alert('Only JPG and JPEG files are allowed for images.');
                    return false;
                }
            }

            return true;
        }

        function toggleForm() {
            const visitedSwitch = document.getElementById('visitedSwitch');
            const visitFields = document.querySelectorAll('.visit-fields');
            const sw = document.getElementById('switch');
            const sw_state = document.getElementById('visitedSwitch');
            if (sw_state.checked) {
                sw.style.background = "#333";
            } else {
                sw.style.background = "#ababab";
            }

            visitFields.forEach(field => {
                field.style.display = visitedSwitch.checked ? 'block' : 'none';
            });
        }

        function addLocation() {
            if (validateForm()) {
                var form = document.getElementById("imageForm");
                var formData = new FormData(form);

                var xhr = new XMLHttpRequest();
                xhr.open("POST", "add_location.php");
                xhr.upload.addEventListener("progress", function(event) {
                    if (event.lengthComputable) {
                        var percentComplete = (event.loaded / event.total) * 100;
                        var progressBar = document.getElementById("progressBar");
                        progressBar.style.display = "flex"
                        progressBar.value = percentComplete;
                        if (percentComplete === 100){
                            alert("Location added!");
                            location.reload()
                        }
                    }
                });

                xhr.onload = function() {
                    // Handle response from server
                    console.log(xhr.responseText);
                };

                xhr.send(formData);
            }
        }
    </script>
</head>
<body>

<nav class="navbar">
    <h1 class="logo">Urbex Portal</h1>
    <ul class="menu">
        <li><a href="locations.php">Visited locations</a></li>&emsp;
        <li><a href="target_locations.php">Target locations</a></li> 
        <a href="my_profile.php"><div class="avatar">
            <div href="my_profile.php" class="user-icon"><span></span></div>
        </div></a>
    </ul>
</nav>

<div class="container">
    <h1>Add Location</h1>
    <!-- Add an ID to the form for easier targeting -->
    <form id="imageForm" action="add_location.php" method="post" enctype="multipart/form-data" onsubmit="return validateForm()">
        <label>Visited: &ensp;</label>
        <div class="form-group" style="display: inline-flex">
            <label id="switch" class="switch" for="visitedSwitch">
                <input type="checkbox" id="visitedSwitch" name="visitedSwitch" onclick="toggleForm()"/>
                <div></div>
            </label>
        </div>

        <div class="form-group">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required>
        </div>

        <div class="form-group">
            <label for="coordinates">Coordinates:</label>
            <input type="text" id="coordinates" name="coordinates" required>
        </div>

        <div class="form-group">
            <label for="address">Address:</label>
            <input type="text" id="address" name="address">
        </div>

        <div class="form-group visit-fields" style="display:none;">
            <label for="visitDate">Visit Date:</label>
            <input type="date" id="visitDate" name="visitDate">
        </div>

        <div class="form-group visit-fields" style="display:none;">
            <label for="partofDay">Part of Day:</label>
            <input type="text" id="partofDay" name="partofDay">
        </div>

        <div class="form-group">
            <label for="factor">Factor:</label>
            <input type="text" id="factor" name="factor">
        </div>

        <div class="form-group">
            <label for="description">Description:</label>
            <textarea id="description" name="description"></textarea>
        </div>

        <div class="form-group">
            <label for="links">Links:</label>
            <textarea id="links" name="links" placeholder="Enter links separated by commas"></textarea>
        </div>

        <div class="form-group">
            <label for="titleImage">Title Image:</label>
            <input type="file" id="titleImage" name="titleImage" accept=".jpg, .jpeg" required>
        </div>

        <div class="form-group">
            <label for="images">Images:</label>
            <input type="file" id="images" name="images[]" accept=".jpg, .jpeg" multiple>
        </div>

       <!-- Progress bar -->
       <progress style="display: none;" id="progressBar" value="0" max="100"></progress>

        <!-- Add Location button -->
        <button class="btn" type="button" onclick="addLocation()">Add Location</button>
    </form>
</div>

</body>
</html>
