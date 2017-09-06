<html>
    <body>
        <?php
        $servername = "localhost";
        $dbname = "rpihome";
        $username = "python";
        $password = "python";

        // Create connection
        $conn = new mysqli($servername, $username, $password, $dbname);

        // Check connection
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }

        $devname = $_POST['devname'];

        // Execute query
        $sql = "SELECT device, status FROM device_log WHERE device = '$devname' AND (device, timestamp) IN (SELECT device, Max(timestamp) FROM device_log GROUP BY device) LIMIT 1";
        $result = $conn->query($sql);

        // Check and return results
        if ($result->num_rows > 0) {
            // output data of each row
            while($row = $result->fetch_assoc()) {
                echo $row['status'];
            }
        } else {
            echo "??";
        }

        // Close connection to database
        $conn->close();
        ?>

    </body>
</html>
