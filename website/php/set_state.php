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

        $devname = $_REQUEST['devname'];
        $devcmd = $_REQUEST['devcmd'];
        
         // Execute query
         $sql = "INSERT INTO device_cmd (device, cmd) VALUES ('$devname', '$devcmd')";

         // Exxecute query and return results
         if ($conn->query($sql) === TRUE) {
             echo "New record created successfully";
         } else {
             echo "Error: " . $sql . "<br>" . $conn->error;
         }

         // Close connection to database
         $conn->close();
        ?>

    </body>
</html>
