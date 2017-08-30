<html>
    <body>
        <?php
        $servername = "localhost";
        $dbname = "rpihome";        
        $username = "python";
        $password = "python";
        $dbname = "rpihome";

        // Create connection
        $conn = new mysqli($servername, $username, $password, $dbname);

        // Check connection
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }

        // Execute query
        $sql = "SELECT device, status FROM device_log WHERE device = '$_POST[devName]' AND (device, timestamp) IN (SELECT device, Max(timestamp) FROM device_log GROUP BY device) LIMIT 1";
        $result = $conn->query($sql);

        // Check and return results
        if ($result->num_rows > 0) {
            // output data of each row
            while($row = $result->fetch_assoc()) {
                echo "device: " . $row["device"]. " - " . $row["status"]. "<br>";
            }
        } else {
            echo "0 results";
        }

        // Close connection to database
        $conn->close();
        ?>

    </body>
</html>
